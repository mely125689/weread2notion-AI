from test_sync import Notion
from weread2notion.sync import Synchronizer


def test_multiple_notes_link_daily_relations_once():
    notion = Notion()
    Synchronizer(None, notion).sync_periods(
        [{"timestamp": 1691251200, "duration": 600},
         {"timestamp": 1691337600, "duration": 300}],
        [1691251201, 1691251202, 1691337601],
    )
    relation_updates = [
        args for args, _ in notion.requests
        if args[1] == "PATCH" and "年" in args[2]["properties"]
    ]
    assert len(relation_updates) == 2
    day_seconds = [raw["时长"] for database, raw in notion.rows if database == "日"]
    assert sorted(day_seconds) == [300, 600]
