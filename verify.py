from function.jwt import decode

def perform_verify(auth):
    if not auth:
        return {'status': 'error', 'message': 'Session expired'}
    else:
        try:
            decoded_payload = decode(auth)
            if decoded_payload is None:
                return {'status': 'error', 'message': 'Invalid token'}
            else:
                return {'status': 'success', 'message': 'You are authorized'}
        except ValueError as e:
            return {'status': 'error', 'message': 'Invalid token'}