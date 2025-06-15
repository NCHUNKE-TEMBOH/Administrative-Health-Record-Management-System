#!/usr/bin/env python3
"""
Minimal Flask app to test blockchain functionality
"""

from flask import Flask, jsonify, request, send_from_directory
import json
import time
import hashlib
import sqlite3
import os

app = Flask(__name__, static_url_path='')

# Simple blockchain implementation
class SimpleBlock:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class SimpleBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return SimpleBlock(0, time.time(), {
            'type': 'genesis',
            'message': 'Administrative Health Record Management System Blockchain Initialized'
        }, '0')

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = SimpleBlock(
            index=last_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def to_list(self):
        return [block.to_dict() for block in self.chain]

# Initialize blockchain
blockchain = SimpleBlockchain()

# Add some sample data
sample_data = [
    {'type': 'medical_record', 'patientId': 1, 'diagnosis': 'Hypertension', 'doctor': 'Dr. Smith'},
    {'type': 'vital_signs', 'patientId': 1, 'blood_pressure_systolic': 140, 'heart_rate': 75},
    {'type': 'prescription', 'patientId': 1, 'medication_name': 'Lisinopril', 'dosage': '10mg'}
]

for data in sample_data:
    blockchain.add_block(data)

# API Routes
@app.route('/api/blockchain/chain', methods=['GET'])
def get_blockchain_chain():
    try:
        chain_data = blockchain.to_list()
        return jsonify({'chain': chain_data, 'length': len(chain_data)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/add', methods=['POST'])
def add_blockchain_record():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        block = blockchain.add_block(data)
        return jsonify({'block': block.to_dict(), 'message': 'Block added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/validate', methods=['GET'])
def validate_blockchain():
    try:
        is_valid = blockchain.is_chain_valid()
        return jsonify({'valid': is_valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Static file routes
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/blockchain/dashboard.html')
def blockchain_dashboard():
    return send_from_directory('static/blockchain', 'dashboard.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("🏥 Minimal Blockchain Test Server")
    print("🌐 Server: http://127.0.0.1:5001")
    print("🔗 Blockchain API: http://127.0.0.1:5001/api/blockchain/chain")
    print("🔗 Dashboard: http://127.0.0.1:5001/blockchain/dashboard.html")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=5001, debug=True)
