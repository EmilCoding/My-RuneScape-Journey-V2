"""Local web application for browsing and updating RuneScape goals."""

from __future__ import annotations

import pathlib
import re
import urllib.parse
from typing import Any

from flask import Flask, abort, jsonify, render_template, request

from rshisttools.paths import ROOT
from rshisttools.walk import get_updates_from_folder


UPDATE_STATUSES = {
    "completed goals": "completed",
    "partially completed": "partial",
    "future goals": "future",
}
GOAL_LINE_PATTERN = re.compile(
    r"^(?P<indent>\s*)-\s+\[(?P<state>[ xX])\]\s+(?P<description>.*)$"
)
HEADING_PATTERN = re.compile(r"^###\s+(.+?)\s*$")
OPTIONAL_PREFIX = "(!Optional) "
BACKLOG_MARKER_PATTERN = re.compile(
    r"^<!-- rshisttools-web-backlog:(?P<path>.+):(?P<line>\d+) -->$"
)
BACKLOG_HEADING = "## Added from the update timeline"


def _backlog_keys(backlog_path: pathlib.Path) -> set[str]:
    """Return goal identifiers recorded by this app in the backlog file."""
    if not backlog_path.exists():
        return set()

    keys: set[str] = set()
    for line in backlog_path.read_text(encoding="utf-8").splitlines():
        match = BACKLOG_MARKER_PATTERN.match(line)
        if match:
            keys.add(f"{match['path']}:{match['line']}")
    return keys


def _read_update_text(update_path: pathlib.Path) -> tuple[str, str]:
    """Read modern UTF-8 notes and legacy Windows-1252 update files."""
    raw_contents = update_path.read_bytes()
    try:
        return raw_contents.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw_contents.decode("cp1252"), "cp1252"


def _read_goals(
    update_path: pathlib.Path,
    relative_path: str,
    backlog_keys: set[str],
) -> list[dict[str, Any]]:
    goals: list[dict[str, Any]] = []
    section = ""
    contents, _ = _read_update_text(update_path)
    for line_number, line in enumerate(
        contents.splitlines(), start=1
    ):
        heading = HEADING_PATTERN.match(line)
        if heading:
            section = heading.group(1)

        match = GOAL_LINE_PATTERN.match(line)
        if match is None:
            continue

        description = match["description"]
        optional = description.startswith(OPTIONAL_PREFIX)
        if optional:
            description = description[len(OPTIONAL_PREFIX):]

        goal_id = f"{relative_path}:{line_number}"
        goals.append({
            "id": goal_id,
            "line": line_number,
            "text": description,
            "section": section,
            "completed": match["state"].lower() == "x",
            "optional": optional,
            "backlogged": goal_id in backlog_keys,
        })
    return goals


def _get_update_status(folder_status: str, goals: list[dict[str, Any]]) -> str:
    """Treat updates with every required goal checked as completed."""
    required_goals = [goal for goal in goals if not goal["optional"]]
    if folder_status == "completed" or (
        required_goals and all(goal["completed"] for goal in required_goals)
    ):
        return "completed"
    return folder_status


def _read_updates(root: pathlib.Path) -> list[dict[str, Any]]:
    backlog_keys = _backlog_keys(root / "backlog.md")
    updates: list[dict[str, Any]] = []

    for folder_name, status in UPDATE_STATUSES.items():
        folder = root / folder_name
        for update in get_updates_from_folder(folder):
            relative_path = update.path.relative_to(root).as_posix()
            goals = _read_goals(update.path, relative_path, backlog_keys)
            update_status = _get_update_status(status, goals)
            updates.append({
                "id": relative_path,
                "name": update.name,
                "date": update.date.isoformat(),
                "display_date": update.date.strftime("%d %b %Y").lstrip("0"),
                "status": update_status,
                "goals": goals,
            })

    updates.sort(key=lambda item: (item["date"], item["name"]))
    return updates


def _goal_target(root: pathlib.Path, relative_path: str) -> pathlib.Path:
    """Resolve an update path only if it belongs to one of the three data folders."""
    candidate_relative = pathlib.PurePosixPath(relative_path)
    if candidate_relative.is_absolute() or ".." in candidate_relative.parts:
        abort(400, description="Invalid update path.")

    candidate = (root / pathlib.Path(*candidate_relative.parts)).resolve()
    allowed_folders = [
        (root / folder_name).resolve() for folder_name in UPDATE_STATUSES
    ]
    if not any(candidate.is_relative_to(folder) for folder in allowed_folders):
        abort(400, description="Update is outside the supported folders.")
    if candidate.suffix.lower() != ".md" or not candidate.is_file():
        abort(404, description="Update file not found.")
    return candidate


