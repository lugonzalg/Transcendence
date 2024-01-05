from ninja import Router

from . import schemas

router = Router()

@router.post("/create_user")
async def create_user(request, user: schemas.User):

    return {"user": "new user"}