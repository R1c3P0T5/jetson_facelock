from fastapi.routing import APIRoute

from main import app, create_app


def test_create_app_returns_configured_fastapi_app() -> None:
    created_app = create_app()

    assert created_app.title == "Jetson Facelock API"
    assert created_app.version == "0.1.0"


def test_create_app_configures_cors_for_local_development() -> None:
    created_app = create_app()

    cors_middleware = [
        middleware
        for middleware in created_app.user_middleware
        if getattr(middleware.cls, "__name__", "") == "CORSMiddleware"
    ]

    assert len(cors_middleware) == 1
    assert getattr(cors_middleware[0], "kwargs")["allow_origins"] == [
        "http://localhost:3000",
        "http://localhost:8000",
    ]


def test_main_app_includes_auth_routes() -> None:
    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert ("/api/auth/register", ("POST",)) in routes
    assert ("/api/auth/login", ("POST",)) in routes
    assert ("/api/auth/token", ("POST",)) in routes
    assert ("/api/auth/me", ("GET",)) in routes


def test_main_app_includes_health_route() -> None:
    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert ("/health", ("GET",)) in routes
