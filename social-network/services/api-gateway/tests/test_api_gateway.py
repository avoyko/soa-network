import grpc
import pytest
import httpx
import json
import time
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_register_user(api_client):
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com",
    }

    response = await api_client.post("/users/register", json=test_user)

    assert response.status_code == 201
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]

    return test_user


@pytest.mark.asyncio
async def test_login_success(api_client):
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com",
    }

    response = await api_client.post("/users/register", json=test_user)

    login_data = {"login": test_user["login"], "password": test_user["password"]}

    response = await api_client.post("/users/login", json=login_data)

    assert response.status_code == 200
    data = response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(api_client):
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com",
    }

    response = await api_client.post("/users/register", json=test_user)

    login_data = {"login": test_user["login"], "password": "wrong_password"}

    response = await api_client.post("/users/login", json=login_data)

    assert response.status_code == 401
    data = response.json()
    assert "Неверный логин или пароль" in data["detail"]


@pytest.mark.asyncio
async def test_get_profile(api_client):
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com",
    }

    response = await api_client.post("/users/register", json=test_user)

    response = await api_client.get(f"/users/profile/{test_user['login']}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_profile(api_client):
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com",
    }

    response = await api_client.post("/users/register", json=test_user)

    update_data = {
        "first_name": "Test",
        "last_name": "User",
        "birth_date": "1990-01-01",
        "phone": "+1234567890",
        "bio": "Test bio",
    }

    response = await api_client.put(
        f"/users/profile/{test_user['login']}", json=update_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["birth_date"] == update_data["birth_date"]
    assert data["phone"] == update_data["phone"]

    response = await api_client.get(f"/users/profile/{test_user['login']}")
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]


@pytest.mark.asyncio
async def test_nonexistent_profile(api_client):
    response = await api_client.get("/users/profile/nonexistent_user")

    assert response.status_code == 404
    data = response.json()
    assert "Пользователь не найден" in data["detail"]



@pytest.mark.asyncio
async def test_create_post(api_client, patch_grpc_client, mock_grpc_posts_client):

    test_user = await test_register_user(api_client)
    
    post_data = {
        "title": "Test Post Title",
        "description": "This is a test post description",
        "username": test_user["login"],
        "is_private": False,
        "tags": ["test", "api"]
    }
    

    mock_response = MagicMock()
    mock_response.post = MagicMock(
        id=1,
        title=post_data["title"],
        description=post_data["description"],
        username=post_data["username"],
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        is_private=post_data["is_private"],
        tags=post_data["tags"]
    )
    mock_grpc_posts_client.CreatePost.return_value = mock_response

    response = await api_client.post("/posts/", json=post_data)
    

    assert response.status_code == 200
    data = response.json()
    assert "post" in data
    assert data["post"]["title"] == post_data["title"]
    assert data["post"]["description"] == post_data["description"]
    assert data["post"]["username"] == post_data["username"]
    assert data["post"]["is_private"] == post_data["is_private"]
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.CreatePost.assert_called_once()
    
    # Возвращаем данные поста для использования в других тестах
    return data["post"]


@pytest.mark.asyncio
async def test_get_post(api_client, patch_grpc_client, mock_grpc_posts_client):
    # Регистрация пользователя
    test_user = await test_register_user(api_client)
    
    # Создаем фиктивные данные поста
    post_id = 1
    post_data = {
        "id": post_id,
        "title": "Test Post Title",
        "description": "This is a test post description",
        "username": test_user["login"],
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_private": False,
        "tags": ["test", "api"]
    }
    
    # Настраиваем ответ мока для GetPost
    mock_response = MagicMock()
    mock_response.post = MagicMock(**post_data)
    mock_grpc_posts_client.GetPost.return_value = mock_response
    
    # Отправляем запрос на получение поста
    response = await api_client.get(f"/posts/{post_id}")
    
    # Проверка успешного получения поста
    assert response.status_code == 200
    data = response.json()
    assert "post" in data
    assert data["post"]["id"] == post_data["id"]
    assert data["post"]["title"] == post_data["title"]
    assert data["post"]["description"] == post_data["description"]
    assert data["post"]["username"] == post_data["username"]
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.GetPost.assert_called_once()


@pytest.mark.asyncio
async def test_update_post(api_client, patch_grpc_client, mock_grpc_posts_client):
    # Регистрация пользователя
    test_user = await test_register_user(api_client)
    
    # Создаем фиктивные данные поста
    post_id = 1
    original_post = {
        "id": post_id,
        "title": "Original Title",
        "description": "Original Description",
        "username": test_user["login"],
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_private": False,
        "tags": ["test"]
    }
    
    # Данные для обновления поста
    update_data = {
        "username": test_user["login"],
        "title": "Updated Post Title",
        "description": "This is an updated post description",
        "is_private": True,
        "tags": ["updated", "test"]
    }
    
    # Настраиваем ответ мока для UpdatePost
    updated_post = original_post.copy()
    updated_post.update({
        "title": update_data["title"],
        "description": update_data["description"],
        "is_private": update_data["is_private"],
        "tags": update_data["tags"],
        "updated_at": "2023-01-01T01:00:00"
    })
    
    mock_response = MagicMock()
    mock_response.post = MagicMock(**updated_post)
    mock_grpc_posts_client.UpdatePost.return_value = mock_response
    
    # Отправляем запрос на обновление поста
    response = await api_client.put(f"/posts/{post_id}", json=update_data)
    
    # Проверка успешного обновления поста
    assert response.status_code == 200
    data = response.json()
    assert "post" in data
    assert data["post"]["id"] == post_id
    assert data["post"]["title"] == update_data["title"]
    assert data["post"]["description"] == update_data["description"]
    assert data["post"]["is_private"] == update_data["is_private"]
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.UpdatePost.assert_called_once()


