from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(title="API Gateway")

USERS_SERVICE_URL = "http://users-service:8000"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    url = f"{USERS_SERVICE_URL}/{path}"
    client = httpx.AsyncClient()
    
    # Копируем заголовки запроса
    headers = {key: value for key, value in request.headers.items() if key.lower() != "host"}
    
    # Получаем тело запроса, если оно есть
    body = await request.body()
    
    response = await client.request(
        method=request.method,
        url=url,
        headers=headers,
        content=body,
    )
    
    # Возвращаем ответ
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
