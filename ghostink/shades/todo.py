import json
from rich import pretty
from rich.text import Text
from .base import BaseEntry
from itertools import chain
from rich.console import Console
from typing import List
from pydantic import BaseModel, Field, ValidationError

pretty.install()
console = Console()


class TodoSubtask(BaseModel):
    title: str
    status: str = Field(..., pattern="^(Pending|Completed)$")


class TodoItemModel(BaseModel):
    title: str
    description: str
    priority: str = Field(..., pattern="^(High|Medium|Low)$")
    status: str = Field(..., pattern="^(Pending|Completed)$")
    tags: List[str] | str | None = None
    subtasks: List[TodoSubtask] | None = None


class Todo(BaseEntry):
    def __init__(self, ghost_ink) -> None:
        self.TODO = ghost_ink.shade.TODO
        self.TITLE_COLOR = self.ColorMapper.get_color("title")
        self.RESET = self.ColorMapper.RESET
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        shade = self.TODO
        # Validate entry_obj with pydantic
        try:
            validated_items = [TodoItemModel(**item) for item in entry_obj]
        except ValidationError as e:
            error_details = json.loads(e.json())
            error_output = Text("")
            for err in error_details:
                error_output.append(f"{err.get('loc')[0]}: {err.get('msg')}\n")
            raise ValueError(f"{error_output}")

        for item in entry_obj:
            entry = Text("")
            priority = item["priority"]
            status = item["status"]
            priority_color = self.ColorMapper.get_color(priority)
            status_color = self.ColorMapper.get_color(status)
            entry.append(
                f"{self.TITLE_COLOR}{item['title']}{self.RESET} ({status_color}{status[0]}{self.RESET}/{priority_color}{priority[0]}{self.RESET})\n"
            )
            entry.append(f"{item['description']}\n")

            if isinstance(item["tags"], str):
                tags_list = [item["tags"]]
            else:
                tags_list = item["tags"]

            if "tags" in item:
                formatted_tags = self._format_tags(tags_list)
            else:
                formatted_tags = ""

            if "subtasks" in item:
                entry.append(f"- {self.TITLE_COLOR}Subtasks:{self.RESET}\n")
                for subtask in item["subtasks"]:
                    sub_title = subtask["title"]
                    sub_status = subtask["status"]
                    sub_color = self.ColorMapper.get_color(sub_status)
                    entry.append(f"  - {sub_color}{sub_title}{self.RESET}\n")
            relative_path, line_no, func_name = self.ghost_ink._get_relative_path()

            formatted_entry = (
                shade,
                str(entry),
                relative_path,
                line_no,
                func_name,
                formatted_tags,
            )

            if formatted_entry not in self.ghost_ink.entries:
                self.ghost_ink.entries.add(formatted_entry)
