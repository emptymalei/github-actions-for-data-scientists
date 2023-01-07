from ufo_data.utils import BASE_URL, get_raw_html


def test_get_raw_html(requests_mock):

    mocked_content = b"This is a test"
    requests_mock.get(BASE_URL, content=mocked_content)
    content = get_raw_html(BASE_URL)

    assert content == mocked_content
