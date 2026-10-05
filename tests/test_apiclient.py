from unittest.mock import Mock, patch

import pytest

from pyproresult import ApiClient, CsvDataError, ProresultException


def make_response(body: str, status_code: int = 200) -> Mock:
    return Mock(status_code=status_code, content=body.encode("utf-8"), text=body)


@pytest.fixture
def client():
    return ApiClient(account_id="acc", api_secret="secret")


@patch("pyproresult.api_client.requests.get")
def test_get_csv_data_parses_rows(mock_get, client):
    mock_get.return_value = make_response("id;navn\n1;Ærlig\n2;Bø\n")

    rows = client.get_csv_data("kundeCSV")

    assert rows == [{"id": "1", "navn": "Ærlig"}, {"id": "2", "navn": "Bø"}]
    url = mock_get.call_args.args[0]
    assert url.endswith("?fn=kundeCSV")
    assert mock_get.call_args.kwargs["headers"] == {
        "X-Account-ID": "acc",
        "X-API-Secret": "secret",
    }


@patch("pyproresult.api_client.requests.get")
def test_get_projects_include_inactive(mock_get, client):
    mock_get.return_value = make_response("id\n1\n")

    client.get_projects(include_inactive=True)

    assert mock_get.call_args.args[0].endswith("?fn=prosjektCSV&taMedAvslutta=1")


@patch("pyproresult.api_client.requests.get")
def test_get_csv_data_bad_status(mock_get, client):
    mock_get.return_value = make_response("boom", status_code=500)

    with pytest.raises(CsvDataError):
        client.get_csv_data("kundeCSV")


@patch("pyproresult.api_client.requests.get")
def test_get_csv_data_no_access(mock_get, client):
    mock_get.return_value = make_response("TMCAPI - ingen tilgang")

    with pytest.raises(ProresultException):
        client.get_csv_data("kundeCSV")


@patch("pyproresult.api_client.requests.get")
def test_get_images_skips_duplicates(mock_get, client):
    mock_get.return_value = make_response(
        "<Bilder>"
        "<Bilde><Url>https://x/a</Url><Filnavn>a.jpg</Filnavn></Bilde>"
        "<Bilde><Url>https://x/b</Url><Filnavn>a.jpg</Filnavn></Bilde>"
        "<Bilde><Url>https://x/c</Url><Filnavn>c.jpg</Filnavn></Bilde>"
        "</Bilder>"
    )

    images = client.get_images(42)

    assert images == {"a.jpg": "https://x/a", "c.jpg": "https://x/c"}
    assert "hse_deviationId=42" in mock_get.call_args.args[0]
