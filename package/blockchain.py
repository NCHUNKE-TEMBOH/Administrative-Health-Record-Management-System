import hashlib
import json
import time
import sqlite3
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self, db_path: str = None):
        self.chain: List[Block] = []
        self.db_path = db_path
        self.pending_transactions = []

        # Initialize database tables
        self.init_database()

        # Load existing blockchain from database
        self.load_from_database()

        # Create genesis block if chain is empty
        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_to_database()
            print("✓ Genesis block created and saved to database")

    def init_database(self):
        """Initialize blockchain database tables"""
        if not self.db_path:
            print("⚠ No database path provided for blockchain")
            return

        try:
            conn = sqlite3.connect(self.db_path)

            # Create blockchain blocks table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS blockchain_blocks (
                    block_index INTEGER PRIMARY KEY,
                    timestamp REAL NOT NULL,
                    data TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    record_type TEXT,
                    patient_id INTEGER,
                    created_by INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create blockchain metadata table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS blockchain_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create blockchain audit log
            conn.execute('''
                CREATE TABLE IF NOT EXISTS blockchain_audit_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    block_index INTEGER,
                    details TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Initialize metadata
            conn.execute('''
                INSERT OR IGNORE INTO blockchain_metadata (key, value)
                VALUES
                ('initialized', 'true'),
                ('version', '2.0'),
                ('created_at', datetime('now'))
            ''')

            conn.commit()
            conn.close()
            print("✓ Blockchain database tables initialized")

        except Exception as e:
            print(f"❌ Error initializing blockchain database: {e}")

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), {
            'type': 'genesis',
            'message': 'Administrative Health Record Management System Blockchain Initialized',
            'hospital': 'Medicare Health System',
            'version': '2.0'
        }, '0')

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Dict[str, Any]) -> Block:
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        self.save_to_database()
        return new_block

    def add_health_record(self, record_data: Dict[str, Any]) -> Block:
        """Add a health record to the blockchain with enhanced security"""
        try:
            blockchain_data = {
                'type': 'health_record',
                'record_id': record_data.get('record_id'),
                'patient_id': record_data.get('patient_id') or record_data.get('pat_id'),
                'record_type': record_data.get('record_type'),
                'title': record_data.get('title'),
                'content_hash': record_data.get('content_hash'),
                'created_by': record_data.get('created_by'),
                'timestamp': record_data.get('timestamp') or time.time(),
                'security_level': 'HIGH',
                'encryption_method': 'SHA256',
                'hash_verification': hashlib.sha256(str(record_data).encode()).hexdigest()
            }

            block = self.add_block(blockchain_data)

            # Log to audit trail
            if self.db_path:
                try:
                    conn = sqlite3.connect(self.db_path)
                    conn.execute('''
                        INSERT INTO blockchain_audit_log (action, block_index, details)
                        VALUES ('HEALTH_RECORD_ADDED', ?, ?)
                    ''', (block.index, f"Health record {record_data.get('record_id')} for patient {record_data.get('patient_id')}"))
                    conn.commit()
                    conn.close()
                except Exception as e:
                    print(f"⚠ Audit log error: {e}")

            return block

        except Exception as e:
            print(f"❌ Error adding health record to blockchain: {e}")
            raise

    def add_vital_signs(self, vital_data: Dict[str, Any]) -> Block:
        """Add vital signs to the blockchain"""
        blockchain_data = {
            'type': 'vital_signs',
            'vital_id': vital_data.get('vital_id'),
            'patient_id': vital_data.get('pat_id'),
            'recorded_by': vital_data.get('recorded_by'),
            'temperature': vital_data.get('temperature'),
            'blood_pressure_systolic': vital_data.get('blood_pressure_systolic'),
            'blood_pressure_diastolic': vital_data.get('blood_pressure_diastolic'),
            'heart_rate': vital_data.get('heart_rate'),
            'timestamp': time.time(),
            'hash_verification': hashlib.sha256(str(vital_data).encode()).hexdigest()
        }
        return self.add_block(blockchain_data)

    def add_prescription(self, prescription_data: Dict[str, Any]) -> Block:
        """Add prescription to the blockchain"""
        blockchain_data = {
            'type': 'prescription',
            'prescription_id': prescription_data.get('prescription_id'),
            'patient_id': prescription_data.get('pat_id'),
            'doctor_id': prescription_data.get('doc_id'),
            'medication_code': prescription_data.get('med_code'),
            'dosage': prescription_data.get('dosage'),
            'frequency': prescription_data.get('frequency'),
            'timestamp': time.time(),
            'hash_verification': hashlib.sha256(str(prescription_data).encode()).hexdigest()
        }
        return self.add_block(blockchain_data)

    def add_lab_result(self, lab_data: Dict[str, Any]) -> Block:
        """Add lab result to the blockchain"""
        blockchain_data = {
            'type': 'lab_result',
            'test_id': lab_data.get('test_id'),
            'patient_id': lab_data.get('pat_id'),
            'test_type': lab_data.get('test_type'),
            'result_value': lab_data.get('result_value'),
            'status': lab_data.get('status'),
            'technician_id': lab_data.get('technician_id'),
            'timestamp': time.time(),
            'hash_verification': hashlib.sha256(str(lab_data).encode()).hexdigest()
        }
        return self.add_block(blockchain_data)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def get_patient_records(self, patient_id: int) -> List[Dict[str, Any]]:
        """Get all blockchain records for a specific patient"""
        patient_blocks = []
        for block in self.chain:
            if block.data.get('patient_id') == patient_id:
                patient_blocks.append(block.to_dict())
        return patient_blocks

    def get_records_by_type(self, record_type: str) -> List[Dict[str, Any]]:
        """Get all blockchain records of a specific type"""
        type_blocks = []
        for block in self.chain:
            if block.data.get('type') == record_type:
                type_blocks.append(block.to_dict())
        return type_blocks

    def save_to_database(self):
        """Save blockchain to database for persistence"""
        if not self.db_path:
            return

        try:
            conn = sqlite3.connect(self.db_path)

            # Clear existing blocks and insert current chain
            conn.execute('DELETE FROM blockchain_blocks')

            for block in self.chain:
                # Extract metadata from block data
                data = block.data
                record_type = data.get('type', 'unknown')
                patient_id = data.get('patient_id') or data.get('pat_id')
                created_by = data.get('created_by') or data.get('recorded_by') or data.get('doctor_id') or data.get('technician_id')

                conn.execute('''
                    INSERT INTO blockchain_blocks
                    (block_index, timestamp, data, previous_hash, hash, record_type, patient_id, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    block.index,
                    block.timestamp,
                    json.dumps(block.data),
                    block.previous_hash,
                    block.hash,
                    record_type,
                    patient_id,
                    created_by
                ))

            # Update metadata
            conn.execute('''
                INSERT OR REPLACE INTO blockchain_metadata (key, value)
                VALUES
                ('total_blocks', ?),
                ('last_updated', datetime('now')),
                ('chain_valid', ?),
                ('last_block_hash', ?)
            ''', (
                len(self.chain),
                'true' if self.is_chain_valid() else 'false',
                self.get_last_block().hash if self.chain else ''
            ))

            # Log the save action
            conn.execute('''
                INSERT INTO blockchain_audit_log (action, details)
                VALUES ('BLOCKCHAIN_SAVED', ?)
            ''', (f"Saved {len(self.chain)} blocks to database",))

            conn.commit()
            conn.close()
            print(f"✓ Blockchain saved to database: {len(self.chain)} blocks")

        except Exception as e:
            print(f"❌ Error saving blockchain to database: {e}")
            import traceback
            traceback.print_exc()

    def load_from_database(self):
        """Load blockchain from database"""
        if not self.db_path:
            print("⚠ No database path provided for blockchain")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row

            # Check if blockchain table exists
            table_exists = conn.execute('''
                SELECT name FROM sqlite_master WHERE type='table' AND name='blockchain_blocks'
            ''').fetchone()

            if not table_exists:
                print("ℹ Blockchain table doesn't exist yet, will be created on first save")
                conn.close()
                return

            blocks = conn.execute('''
                SELECT * FROM blockchain_blocks ORDER BY block_index
            ''').fetchall()

            if blocks:
                self.chain = []
                loaded_count = 0

                for block_row in blocks:
                    try:
                        block = Block(
                            index=block_row['block_index'],
                            timestamp=block_row['timestamp'],
                            data=json.loads(block_row['data']),
                            previous_hash=block_row['previous_hash']
                        )
                        block.hash = block_row['hash']  # Use stored hash
                        self.chain.append(block)
                        loaded_count += 1
                    except Exception as block_error:
                        print(f"❌ Error loading block {block_row['block_index']}: {block_error}")
                        continue

                print(f"✓ Loaded {loaded_count} blocks from database")

                # Validate loaded chain
                if self.is_chain_valid():
                    print("✓ Loaded blockchain is valid")
                else:
                    print("⚠ Loaded blockchain validation failed")

                # Log the load action
                conn.execute('''
                    INSERT INTO blockchain_audit_log (action, details)
                    VALUES ('BLOCKCHAIN_LOADED', ?)
                ''', (f"Loaded {loaded_count} blocks from database",))
                conn.commit()

            else:
                print("ℹ No blocks found in database")

            conn.close()

        except Exception as e:
            print(f"❌ Error loading blockchain from database: {e}")
            # Initialize with empty chain if loading fails
            self.chain = []

    def to_list(self) -> List[Dict[str, Any]]:
        return [block.to_dict() for block in self.chain]

    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get comprehensive blockchain statistics"""
        if not self.chain:
            return {
                'total_blocks': 0,
                'is_valid': True,
                'genesis_block': None,
                'latest_block': None,
                'record_types': {},
                'patients_count': 0
            }

        # Count record types
        record_types = {}
        patients = set()

        for block in self.chain:
            block_type = block.data.get('type', 'unknown')
            record_types[block_type] = record_types.get(block_type, 0) + 1

            patient_id = block.data.get('patient_id') or block.data.get('pat_id')
            if patient_id:
                patients.add(patient_id)

        return {
            'total_blocks': len(self.chain),
            'is_valid': self.is_chain_valid(),
            'genesis_block': self.chain[0].to_dict() if self.chain else None,
            'latest_block': self.chain[-1].to_dict() if self.chain else None,
            'record_types': record_types,
            'patients_count': len(patients),
            'database_path': self.db_path
        }

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.db_path:
            return {'error': 'No database path configured'}

        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row

            # Get metadata
            metadata = {}
            meta_rows = conn.execute('SELECT key, value FROM blockchain_metadata').fetchall()
            for row in meta_rows:
                metadata[row['key']] = row['value']

            # Get audit log count
            audit_count = conn.execute('SELECT COUNT(*) as count FROM blockchain_audit_log').fetchone()['count']

            # Get record type distribution
            type_dist = conn.execute('''
                SELECT record_type, COUNT(*) as count
                FROM blockchain_blocks
                WHERE record_type IS NOT NULL
                GROUP BY record_type
            ''').fetchall()

            conn.close()

            return {
                'metadata': metadata,
                'audit_log_entries': audit_count,
                'record_type_distribution': {row['record_type']: row['count'] for row in type_dist}
            }

        except Exception as e:
            return {'error': str(e)}

    def add_sample_data(self):
        """Add sample medical data to blockchain for testing"""
        sample_records = [
            {
                'type': 'health_record',
                'patient_id': 8,  # Jane Doe
                'record_type': 'diagnosis',
                'title': 'Hypertension Diagnosis',
                'diagnosis': 'Essential Hypertension',
                'created_by': 2  # Dr. Smith
            },
            {
                'type': 'vital_signs',
                'patient_id': 8,
                'temperature': 98.6,
                'blood_pressure_systolic': 140,
                'blood_pressure_diastolic': 90,
                'heart_rate': 75,
                'recorded_by': 20  # Nurse Emily
            },
            {
                'type': 'prescription',
                'patient_id': 8,
                'doctor_id': 2,
                'medication_name': 'Lisinopril',
                'dosage': '10mg',
                'frequency': 'Once daily'
            },
            {
                'type': 'lab_result',
                'patient_id': 8,
                'test_type': 'Blood Pressure Monitoring',
                'result_value': '140/90 mmHg',
                'status': 'completed',
                'technician_id': 17  # Lab Chen
            }
        ]

        added_count = 0
        for record in sample_records:
            try:
                self.add_block(record)
                added_count += 1
            except Exception as e:
                print(f"❌ Error adding sample record: {e}")

        print(f"✓ Added {added_count} sample records to blockchain")
        return added_count
