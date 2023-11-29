from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    from auth.login import perform_login
    response = perform_login(email, password)
    return jsonify(response)


@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    from auth.register import perform_register
    response = perform_register(email, password)
    return jsonify(response)

@auth_bp.route('/verify', methods=['POST'])
def verify():
    auth = request.json.get('auth')
    from auth.verify import perform_verify
    response = perform_verify(auth)
    return jsonify(response)

@auth_bp.route('/docker_image_verify', methods=['POST'])
def docker_image_verify():
    data = request.json

    if 'docker_id' in data and 'validation_pwd' in data:
        from auth.docker import perform_docker
        response = perform_docker(data)
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Required parameters not provided'}), 400

@auth_bp.route('/addapi', methods=['POST'])
def addapi():
    container_id = request.json.get('containerId')
    docker_id = request.json.get('dockerId')
    accessPassword = request.json.get('accessPassword')
    userRole = request.json.get('userRole')
    session = request.json.get('session')
    from auth.addapi import perform_addapi
    response = perform_addapi(container_id, docker_id, accessPassword, userRole, session)
    return jsonify(response)

@auth_bp.route('/viewapi', methods=['POST'])
def viewapi():
    auth = request.json.get('auth')
    from auth.viewapi import perform_viewapi
    response = perform_viewapi(auth)
    return jsonify(response)
    




