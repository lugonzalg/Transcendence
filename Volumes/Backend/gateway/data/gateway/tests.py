import jwt
from ninja import Schema, Field
from django.core.validators import validate_email
from ninja.errors import HttpError
from django.test import TestCase
from pydantic import validator
import time

class JWTToken(Schema):

    token: str
    refresh: str

secret = "624f21243fe81295b67131fd772e207552a22742fe9e7637e3dfdaf14ad9810d"
algorithm = "HS256"
BEARER_OFFSET=7

REFRESH=100000
class JWTInput(Schema):
    email: str = Field(max_length=256, examples=["walter@gmail.com"])

    @validator('email')
    def validate_email(cls, v):

        try:
            validate_email(v)
        except Exception as err:
            raise HttpError(status_code=404, message="Email: bad format")
        return v
    expire_time: int = Field(ge=30)

import datetime

def encode_token(jwt_input: JWTInput) -> str:

    exp_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_input.expire_time)

    payload = {
        "email": jwt_input.email,
        "exp": exp_date
    }

    return jwt.encode(payload, secret, algorithm=algorithm)

def decode_token(token: str) -> str:

    try:
        decoded = jwt.decode(token, secret, algorithms=algorithm)
    except jwt.exceptions.InvalidSignatureError:
        raise HttpError(status_code=400, message="Error: Invalid Token")

    except jwt.exceptions.ExpiredSignatureError:
        raise HttpError(status_code=403, message="Error: Expired Token")

    except jwt.exceptions.DecodeError:
        raise HttpError(status_code=400, message="Error: Bad Token")

    except Exception:
        raise HttpError(status_code=404, message="Error: Unhandled Error")

    if decoded.get("email") is None:
        raise HttpError(status_code=403, message="Error: User Unauthorized")

    if decoded.get("exp") is None:
        raise HttpError(status_code=403, message="Error: No Time Expedition")

    return decoded

#@router.post("/refresh")
def refresh_token(jwt_token: JWTToken) -> JWTToken:

    token = decode_token(jwt_token.refresh)

    exp = token.get("exp")
    now = time.time()

    if now >= exp:
        raise HttpError(status_code=403, message="Error: Refresh Token Outdated")



def check_jwt(jwt_token: JWTToken) -> bool | HttpError:

    if not jwt_token.token.startswith("Bearer "):
        raise HttpError(status_code=400, message="Error: Token does not have bearer")

    decoded_token = decode_token(jwt_token.token[BEARER_OFFSET:])

    email = decoded_token.get("email")
    if validate_email(email):
        raise HttpError(status_code=400, message="Error: Bad user")

    exp = decoded_token.get("exp")
    now = int(time.time())

    if now > exp - 1000000:
        raise HttpError(status_code=403, message="Error: Token expired")

    return True

def create_jwt(request, jwt_input: JWTInput):

    #TOKEN
    token = encode_token(jwt_input)

    #REFRESH_TOKEN
    refresh_token = encode_token(jwt_input)

    return JWTToken(token=token, refresh=refresh_token)

def refresh_jwt(jwt_token: JWTToken):

    decoded = decode_token(jwt_token.refresh)

    email = decoded.get("email")
    if email is None:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    jwt_input = JWTInput(
        email=email,
        expire_time=30
    )

    jwt_token.token = encode_token(jwt_input)
    return jwt_token

