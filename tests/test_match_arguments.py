from main import KeywordQueryEventListener


def test_found_match_one_item():
    project = "some project"
    search_arg = ["some"]

    result = KeywordQueryEventListener.found_match(project, search_arg)

    assert result is True
