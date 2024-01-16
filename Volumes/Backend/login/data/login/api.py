from typing import Any, Optional
from django.http import HttpRequest
#from ninja.responses import JSONResponse
from ninja.errors import HttpError

from ninja import Router
from . import schemas, crud
from transcendence import Logger

router = Router()
logger = Logger.Logger(name="login")

@router.post('/create_user', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):

    return crud.create_user(user)


@router.get('/get_user')
def get_user(request, user: schemas.Username):

    db_user = crud.get_user(user.username)
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exists")


@router.get('/login_user') #Creacion de endpoint
def login_user(request, username: str):
    
    #Hacer la peticion crud a la bbdd
    db_user = crud.get_user(username) 
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exist")
    
    # Devolver la información del usuario en un formato JSON #no me deja importar la libreria arriba comentada. 
    #user_data = {
    #    "username": db_user.username,
    #    "email": db_user.email,
    #}
    #return JSONResponse(content=user_data) 
    
    return {"username": db_user.username,"email": db_user.email} #(no necesario)la peticion ya devuelve el codigo 200 a la response, pero asi leemos a quien encuentra
