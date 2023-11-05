async def test_get_user_avatars(
    self,
    service_test_client,
    create_user,
    user_db_factory,
    create_avatar,
    avatar_db_factory,
):
    user = await create_user()
    await user_db_factory(user=user)
    avatar_1 = await create_avatar(
        user=user,
        image=AvatarImage(
            small_url="https://test1.com",
            large_url="https://test2.com",
        ),
    )
    await avatar_db_factory(avatar=avatar_1)
    avatar_2 = await create_avatar(
        user=user,
        image=AvatarImage(
            small_url="https://test1.com",
            large_url="https://test2.com",
        ),
    )
    await avatar_db_factory(avatar=avatar_2)
    status, data = await service_test_client.get_user_avatars_handler(
        user_id=1,
    )
    print("status:", status)
    print("data:", data)
    assert data == {
        'data': {
            'items': [
                {'created_at': data['data']['items'][0]['created_at'],
                    'id': 2,
                    'large_url': 'https://test2.com',
                    'small_url': 'https://test1.com',
                    'user_id': 1},
                {'created_at': data['data']['items'][1]['created_at'],
                    'id': 1,
                    'large_url': 'https://test2.com',
                    'small_url': 'https://test1.com',
                    'user_id': 1}
            ],
            'limit': 100,
            'offset': 0,
            'total': None,
        }
    }
    assert status == 200

    #...
    @classmethod
    async def get_user_avatars_handler(
            cls,
            user_id: int,
    ):
        print("user_id", user_id)
        print(f"/users/{user_id}/avatars")
        return await cls.request(path=f"/users/{user_id}/avatars", method="get")
    
    #...
    @classmethod
    async def request(
            cls,
            path: str,
            method: str,
            json=None,
            headers=None,
            data=None,
            files=None,
            params=None,
            cookies=None,
            prefix: str = "v1",
    ):
        host = "localhost"
        port = int(os.environ.get("GATEWAY_PORT"))
        print("method:", method)
        print("params:", params)
        print("url:", path)
        print("json:", json)
        print("files:", files)
        print("data:", data)
        print("headers:", headers)
        print("cookies:", cookies)

        async with AsyncClient(base_url=f"http://{host}:{port}/{prefix}") as client:
            resp = await client.request(
                method=method,
                params=params,
                url=path,
                json=json,
                files=files,
                data=data,
                headers=headers,
                cookies=cookies,
                timeout=10,
            )
            status = resp.status_code
            data = resp.json() if resp.text else None
        return status, data
