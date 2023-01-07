import pytest
from ufo_data.utils import (
    BASE_URL,
    TABLE_PAGE_BASE_URL,
    extract_links,
    extract_table,
    get_raw_html,
)


@pytest.mark.skip(reason="only used to generate test artefacts")
def test_regenerate_get_raw_html(artefact_base_path):

    content = get_raw_html(BASE_URL)

    with open(artefact_base_path / "raw_html.binary", "wb") as fp:
        fp.write(bytearray(content))

    with open(artefact_base_path / "raw_html.binary", "rb") as fp:
        content_reloaded = fp.read()

    assert content == content_reloaded


@pytest.mark.skip(reason="only used to generate test artefacts")
def test_regenerate_get_raw_html_of_table(artefact_base_path):

    content = get_raw_html("https://www.nuforc.org/webreports/ndxe.html")

    with open(artefact_base_path / "raw_html_ndxe.binary", "wb") as fp:
        fp.write(bytearray(content))

    with open(artefact_base_path / "raw_html_ndxe.binary", "rb") as fp:
        content_reloaded = fp.read()

    assert content == content_reloaded


@pytest.mark.parametrize(
    "artefact_file, top, expected, artefact_base_path",
    [
        (
            "raw_html.binary",
            None,
            {"len": 973, "first": f"{TABLE_PAGE_BASE_URL}/ndxe202212.html"},
            "artefact_base_path",
        ),
        ("raw_html.binary", 10, {"len": 10, "first": f"{TABLE_PAGE_BASE_URL}/ndxe202212.html"}, "artefact_base_path"),
    ],
    ids=["top_unset", "top_10"],
    indirect=["artefact_base_path"],
)
def test_extract_links(artefact_file, top, expected, artefact_base_path):
    with open(artefact_base_path / artefact_file, "rb") as fp:
        content = fp.read()

    links = extract_links(content, top)

    assert len(links) == expected["len"]
    assert links[0] == expected["first"]


@pytest.mark.parametrize(
    "artefact_file, expected, artefact_base_path",
    [("raw_html_ndxe.binary", {"len": 1, "first_shape": (376, 9)}, "artefact_base_path")],
    ids=[
        "raw_html_ndxe",
    ],
    indirect=["artefact_base_path"],
)
def test_extract_table(artefact_file, expected, artefact_base_path):
    with open(artefact_base_path / artefact_file, "rb") as fp:
        content = fp.read()

    dfs = extract_table(content)

    assert len(dfs) == expected["len"]
    assert dfs[0].shape == expected["first_shape"]
