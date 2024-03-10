import pytest
from aioresponses import aioresponses

from sample_requests.async_req import sample_asyn_get_request


@pytest.mark.asyncio
async def test_sample_async_request_works_properly() -> None:
    base_url = ""
    endpoint_prefix = ""
    user_id = 1

    with aioresponses() as m:
        m.get(
            f"{base_url}{endpoint_prefix}{user_id}",
            status=200,
            headers={},
            payload={"user": user_id},
        )
        status_code, json_response = await sample_asyn_get_request(
            base_url, endpoint_prefix, user_id
        )

    assert status_code == 200
    assert json_response["user"] == user_id
