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
    # Calculate a hash of the entire blockchain content
    combined_data = ''.join(','.join(block.data_history) for block in blockchain.chain)
    return hashlib.sha256(combined_data.encode()).hexdigest()



def perform_viewapi(auth):
    if not auth:
        return {'status': 'error', 'message': 'Unable to fetch data'}
    else:
        if os.path.exists(blockchain_file):
            blockchain = Blockchain.load_from_file(blockchain_file)
        else:
            return {'status': 'error', 'message': 'No container found'}

        container_id = []
        i = 0
        for block in reversed(blockchain.chain):
            if block.data_history[0].startswith(f"session: {auth}"):
                container_id.insert(i, block.data_history[0].split(", ")[1].split(": ")[1])
                i+=1
                
        return {'status': 'success', 'data': container_id}
            
        
                
