from blockchain.block.registerblock import Blockchain
import os
import hashlib

# Define the path to the blockchain data directory and the JSON file
blockchain_data_dir = 'blockchain/data/'
blockchain_file = os.path.join(blockchain_data_dir, 'register.json')

def email_exists(email, blockchain):
    for block in blockchain.chain:
        if any(entry.startswith(f"Email: {email}") for entry in block.data_history):
            return True
    return False

def perform_register(email, password):
    if not email or not password:
        return {'status': 400, 'message': 'Email and password are required'}
    else:
        # Create or load the blockchain
        password = hashlib.sha256(password.encode()).hexdigest()
        if os.path.exists(blockchain_file):
            blockchain = Blockchain.load_from_file(blockchain_file)
        else:
            blockchain = Blockchain()

        # Check if the email already exists
        if email_exists(email, blockchain):
            return {'status': 'error', 'message': 'Email already registered'}

        # Add email and password data as a new block
        data = f"Email: {email}, Password: {password}"
        blockchain.mine_block(data)

        # Save the blockchain data to the JSON file
        blockchain.save_to_file(blockchain_file)

        return {'status': 'success', 'message': 'Registration successful'}
