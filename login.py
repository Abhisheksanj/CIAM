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
blockchain_file = os.path.join(blockchain_data_dir, 'register.json')

def calculate_blockchain_hash(blockchain):
    # Calculate a hash of the entire blockchain content
    combined_data = ''.join(','.join(block.data_history) for block in blockchain.chain)
    return hashlib.sha256(combined_data.encode()).hexdigest()

def generate_session_token(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def perform_login(email, password):
    if not email or not password:
        return {'status': 'error', 'message': 'Email and password are required'}
    else:
        password = hashlib.sha256(password.encode()).hexdigest()
        if os.path.exists(blockchain_file):
            blockchain = Blockchain.load_from_file(blockchain_file)
        else:
            return {'status': 'error', 'message': 'User not registered'}

        # Find the last block that matches the email
        last_matching_block = None
        for block in reversed(blockchain.chain):
            if block.data_history[0].startswith(f"Email: {email}"):
                last_matching_block = block
                break

        if last_matching_block:
            stored_hashed_password = last_matching_block.data_history[0].split(", ")[1].split(": ")[1]

            # Hash the entered password for comparison
            if stored_hashed_password == password:
                ip_address = request.remote_addr
                session_token = generate_session_token()

                # Generate a JWT token
                expiration_time = datetime.utcnow() + timedelta(hours=1)
                payload = {
                    'email': email,
                    'ip_address': ip_address,
                    'user_type': 'users',
                    'exp': expiration_time.strftime('%Y-%m-%d %H:%M:%S')  # Convert to string
                }
                token = encode(payload)

                response = {
                    'status': 'success',
                    'message': 'Authenticated successfully',
                    'path': '/dashboard',
                    'auth': token
                }
                return response
            else:
                return {'status': 'error', 'message': 'Bad credentials'}
        else:
            return {'status': 'error', 'message': 'User not registered'}
