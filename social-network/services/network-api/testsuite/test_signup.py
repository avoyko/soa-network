# /// [Functional test]
async def test_happy_path(service_client, mockserver):
    @mockserver.handler("http://network-users.net/v1/signup")
    def _mock(request):
        return mockserver.make_response()

    response = await service_client.post(
        "/users/signup",
        json={
            "username": "Ivanov",
            "name": "Ivan",
        },
    )
    assert response.status == 200