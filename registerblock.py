import hashlib
import time
import json
import os

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data_history = [data]  # Store data history as a list
        self.nonce = nonce
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block", 0, self.calculate_hash(0, "0", int(time.time()), "Genesis Block", 0))

    def calculate_hash(self, index, previous_hash, timestamp, data, nonce):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(nonce)
        return hashlib.sha256(value.encode()).hexdigest()

    def mine_block(self, data):
        index = len(self.chain)
        previous_hash = self.chain[-1].hash if self.chain else "0"
        timestamp = int(time.time())
        nonce = 0
        while True:
            hash_attempt = self.calculate_hash(index, previous_hash, timestamp, data, nonce)
            if hash_attempt[:4] == "0000":  # Adjust the difficulty by changing the prefix
                new_block = Block(index, previous_hash, timestamp, data, nonce, hash_attempt)
                self.chain.append(new_block)
                return new_block
            nonce += 1
    
    

    

    def to_dict(self):
        return [block.__dict__ for block in self.chain]

    @classmethod
    def from_dict(cls, block_list):
        blockchain = cls()
        for block_data in block_list:
            block = Block(
                block_data['index'],
                block_data['previous_hash'],
                block_data['timestamp'],
                block_data['data_history'][0],  # Access the first element of the 'data_history' list
                block_data['nonce'],
                block_data['hash']
            )
            blockchain.chain.append(block)
        return blockchain




    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def load_from_file(cls, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return cls.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return cls()

blockchain = Blockchain()