# Create your tests here.
class CheckJWT(TestCase):

    count: int = 0

    def header(self, msg: str):

        self.count += 1
        print(f"\n[{self.count}] {msg}\n")

    def test_create_jwt(self):

        print("\n//////////////////////////")
        print("// Create JWT Test Cases//")
        print("//////////////////////////\n")
        try:
            self.header("No email")
            token_input = JWTInput(email=None, expire_time=30)
            self.assertEqual(encode_token(token_input), None)

        except Exception as err:
            print(err)

        try:
            self.header("No exp time")
            token_input = JWTInput(email="test@test.es", expire_time=None)
            self.assertEqual(encode_token(token_input), None)

        except Exception as err:
            print(err)

        try:
            self.header("No mail, no exp time")
            token_input = JWTInput(email=None, expire_time=None)
            self.assertEqual(encode_token(token_input), None)

        except Exception as err:
            print(err)

        try:
            self.header("Bad email")
            token_input = JWTInput(email="test.es", expire_time=30)
            self.assertEqual(encode_token(token_input), None)

        except Exception as err:
            print(err)

        try:
            self.header("Bad time type")
            token_input = JWTInput(email="test@test.es", expire_time="asfd")
            self.assertEqual(encode_token(token_input), None)

        except Exception as err:
            print(err)

        try:
            self.header("Bad time lapse")
            token_input = JWTInput(email="test@test.es", expire_time=10)
            self.assertEqual(encode_token(token_input), None)

        except Exception as err:
            print(err)

        try:
            self.header("Email and Exp time OK")
            token_input = JWTInput(email="test@test.es", expire_time=30)
            self.assertNotEqual(value := encode_token(token_input), None)
            print(value)

        except Exception as err:
            print(err)

    def test_decode_data(self):

        weird_jwt = "asdfasddf"
        random_jwt_1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoidXNlcjEyMyIsImV4cCI6MTY0NTY5NzA4Mn0.-0He71b6bhkfuS9xv3MBLNKDGz7dch4rDgyIDi1kH84"
        random_jwt_2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0NTYsInVzZXJuYW1lIjoidXNlcjQ1NiIsImV4cCI6MTY0NTY5NzA4M30.Z9cLRHGRNmtXrxTY0sDVll-x9zZSOOT0Bmsc5ZVJt0E"

        outdated_jwt = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDcyNDI3MTl9.HA10QXOoEwnUOxywKyAIqXHjxkoAMiCKlr24B0E2n6Q",
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDcyNDI3MTl9.HA10QXOoEwnUOxywKyAIqXHjxkoAMiCKlr24B0E2n6Q"
        }

        correct_jwt = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDcyNDY2MzV9.LVR9u_YH-kxRSBti8wTMWbsU8_OPJG5Y5ZRZEZLvhRg",
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDcyNDY2MzV9.LVR9u_YH-kxRSBti8wTMWbsU8_OPJG5Y5ZRZEZLvhRg"
        }

        try:
            self.header("weird jwt")
            decoded = decode_token(weird_jwt)
            print(decoded)
        except Exception as err:
            print(err)

        try:
            self.header("outdated jwt")
            decoded = decode_token(outdated_jwt['token'])
            print(decoded)
        except Exception as err:
            print(err)

        try:
            self.header("random jwt 1")
            decoded = decode_token(random_jwt_1)
            print(decoded)
        except Exception as err:
            print(err)

        try:
            self.header("random jwt 2")
            decoded = decode_token(random_jwt_2)
            print(decoded)
        except Exception as err:
            print(err)

        try:
            self.header("correct jwt")
            decoded = decode_token(correct_jwt['token'])
            print(decoded)
        except Exception as err:
            print(err)


    def test_check_jwt(self):

        print("Empty parameters")
        try:
            token_input = JWTToken(
                token=None,
                refresh=None)

            self.assertEqual(check_jwt(token_input), None)
        except Exception as err:
            print(err)

        print("No Bearer parameters")
        try:
            token_input = JWTToken(
                token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHBpcmVfdGltZSI6MzB9.4hMibspanHbe5dkkrXox7U-R3ztIXbCgdzTh7qK4AgI",
                refresh="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHBpcmVfdGltZSI6MTgwfQ.uAkc0UzPCkb70k3gDsJT36SXMFDIjju_h0G03rLejHg")

            self.assertEqual(check_jwt(token_input), None)
        except Exception as err:
            print(err)

        print("Normal parameters")
        try:
            token_input = JWTToken(
                token= "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDcyNDAxNDF9.98fFMoPcfg6rp_PqKRhvuE685Lh8d-pahz3CxPsNiwI",
                refresh= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDcyNDkxNDF9.7xzzwv5M99lWpiMT-PM0CBT3QKXdB8MbHfdmpGXxlto"
            )

            self.assertEqual(check_jwt(token_input), None)
        except Exception as err:
            print(err)

    def test_refresh_token(self):

        good_token = JWTToken(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDczMDg4Mjh9.g15poNX4D9cNU7I-LCkw-yI1yx9_9bL0nT_rhzp6xgI",
            refresh="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndhbHRlckBnbWFpbC5jb20iLCJleHAiOjE3MDczMDg4Mjh9.g15poNX4D9cNU7I-LCkw-yI1yx9_9bL0nT_rhzp6xgI"
        )

        self.assertIsNotNone(refresh_jwt(good_token))