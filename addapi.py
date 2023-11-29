from blockchain.block.registerblock import Blockchain
import os
import hashlib

# Define the path to the blockchain data directory and the JSON file
blockchain_data_dir = 'blockchain/data/'
blockchain_file = os.path.join(blockchain_data_dir, 'dockervalid.json')

def email_exists( docker_id, blockchain):
    for block in blockchain.chain:
        for entry in block.data_history:
            if entry.endswith(f"Docker ID: {docker_id}"):
                return True
    return False


def perform_addapi(container_id, docker_id, accessPassword, userRole, session):
    if not container_id or not docker_id or not accessPassword or not userRole or not session:
        return {'status': 400, 'message': 'Email and password are required'}
    else:
        password = hashlib.sha256(accessPassword.encode()).hexdigest()
        if os.path.exists(blockchain_file):
            blockchain = Blockchain.load_from_file(blockchain_file)
        else:
            blockchain = Blockchain()

        # Check if the email already exists
        if email_exists(docker_id, blockchain):
            return {'status': 'error', 'message': 'Docker is already register'}

        # Add email and password data as a new block
        data = f"docker_id: {docker_id}, session: {session}, container_id: {container_id}, accessPassword: {password}, userRole: {userRole}"
        blockchain.mine_block(data)

        # Save the blockchain data to the JSON file
        blockchain.save_to_file(blockchain_file)

        return {'status': 'success', 'message': 'Registration successful'}
