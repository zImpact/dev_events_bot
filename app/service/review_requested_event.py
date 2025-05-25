from app.config import JIRA_BASE_URL, JIRA_REVIEWER_FIELD_IDS, REPO_NAMES
from app.models import JiraColumn
from app.repository.jira import JiraRepository
from app.repository.telegram import TelegramRepository
from app.utils import github_to_jira, github_to_tg


def process_review_requested_event(data):
    if data.get("action") == "review_requested":
        repo = data["repository"]["name"]
        pull_request = data["pull_request"]
        assignee = data["sender"]["login"]

        reviewers = pull_request["requested_reviewers"]
        reviewers_mentions = ", ".join(
            f"[{r['login']}](tg://user?id={github_to_tg(r['login'])})"
            for r in reviewers
        )

        assignee_mention = f"tg://user?id={github_to_tg(assignee)}"

        if len(reviewers) == 1:
            reviewers_label = "Ревьювер:"
            title_label = "Назначен ревьювер"

        else:
            reviewers_label = "Ревьюверы:"
            title_label = "Назначены ревьюверы"

        project_name = REPO_NAMES.get(repo, repo)
        repo_part = f"{project_name}" if project_name != repo else f"{repo}"

        telegram_repo = TelegramRepository()
        jira_repo = JiraRepository()

        pr_branch = pull_request["head"]["ref"]
        jira_url = f"{JIRA_BASE_URL}/browse/{pr_branch}"

        task_title = jira_repo.get_issue_title(pr_branch)
        if task_title is None:
            task_part = "Pull Request-a"
            include_jira_link = False
        else:
            task_part = f"для задачи *«{task_title}»*"
            include_jira_link = True

            jira_repo.move_issue_to_status(
                pr_branch, JiraColumn.IN_REVIEW.value
            )

            jira_reviewers_ids = [
                github_to_jira(r["login"]) for r in reviewers
            ]
            jira_repo.assign_reviewers(
                pr_branch, JIRA_REVIEWER_FIELD_IDS[repo], jira_reviewers_ids
            )

        lines = [
            f"👀 {title_label} {task_part} в проекте *{repo_part}*!",
            f"👤 *Исполнитель:* [{assignee}]({assignee_mention})",
            f"🔍 *{reviewers_label}* {reviewers_mentions}",
        ]

        if include_jira_link:
            lines.append(f"💻 [Jira]({jira_url})")

        lines.append(f"🔗 [Pull Request]({pull_request['html_url']})")

        text = "\n".join(lines)
        telegram_repo.send_message(text)
        return "Review request event processed", 200

    return "Ignored", 200
