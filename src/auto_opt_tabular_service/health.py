from datetime import datetime, timezone
from importlib.metadata import version, PackageNotFoundError
import os

from fastapi import APIRouter

router = APIRouter()

try:
	SERVICE_VERSION = version("auto-opt-tabular-service")
except PackageNotFoundError:
	SERVICE_VERSION = "unknown"

BUILD_SHA = os.environ.get("BUILD_SHA", "unknown")

SERVICE_NAME = "auto-opt-tabular-service"

@router.get("/health")
def health() -> dict:
	"""Liveness + version check. Must stay fast and dependency-free."""
	return {
		"status": "ok",
		"service": SERVICE_NAME,
		"version": SERVICE_VERSION,
		"build_sha": BUILD_SHA,
		"timestamp": datetime.now(timezone.utc).isoformat(),
	}
