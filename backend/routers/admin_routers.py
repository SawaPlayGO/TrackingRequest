from fastapi import APIRouter, Depends

from utils.depend import verify_admin

router = APIRouter(tags=["admin"], prefix="/admin")


@router.get("/check")
async def admin_check(username: str = Depends(verify_admin)) -> dict[str, str]:
    return {"status": "ok", "user": username}
