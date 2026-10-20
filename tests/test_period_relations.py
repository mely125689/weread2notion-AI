"""Regression check: multiple notes on one day need one relation update."""
from test_sync import Notion
from weread2notion.sync import Synchronizer


def test_daily_relations_written_once_per_day_and_durations_preserved():
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


def test_review_preserves_source_and_personal_labels():
    blocks = Synchronizer.book_content_blocks({
        "reviews": [{"abstract": "作者的句子", "content": "我自己的想法"}],
    })
    text = "".join(x["text"]["content"] for x in blocks[-1]["callout"]["rich_text"])
    assert text == "引用原文：\n作者的句子\n\n我的批注：\n我自己的想法"


def test_long_callout_preserves_complete_text():
    from weread2notion.blocks import get_callout
    original = "阅读记录" * 1100
    parts = get_callout(original, "💭")["callout"]["rich_text"]
    assert "".join(x["text"]["content"] for x in parts) == original
    assert all(len(x["text"]["content"]) <= 2000 for x in parts)
