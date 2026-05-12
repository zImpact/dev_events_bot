from typing import Any

from app.config import MAIN_BRANCH


def process_pull_request_merged_event(data: Any) -> tuple[str, int]:
    if data.get("action") == "closed" and data.get("pull_request", {}).get(
        "merged"
    ):
        target_branch = data["pull_request"]["base"]["ref"]

        if target_branch != MAIN_BRANCH:
            return f"Ignored: merged into {target_branch}", 200

        return "Pull request merged event processed", 200

    return "Ignored", 200
