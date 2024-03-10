import asyncio

import aiohttp

sample_data_to_send = {
    "username": "Alexander",
    "liked_posts": [6, 7, 0],
    "short_description": "Very short desc",
    "long_bio": "Amazing",
}


async def sample_asyn_get_request(base_url: str, endpoint_prefix: str, user_id: int) -> (int, dict):  # type: ignore
    url = f"{base_url}{endpoint_prefix}{user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_response = await response.json()
            status_code = response.status
            return status_code, json_response


# asyncio.run(sample_asyn_post_request())
