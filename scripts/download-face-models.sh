#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MODELS_DIR="${SCRIPT_DIR}/models"

DETECTOR_FILE="face_detection_yunet_2023mar.onnx"
RECOGNIZER_FILE="face_recognition_sface_2021dec.onnx"

DETECTOR_URL="https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/${DETECTOR_FILE}"
RECOGNIZER_URL="https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/${RECOGNIZER_FILE}"

DETECTOR_SHA256="8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4"
RECOGNIZER_SHA256="0ba9fbfa01b5270c96627c4ef784da859931e02f04419c829e83484087c34e79"

download() {
  local url="$1"
  local output="$2"

  if command -v curl >/dev/null 2>&1; then
    curl --fail --location --show-error --output "${output}" "${url}"
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    wget --output-document="${output}" "${url}"
    return
  fi

  echo "Neither curl nor wget is installed." >&2
  return 1
}

verify_sha256() {
  local path="$1"
  local expected="$2"

  if ! command -v sha256sum >/dev/null 2>&1; then
    echo "sha256sum is required to verify ${path}." >&2
    return 1
  fi

  echo "${expected}  ${path}" | sha256sum --check --status
}

download_model() {
  local filename="$1"
  local url="$2"
  local checksum="$3"
  local output="${MODELS_DIR}/${filename}"
  local tmp="${output}.tmp"

  if [[ -f "${output}" ]] && verify_sha256 "${output}" "${checksum}"; then
    echo "${filename} already exists and passed checksum."
    return
  fi

  echo "Downloading ${filename}..."
  rm -f "${tmp}"
  download "${url}" "${tmp}"

  if ! verify_sha256 "${tmp}" "${checksum}"; then
    rm -f "${tmp}"
    echo "Checksum failed for ${filename}." >&2
    return 1
  fi

  mv "${tmp}" "${output}"
  echo "Saved ${output}"
}

mkdir -p "${MODELS_DIR}"

download_model "${DETECTOR_FILE}" "${DETECTOR_URL}" "${DETECTOR_SHA256}"
download_model "${RECOGNIZER_FILE}" "${RECOGNIZER_URL}" "${RECOGNIZER_SHA256}"

echo "Face models are ready in ${MODELS_DIR}."
