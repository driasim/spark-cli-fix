"""Tests for suspicious Docker volume path detection in approval."""
import pytest
from spark_cli.security.approval import approval_required_for_command, CommandContext

CTX = CommandContext()


def _check(path: str) -> bool:
    """Check if a docker -v mount of the given path requires approval."""
    result = approval_required_for_command(
        ["docker", "run", "-v", f"{path}:/mnt", "alpine"], CTX
    )
    return result.requires_approval


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/root",
        "/home",
        "/users",
        # New additions — previously unprotected system dirs
        "/usr",
        "/etc",
        "/var",
        "/opt",
        "/tmp",
        "/proc",
        "/sys",
        "/boot",
        "/dev",
        "/var/run/docker.sock",
    ],
)
def test_dangerous_volume_path_requires_approval(path: str) -> None:
    """All protected system paths should trigger approval."""
    assert _check(path), f"{path} should require approval"


def test_docker_run_without_volume_is_not_blocked() -> None:
    """Plain docker run without volume mounts should pass."""
    result = approval_required_for_command(["docker", "run", "alpine"], CTX)
    assert not result.requires_approval