@pytest.mark.asyncio
async def test_delete_post(api_client, patch_grpc_client, mock_grpc_posts_client, grpc_error_mock):
    # Регистрация пользователя
    test_user = await test_register_user(api_client)
    
    # Создаем фиктивные данные поста
    post_id = 1
    
    # Настраиваем ответ мока для DeletePost
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.message = "Post deleted successfully"
    mock_grpc_posts_client.DeletePost.return_value = mock_response
    
    # Отправляем запрос на удаление поста
    response = await api_client.delete(f"/posts/{post_id}?username={test_user['login']}")
    
    # Проверка успешного удаления поста
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Post deleted successfully"
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.DeletePost.assert_called_once()
    
    # Настраиваем мок, чтобы симулировать, что пост не найден после удаления
    mock_grpc_posts_client.GetPost.side_effect = grpc_error_mock(
        grpc.StatusCode.NOT_FOUND, "Post not found"
    )
    
    # Пытаемся получить удаленный пост
    response = await api_client.get(f"/posts/{post_id}")
    
    # Должны получить ошибку 404
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_posts(api_client, patch_grpc_client, mock_grpc_posts_client):
    # Регистрация пользователя
    test_user = await test_register_user(api_client)
    
    # Создаем фиктивные данные постов
    mock_posts = []
    for i in range(3):
        mock_posts.append(MagicMock(
            id=i+1,
            title=f"Test Post {i+1}",
            description=f"Description for test post {i+1}",
            username=test_user["login"],
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00",
            is_private=False,
            tags=["test", f"tag{i+1}"]
        ))
    
    # Настраиваем ответ мока для ListPosts
    mock_response = MagicMock()
    mock_response.posts = mock_posts
    mock_response.total = len(mock_posts)
    mock_response.page = 1
    mock_response.page_size = 10
    mock_response.pages = 1
    mock_grpc_posts_client.ListPosts.return_value = mock_response
    
    # Отправляем запрос на получение списка постов
    response = await api_client.get("/posts/")
    
    # Проверка успешного получения списка постов
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "pages" in data
    assert len(data["posts"]) == 3
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.ListPosts.assert_called_once()
    
    # Сбрасываем счетчик вызовов
    mock_grpc_posts_client.ListPosts.reset_mock()
    
    # Настраиваем ответ для фильтрации по имени пользователя
    mock_grpc_posts_client.ListPosts.return_value = mock_response
    
    # Проверяем фильтрацию по имени пользователя
    response = await api_client.get(f"/posts/?username={test_user['login']}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) == 3
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.ListPosts.assert_called_once()


@pytest.mark.asyncio
async def test_nonexistent_post(api_client, patch_grpc_client, mock_grpc_posts_client, grpc_error_mock):
    # Настраиваем мок, чтобы симулировать, что пост не найден
    mock_grpc_posts_client.GetPost.side_effect = grpc_error_mock(
        grpc.StatusCode.NOT_FOUND, "Post not found"
    )
    
    # Пытаемся получить несуществующий пост
    response = await api_client.get("/posts/99999")
    
    # Должны получить ошибку 404
    assert response.status_code == 404
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.GetPost.assert_called_once()


@pytest.mark.asyncio
async def test_post_with_tags(api_client, patch_grpc_client, mock_grpc_posts_client):
    # Регистрация пользователя
    test_user = await test_register_user(api_client)
    
    # Создаем фиктивные данные поста с тегами
    post_id = 1
    post_data = {
        "title": "Post with specific tags",
        "description": "This post has specific tags for testing",
        "username": test_user["login"],
        "is_private": False,
        "tags": ["important", "feature", "testing"]
    }
    
    # Настраиваем ответ мока для CreatePost
    create_response = MagicMock()
    create_response.post = MagicMock(
        id=post_id,
        title=post_data["title"],
        description=post_data["description"],
        username=post_data["username"],
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        is_private=post_data["is_private"],
        tags=post_data["tags"]
    )
    mock_grpc_posts_client.CreatePost.return_value = create_response
    
    # Отправляем запрос на создание поста
    response = await api_client.post("/posts/", json=post_data)
    assert response.status_code == 200
    
    # Настраиваем ответ мока для ListPosts с фильтром по тегу
    list_response = MagicMock()
    list_response.posts = [MagicMock(
        id=post_id,
        title=post_data["title"],
        description=post_data["description"],
        username=post_data["username"],
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        is_private=post_data["is_private"],
        tags=post_data["tags"]
    )]
    list_response.total = 1
    list_response.page = 1
    list_response.page_size = 10
    list_response.pages = 1
    mock_grpc_posts_client.ListPosts.return_value = list_response
    
    # Проверяем фильтрацию по тегу
    response = await api_client.get("/posts/?tag=important")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что в списке есть пост с нужным тегом
    assert len(data["posts"]) == 1
    assert data["posts"][0]["id"] == post_id
    assert "important" in data["posts"][0]["tags"]
    
    # Убеждаемся, что мок был вызван с правильными параметрами
    mock_grpc_posts_client.ListPosts.assert_called_once()
