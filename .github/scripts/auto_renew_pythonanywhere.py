# mypy: ignore-errors
import logging
import os
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)

USERNAME = os.environ.get("PA_USERNAME")
PASSWORD = os.environ.get("PA_PASSWORD")

LOGIN_URL = "https://www.pythonanywhere.com/login/"
DASHBOARD_URL = f"https://www.pythonanywhere.com/user/{USERNAME}/webapps/"


def renew() -> bool:
    if not USERNAME or not PASSWORD:
        LOGGER.error("PA_USERNAME and PA_PASSWORD must be set")
        return False

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            )
        }
    )

    try:
        LOGGER.info("Logging in as %s...", USERNAME)
        login_page = session.get(LOGIN_URL, timeout=10)
        login_page.raise_for_status()

        soup = BeautifulSoup(login_page.content, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})

        if not csrf_token:
            LOGGER.error("Could not find CSRF token on login page")
            return False

        payload = {
            "csrfmiddlewaretoken": csrf_token["value"],
            "auth-username": USERNAME,
            "auth-password": PASSWORD,
            "login_view-current_step": "auth",
        }

        response = session.post(
            LOGIN_URL,
            data=payload,
            headers={"Referer": LOGIN_URL},
            timeout=10,
            allow_redirects=True,
        )
        response.raise_for_status()

        if (
            "Log out" not in response.text
            and "logout" not in response.text.lower()
        ):
            LOGGER.error("Login failed - 'Log out' not found in response")
            LOGGER.error("Response URL: %s", response.url)
            return False

        if "login" in response.url.lower():
            LOGGER.error("Login failed - still on login page")
            return False

        time.sleep(1)

        dashboard = session.get(DASHBOARD_URL, timeout=10)
        dashboard.raise_for_status()
        soup = BeautifulSoup(dashboard.content, "html.parser")

        extend_action = None
        for form in soup.find_all("form", action=True):
            action = form.get("action", "")
            if "/extend" in action.lower():
                extend_action = action
                break

        if not extend_action:
            return True

        dashboard_csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if not dashboard_csrf:
            LOGGER.error("Could not find CSRF token on dashboard")
            return False

        extend_url = urljoin("https://www.pythonanywhere.com", extend_action)

        result = session.post(
            extend_url,
            data={"csrfmiddlewaretoken": dashboard_csrf["value"]},
            headers={"Referer": DASHBOARD_URL},
            timeout=10,
        )
        result.raise_for_status()

        if result.status_code != 200:
            LOGGER.error(
                "Extension failed with status: %s", result.status_code
            )
            return False

        if "webapps" in result.url.lower():
            return True

        LOGGER.warning("Unexpected redirect to: %s", result.url)
        return False
    except requests.Timeout:
        LOGGER.exception("Request timed out")
        return False
    except requests.RequestException:
        LOGGER.exception("Network error")
        return False
    except Exception:
        LOGGER.exception("Unexpected error")
        return False


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )
    return renew()


if __name__ == "__main__":
    sys.exit(main())
