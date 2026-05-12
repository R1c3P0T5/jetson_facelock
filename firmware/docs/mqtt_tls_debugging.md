# Pico 2 W MQTT/TLS Debugging Notes

Date: 2026-04-28

## Goal

Make the Raspberry Pi Pico 2 W connect to the HiveMQ Cloud MQTT broker over TLS on port 8883, subscribe to the exact topic `DOOR`, and trigger GP15 when the payload starts with `1`.

The topic is not a sub-topic. `DOOR` is the full MQTT topic string. Topic matching is case-sensitive, so `DOOR`, `door`, `/DOOR`, and `DOOR/` are all different topics.

## Confirmed Observations

Initial serial logs showed:

- WiFi eventually connected.
- DNS resolved the HiveMQ Cloud hostname to an IP.
- TCP connected to broker port 8883.
- The program stopped progressing before `MQTT connected`.

That ruled out topic subscription as the first failure. MQTT topics only matter after the MQTT connection is accepted; the failure was happening earlier in the TLS/MQTT connection path.

After enabling mbedTLS debug, the TLS handshake was confirmed to complete:

```text
server hello, chosen ciphersuite: TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256
handshake: done
mqtt_tcp_connect_cb: TCP connection established to server
*** PANIC ***
```

This means the current blocker moved from TLS negotiation to the first MQTT CONNECT write after TLS succeeds.

A later normal-debug run showed a different panic point:

```text
[v] TLS SNI hostname set: ...
[v] mqtt_client_connect -> err=0
*** PANIC ***
```

There was no `mqtt_tcp_connect_cb` line in that run, which made the timing of the SNI change itself suspicious.

## Effective Changes Made

### TLS SNI

HiveMQ Cloud is a multi-tenant TLS service, so the TLS ClientHello needs the hostname, not just the resolved IP.

The first working attempt set SNI by reaching into lwIP MQTT private state after `mqtt_client_connect()` returned:

```c
mbedtls_ssl_context *ssl = (mbedtls_ssl_context *)altcp_tls_context(client->conn);
mbedtls_ssl_set_hostname(ssl, MQTT_HOST);
```

That proved SNI was required, but it was not a good final shape. It depended on `mqtt_priv.h` and modified the TLS context after lwIP MQTT had already started creating/connecting the PCB.

The current implementation uses a linker wrapper around `altcp_tls_new()`:

```c
struct altcp_pcb *__wrap_altcp_tls_new(struct altcp_tls_config *config, u8_t ip_type) {
    struct altcp_pcb *pcb = __real_altcp_tls_new(config, ip_type);
    mbedtls_ssl_set_hostname(altcp_tls_context(pcb), MQTT_HOST);
    return pcb;
}
```

`CMakeLists.txt` enables this with:

```cmake
target_link_options(blink PRIVATE "-Wl,--wrap=altcp_tls_new")
```

This matches the timing used by the local Pico HTTP client example: set SNI immediately after TLS PCB allocation and before `altcp_connect()` starts the TLS session.

This was verified in the TLS debug log:

```text
client hello, adding server name extension: 447423265c34458d9135d462c59b08e8.s1.eu.hivemq.cloud
```

### ECDHE-RSA Cipher Support

The broker selected:

```text
TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256
```

`mbedtls_config.h` now includes:

```c
#define MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED
```

This is an effective fix. Without ECDHE-RSA enabled, the client may not offer the cipher suite HiveMQ selects for TLS 1.2.

### Real TLS Debug Output

`MBEDTLS_DEBUG_C` alone was not enough. mbedTLS also requires a runtime threshold:

```c
mbedtls_debug_set_threshold(4);
```

That produced the detailed handshake log used to confirm SNI and cipher negotiation.

This runtime threshold was later removed because level 4 prints very sensitive and heavy output, including TLS key material. Do not keep verbose TLS debug enabled in normal firmware.

### lwIP Memory

After TLS succeeded, the program panicked immediately after:

```text
mqtt_tcp_connect_cb: TCP connection established to server
```

The likely path is `mqtt_output_send()` calling `altcp_write()` with the MQTT CONNECT packet. In Pico SDK's `altcp_tls_mbedtls.c`, the TLS write path can assert if TCP write fails unexpectedly, and verbose TLS debug also consumes significant RAM and output bandwidth.

`lwipopts.h` now increases:

```c
#define MEM_SIZE 65536
```

Verbose lwIP/TCP/MQTT/mbedTLS debug is also disabled for the normal test build:

```c
#define MQTT_DEBUG              LWIP_DBG_OFF
#define ALTCP_MBEDTLS_LIB_DEBUG LWIP_DBG_OFF
#define TCP_DEBUG               LWIP_DBG_OFF
```

The later normal-debug run still panicked immediately after `mqtt_client_connect -> err=0`. Re-reading lwIP's official MQTT documentation showed an important missing setting: MQTT needs one additional `SYS_TIMEOUT` slot for its cyclic timer. The detailed TLS log also showed the panic happened right after `mqtt_tcp_connect_cb: TCP connection established to server`, and lwIP MQTT schedules that cyclic timer before sending the MQTT CONNECT packet.

`lwipopts.h` now includes:

```c
#define MEMP_NUM_SYS_TIMEOUT 16
```

This is the current most evidence-based fix for the immediate panic.

## Things Proven Not To Be The Root Cause

- `DOOR` topic spelling is not the initial connection blocker. It only affects messages after MQTT connection and subscription.
- DNS is working.
- TCP port 8883 is reachable.
- TLS SNI is now present.
- TLS 1.2 handshake can complete.
- HiveMQ selected a supported ECDHE-RSA cipher after enabling `MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED`.
- The lwIP MQTT timeout pool was previously underconfigured for MQTT's extra cyclic timer.

## Current Expected Test

Build:

```powershell
cmake --build build
```

Flash `build/blink.uf2`.

Expected successful serial sequence:

```text
[+] WiFi connected
[+] resolved ...
[v] TLS SNI hostname set: ...
[v] mqtt_client_connect -> err=0
[+] MQTT connected
[+] subscribed to DOOR
```

Then publish payload `1` to topic `DOOR`. Expected result:

```text
[+] DOOR trigger received
[+] GP15 HIGH
[+] GP15 LOW
```

## If It Still Panics

The next useful data is the last 20-40 serial lines before `*** PANIC ***` with normal debug disabled. Avoid TLS debug level 4 unless needed, because it prints sensitive key material.

If the panic still happens immediately after `mqtt_client_connect -> err=0`, capture whether there are any lines after that. If the next line is still only `*** PANIC ***`, investigate the async-context/lwIP timer path after returning from `mqtt_client_connect()`. If it reaches `mqtt_tcp_connect_cb` first, inspect the Pico SDK TLS write path around `altcp_mbedtls_write()` and `altcp_mbedtls_bio_send()`. The likely failure class is memory or send-buffer pressure during the first encrypted MQTT CONNECT write, not HiveMQ authentication or topic subscription.