def _remove_backlog_entry(backlog_path: pathlib.Path, goal_id: str) -> None:
    if not backlog_path.exists():
        return

    lines = backlog_path.read_text(encoding="utf-8").splitlines()
    marker = f"<!-- rshisttools-web-backlog:{goal_id} -->"
    filtered: list[str] = []
    skip_entry = False
    for line in lines:
        if line == marker:
            skip_entry = True
            continue
        if skip_entry:
            skip_entry = False
            continue
        filtered.append(line)
    backlog_path.write_text("\n".join(filtered).rstrip() + "\n", encoding="utf-8")


def _add_backlog_entry(
    backlog_path: pathlib.Path,
    goal_id: str,
    goal_text: str,
    update_name: str,
    relative_path: str,
) -> None:
    contents = backlog_path.read_text(encoding="utf-8")
    if f"<!-- rshisttools-web-backlog:{goal_id} -->" in contents:
        return

    if BACKLOG_HEADING not in contents:
        contents = contents.rstrip() + f"\n\n{BACKLOG_HEADING}\n"
    encoded_path = urllib.parse.quote(relative_path, safe="/")
    entry = (
        f"<!-- rshisttools-web-backlog:{goal_id} -->\n"
        f"- {goal_text} - [{update_name}](./{encoded_path})"
    )
    backlog_path.write_text(contents.rstrip() + f"\n\n{entry}\n", encoding="utf-8")


def create_app(repository_root: pathlib.Path = ROOT) -> Flask:
    """Create the timeline web application."""
    app = Flask(__name__)
    root = repository_root.resolve()

    @app.get("/")
    def index() -> str:
        return render_template("timeline.html")

    @app.get("/api/updates")
    def updates() -> Any:
        return jsonify({"updates": _read_updates(root)})

    @app.post("/api/goals/<action>")
    def update_goal(action: str) -> Any:
        if action not in {"completed", "backlog"}:
            abort(404)

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            abort(400, description="Expected a JSON request body.")
        relative_path = payload.get("update")
        goal_line = payload.get("line")
        expected_text = payload.get("text")
        if (
            not isinstance(relative_path, str)
            or not isinstance(goal_line, int)
            or isinstance(goal_line, bool)
            or goal_line < 1
            or not isinstance(expected_text, str)
        ):
            abort(400, description="Update, goal line, and goal text are required.")

        update_path = _goal_target(root, relative_path)
        contents, encoding = _read_update_text(update_path)
        file_lines = contents.splitlines()
        if goal_line > len(file_lines):
            abort(409, description="Goal changed; reload the timeline and try again.")

        match = GOAL_LINE_PATTERN.match(file_lines[goal_line - 1])
        if match is None:
            abort(409, description="Goal changed; reload the timeline and try again.")

        description = match["description"]
        if description.startswith(OPTIONAL_PREFIX):
            description = description[len(OPTIONAL_PREFIX):]
        if description != expected_text:
            abort(409, description="Goal changed; reload the timeline and try again.")

        relative_path = pathlib.PurePosixPath(relative_path).as_posix()
        goal_id = f"{relative_path}:{goal_line}"
        backlog_path = root / "backlog.md"
        if action == "backlog":
            if match["state"].lower() == "x":
                abort(409, description="A completed goal cannot be backlogged.")
            _add_backlog_entry(
                backlog_path,
                goal_id,
                expected_text,
                re.sub(
                    r"^\d{4}\.\d{2}\.\d{2} - (?:Update )?",
                    "",
                    update_path.stem,
                ),
                relative_path,
            )
        else:
            file_lines[goal_line - 1] = (
                f"{match['indent']}- [x] {match['description']}"
            )
            update_path.write_text(
                "\n".join(file_lines) + "\n",
                encoding=encoding,
            )
            _remove_backlog_entry(backlog_path, goal_id)

        return jsonify({"updates": _read_updates(root)})

    return app


def main() -> None:
    """Run the local development server."""
    create_app().run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()
