import csv
import json
import logging
from pathlib import Path
from urllib import error, request

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

LEADS_DIR = Path(settings.BASE_DIR) / "leads"
LEADS_FILE = LEADS_DIR / "leads.csv"
LEAD_COLUMNS = [
    "timestamp",
    "event_type",
    "username",
    "email",
    "full_name",
    "phone",
    "primary_goal",
    "message",
]


def ensure_leads_file():
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    if LEADS_FILE.exists():
        return
    with LEADS_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LEAD_COLUMNS)
        writer.writeheader()


def append_lead_row(
    *,
    event_type,
    username="",
    email="",
    full_name="",
    phone="",
    primary_goal="",
    message="",
):
    ensure_leads_file()
    row = {
        "timestamp": timezone.now().isoformat(),
        "event_type": event_type,
        "username": username,
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "primary_goal": primary_goal,
        "message": message,
    }

    with LEADS_FILE.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LEAD_COLUMNS)
        writer.writerow(row)

    _push_to_google_sheets(row)


def _push_to_google_sheets(row):
    webhook_url = getattr(settings, "GOOGLE_SHEETS_WEBHOOK_URL", "")
    if not webhook_url:
        return

    payload = json.dumps(row).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        timeout_seconds = getattr(settings, "GOOGLE_SHEETS_TIMEOUT_SECONDS", 5)
        with request.urlopen(req, timeout=timeout_seconds) as response:
            if response.status >= 400:
                logger.warning("Google Sheets webhook failed with status %s", response.status)
    except error.URLError as exc:
        logger.warning("Google Sheets webhook request failed: %s", exc)
