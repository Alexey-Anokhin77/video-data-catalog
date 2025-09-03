from api.api_v1.video_catalog.dependencies import UNSAFE_METHOD


def test_unsafe_methods_doesnt_contain_safe_methods() -> None:
    safe_methods = {
        "GET",
        "HEAD",
        "OPTIONS",
    }

    assert not UNSAFE_METHOD & safe_methods
