import base64
import hashlib
import json
import time

SECRET_KEY = 'fuckmeasyoudo12111'

def encode(payload):
    header = {'alg': 'HS256', 'typ': 'JWT'}
    header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
    header_base64 = base64.urlsafe_b64encode(header_json.encode()).rstrip(b'=').decode()

    payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    payload_base64 = base64.urlsafe_b64encode(payload_json.encode()).rstrip(b'=').decode()

    signature_input = f"{header_base64}.{payload_base64}".encode()
    signature = hashlib.sha256(signature_input + SECRET_KEY.encode()).hexdigest()

    jwt_token = f"{header_base64}.{payload_base64}.{signature}"
    return jwt_token

def decode(jwt_token):
    parts = jwt_token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    header_base64, payload_base64, signature = parts
    signature_input = f"{header_base64}.{payload_base64}".encode()

    computed_signature = hashlib.sha256(signature_input + SECRET_KEY.encode()).hexdigest()
    if computed_signature != signature:
        raise ValueError("JWT signature verification failed")

    payload = base64.urlsafe_b64decode(payload_base64 + '=' * (4 - len(payload_base64) % 4))
    payload = payload.decode()

    return json.loads(payload)

