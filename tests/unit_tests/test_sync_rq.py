import responses

from sample_requests.sync_req import get_and_parse_user


@responses.activate
def test_get_and_parse_user_works_properly() -> None:
    base_url = "http://someurl.com"
    user_id = 0
    endpoint_prefix = "/user/"

    responses.add(
        responses.GET,
        f"{base_url}{endpoint_prefix}{user_id}",
        json={"user": user_id},
        status=200,
        headers={},
    )

    response = get_and_parse_user(base_url, endpoint_prefix, user_id)

    assert type(response) is dict
    assert response["user"] == user_id
