import ipaddress
import socket
from urllib.parse import urlparse, urlunparse

from app.config.settings import Settings


class UrlValidationError(ValueError):
    pass


def canonicalize_url(url: str, settings: Settings) -> tuple[str, str]:
    value = (url or "").strip()
    if not value:
        raise UrlValidationError("URL is required.")
    if len(value) > settings.MAX_URL_LENGTH:
        raise UrlValidationError("URL exceeds maximum allowed length.")

    parsed = urlparse(value)
    if parsed.scheme.lower() not in settings.allowed_schemes_set:
        raise UrlValidationError("URL scheme is not allowed.")
    if not parsed.netloc:
        raise UrlValidationError("URL host is missing.")

    hostname = parsed.hostname
    if not hostname:
        raise UrlValidationError("URL hostname is invalid.")

    _enforce_host_policy(hostname, settings)

    canonical = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path or "/",
            "",
            parsed.query,
            "",
        )
    )
    return canonical, hostname.lower()


def _enforce_host_policy(hostname: str, settings: Settings) -> None:
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_loopback and not settings.LOOPBACK_SCAN_ALLOWED:
            raise UrlValidationError("Loopback addresses are blocked.")
        if ip.is_private and not settings.PRIVATE_NETWORK_SCAN_ALLOWED:
            raise UrlValidationError("Private network addresses are blocked.")
        return
    except ValueError:
        pass

    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return

    for info in infos:
        addr = info[4][0]
        try:
            ip = ipaddress.ip_address(addr)
        except ValueError:
            continue
        if ip.is_loopback and not settings.LOOPBACK_SCAN_ALLOWED:
            raise UrlValidationError("Hostname resolves to loopback address.")
        if ip.is_private and not settings.PRIVATE_NETWORK_SCAN_ALLOWED:
            raise UrlValidationError("Hostname resolves to private network address.")
