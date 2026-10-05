from unittest.mock import Mock, patch

import pytest

from pyproresult import ProresultException, WebClient

DOCUMENTS_HTML = """
<ul>
  <li class="mdl-list__item">
    <span class="document-name"> report.pdf </span>
    <div data-document-id="17"></div>
    <span class="document-updated">2026-01-02</span>
  </li>
  <li class="mdl-list__item">
    <span class="document-name">no-id.pdf</span>
  </li>
</ul>
"""


def make_client(session: Mock) -> WebClient:
    with patch("pyproresult.web_client.requests.Session", return_value=session):
        return WebClient("user", "pass", "db")


def test_login_posts_credentials():
    session = Mock()
    session.post.return_value = Mock(status_code=200, text="ok")

    make_client(session)

    session.post.assert_called_once_with(
        "https://proresult.app/adm/userlogin.php",
        data={"brnamn": "user", "pass": "pass", "dbnamn": "db"},
    )


def test_login_failure_raises():
    session = Mock()
    session.post.return_value = Mock(status_code=403, text="denied")

    with pytest.raises(ProresultException):
        make_client(session)


def test_get_documents_parses_list():
    session = Mock()
    session.post.return_value = Mock(status_code=200, text="ok")
    session.get.return_value = Mock(status_code=200, text=DOCUMENTS_HTML)
    client = make_client(session)

    docs = client.get_documents(5)

    assert docs == [
        {"FileName": "report.pdf", "Id": "17", "UploadedDate": "2026-01-02"}
    ]
