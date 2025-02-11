from jwt import encode

def createToken(data: dict):
    token: str = encode(payload=data, key='misecret', algorithm='HS256')
    return token


    