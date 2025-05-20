from enum import Enum


class JiraColumn(Enum):
    IN_PROGRESS = "В работе"
    PAUSED = "В паузе"
    IN_REVIEW = "В ревью"
    DONE = "Готово"
