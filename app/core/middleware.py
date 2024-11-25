from fastapi.middleware.cors import CORSMiddleware


def setup_middleware(app):
    cors_options = {
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_origins": ["*"],
        "allow_credentials": True,
    }

    app.add_middleware(CORSMiddleware, **cors_options)
