from typing import Any, Optional
from django.http import HttpRequest
#from ninja.responses import JSONResponse
from ninja.errors import HttpError

from ninja import Router
from . import schemas, crud
from transcendence import auth
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.post('/create_user', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):

    logger.warning(user)
    hashed_password = auth.get_password_hash(user.password)

    return crud.create_user(user, hashed_password)



@router.get('/get_user', auth=auth.Authentication())
def get_user(request, username: str):
    db_user = crud.get_user(username)
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exists")


@router.post('/login_user') #Creacion de endpoint
def login_user(request, username: str):
    # No recibo bien el json de frontend y no puedo generar el objeto. Desde un curl si funciona , creo , porque le mando el username a pelo
    
    #Tambien hay que usar esquemas
   
    #Hacer la peticion crud a la bbdd
    db_user = crud.get_user(username) 
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exist")
    
    #Validar la password

    # Devolver la información del usuario en un formato JSON #no me deja importar la libreria arriba comentada. 
    #user_data = {
    #    "username": db_user.username,
    #    "email": db_user.email,
    #}
    #return JSONResponse(content=user_data) 
    
    return {"username": db_user.username,"email": db_user.email} #(no necesario)la peticion ya devuelve el codigo 200 a la response, pero asi leemos a quien encuentra