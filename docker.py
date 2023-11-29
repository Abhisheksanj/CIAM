import hashlib
import random
import string
from blockchain.block.registerblock import Blockchain
import os
from flask import Flask, request, jsonify
from function.jwt import encode
from datetime import datetime, timedelta

# Define the path to the blockchain data directory and the JSON file
blockchain_data_dir = 'blockchain/data/'
blockchain_file = os.path.join(blockchain_data_dir, 'dockervalid.json')



def calculate_blockchain_hash(blockchain):
    combined_data = ''.join(','.join(block['data_history']) for block in blockchain.chain)
    return hashlib.sha256(combined_data.encode()).hexdigest()

def generate_session_token(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def perform_docker(data):
    data = request.json
    docker_id = data['docker_id']
    validation_pwd = data['validation_pwd']
    container_id = data['container_id']
    
    if not docker_id or not validation_pwd or not container_id:
        return jsonify({'status': 'error', 'message': 'Authentication failed'})

    password = hashlib.sha256(validation_pwd.encode()).hexdigest()
    
    if os.path.exists(blockchain_file):
        blockchain = Blockchain.load_from_file(blockchain_file)
    else:
        return jsonify({'status': 'error', 'message': 'No block found'})

    for block in reversed(blockchain.chain):
        if block.data_history[0].startswith(f"docker_id: {docker_id}"):
            stored_validation_pwd = block.data_history[0].split(", ")[3].split(": ")[1]
            stored_container_id = block.data_history[0].split(", ")[2].split(": ")[1]
            stored_role = block.data_history[0].split(", ")[4].split(": ")[1]

            if stored_validation_pwd == password and stored_container_id == container_id:
                response = {
                    'status': 'success',
                    'message': 'Docker verification successful',
                    'role': stored_role
                }
                return (response)
            else:
                return ({'status': 'error', 'message': 'Bad credentials'})

    return ({'status': 'error', 'message': 'User not registered'})


