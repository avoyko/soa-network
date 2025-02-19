async def test_happy_path(service_client, mockserver):
    @mockserver.handler("http://network-users.net/v1/profile-info")
    def _mock(request):
        return mockserver.make_response(
            json={
                "profile_id": "a8098c1a-f86e-11da-bd1a-00112444be1e",
                "username": "Ivanov",
                "name": "Ivan",
                "email": "some@email.com",
                "birthdate": "01.01.2000",
                "phone": "7-999-9999-99-99",
                "bio": "some bio",
            }
        )

    response = await service_client.post(
        "/users/profile-info",
        json={"profile_id": "a8098c1a-f86e-11da-bd1a-00112444be1e"},
    )
    assert response.status == 200
    assert response.json() == {
        "profile_id": "a8098c1a-f86e-11da-bd1a-00112444be1e",
        "username": "Ivanov",
        "name": "Ivan",
        "email": "some@email.com",
        "birthdate": "01.01.2000",
        "phone": "7-999-9999-99-99",
        "bio": "some bio",
    }