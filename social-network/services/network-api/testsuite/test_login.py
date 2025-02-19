# /// [Functional test]
async def test_happy_path(service_client, mockserver):
    @mockserver.handler("http://network-users.net/v1/login")
    def _mock(request):
        return mockserver.make_response()

    response = await service_client.post(
        "/users/login",
        json={
            "username": "Ivanov",
            "name": "Ivan",
            "email": "some@email.com",
        },
    )
    assert response.status == 200