from pathlib import Path

from rshisttools.web import create_app


def make_repository(root: Path) -> None:
    (root / "completed goals" / "RuneScape 2" / "2006").mkdir(parents=True)
    (root / "partially completed" / "RuneScape 2" / "2006").mkdir(parents=True)
    (root / "future goals" / "2009").mkdir(parents=True)
    (root / "backlog.md").write_text("# Back log\n", encoding="utf-8")
    (root / "completed goals" / "RuneScape 2" / "2006" / "2006.04.24 - Update Example.md").write_text(
        "# Update:Example - 24 April 2006\n\n## Goals\n\n- [ ] Finish a task\n- [x] Already done\n",
        encoding="utf-8",
    )
    (root / "partially completed" / "RuneScape 2" / "2006" / "2006.06.06 - Update In progress.md").write_text(
        "# Update:In progress - 6 June 2006\n\n## Goals\n\n### Skills\n\n- [ ] (!Optional) Train a skill\n",
        encoding="utf-8",
    )
    (root / "future goals" / "2009" / "2009.08.18 - Update Future.md").write_text(
        "# Update:Future - 18 August 2009\n\n## Goals\n\n- [ ] New goal\n",
        encoding="utf-8",
    )


def test_update_api_lists_status_and_goals(tmp_path: Path) -> None:
    make_repository(tmp_path)
    client = create_app(tmp_path).test_client()

    response = client.get("/api/updates")

    assert response.status_code == 200
    assert response.json is not None
    updates = response.json["updates"]
    assert [update["status"] for update in updates] == ["completed", "partial", "future"]
    optional_goal = updates[1]["goals"][0]
    assert optional_goal["text"] == "Train a skill"
    assert optional_goal["section"] == "Skills"
    assert optional_goal["optional"] is True


def test_update_is_completed_when_all_required_goals_are_done(tmp_path: Path) -> None:
    make_repository(tmp_path)
    update_path = (
        tmp_path / "partially completed" / "RuneScape 2" / "2006"
        / "2006.06.07 - Update Optional reward.md"
    )
    update_path.write_text(
        "# Update:Optional reward - 7 June 2006\n\n"
        "## Goals\n\n"
        "- [x] Complete the required quest\n"
        "- [ ] (!Optional) Collect an optional reward\n",
        encoding="utf-8",
    )
    client = create_app(tmp_path).test_client()

    response = client.get("/api/updates")

    assert response.status_code == 200
    assert response.json is not None
    update = next(
        item for item in response.json["updates"]
        if item["name"] == "Optional reward"
    )
    assert update["status"] == "completed"
    assert update["goals"][1]["optional"] is True
    assert update["goals"][1]["completed"] is False


def test_optional_only_update_keeps_its_folder_status(tmp_path: Path) -> None:
    make_repository(tmp_path)

    response = create_app(tmp_path).test_client().get("/api/updates")

    assert response.status_code == 200
    assert response.json is not None
    update = next(
        item for item in response.json["updates"]
        if item["name"] == "In progress"
    )
    assert update["status"] == "partial"


def test_timeline_page_includes_optional_goal_toggle(tmp_path: Path) -> None:
    make_repository(tmp_path)

    response = create_app(tmp_path).test_client().get("/")

    assert response.status_code == 200
    assert b'id="show-optional" type="checkbox" checked' in response.data
    assert b"Show optional goals" in response.data


def test_completed_action_updates_markdown_and_unbacklogs_goal(tmp_path: Path) -> None:
    make_repository(tmp_path)
    update_path = (
        tmp_path / "partially completed" / "RuneScape 2" / "2006"
        / "2006.06.06 - Update In progress.md"
    )
    client = create_app(tmp_path).test_client()
    backlog_response = client.post("/api/goals/backlog", json={
        "update": "partially completed/RuneScape 2/2006/2006.06.06 - Update In progress.md",
        "line": 7,
        "text": "Train a skill",
    })
    assert backlog_response.status_code == 200
    assert "Train a skill" in (tmp_path / "backlog.md").read_text(encoding="utf-8")

    complete_response = client.post("/api/goals/completed", json={
        "update": "partially completed/RuneScape 2/2006/2006.06.06 - Update In progress.md",
        "line": 7,
        "text": "Train a skill",
    })

    assert complete_response.status_code == 200
    assert "- [x] (!Optional) Train a skill" in update_path.read_text(encoding="utf-8")
    assert "rshisttools-web-backlog" not in (tmp_path / "backlog.md").read_text(encoding="utf-8")


def test_goal_action_rejects_paths_outside_update_folders(tmp_path: Path) -> None:
    make_repository(tmp_path)
    client = create_app(tmp_path).test_client()

    response = client.post("/api/goals/completed", json={
        "update": "../backlog.md",
        "line": 1,
        "text": "anything",
    })

    assert response.status_code == 400


def test_goal_action_preserves_legacy_cp1252_encoding(tmp_path: Path) -> None:
    make_repository(tmp_path)
    relative_path = "future goals/2009/2009.08.19 - Update Legacy.md"
    update_path = tmp_path / relative_path
    update_path.write_bytes(
        "# Update:Legacy - 19 August 2009\n\n## Goals\n\n- [ ] Find Hati’s reward\n".encode("cp1252")
    )
    client = create_app(tmp_path).test_client()

    response = client.post("/api/goals/completed", json={
        "update": relative_path,
        "line": 5,
        "text": "Find Hati’s reward",
    })

    assert response.status_code == 200
    assert "- [x] Find Hati’s reward" in update_path.read_bytes().decode("cp1252")
