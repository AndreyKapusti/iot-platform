from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"}
    ]

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}