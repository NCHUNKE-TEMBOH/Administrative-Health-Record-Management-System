// Medical Records Blockchain Implementation
// Secure, immutable medical record management system

class MedicalBlock {
    constructor(index, timestamp, data, previousHash) {
        this.index = index;
        this.timestamp = timestamp;
        this.data = data;
        this.previousHash = previousHash;
        this.nonce = 0;
        this.hash = this.calculateHash();
    }

    calculateHash() {
        return CryptoJS.SHA256(
            this.index + 
            this.previousHash + 
            this.timestamp + 
            JSON.stringify(this.data) + 
            this.nonce
        ).toString();
    }

    mineBlock(difficulty) {
        const target = Array(difficulty + 1).join("0");
        while (this.hash.substring(0, difficulty) !== target) {
            this.nonce++;
            this.hash = this.calculateHash();
        }
        console.log(`Block mined: ${this.hash}`);
    }
}

class MedicalBlockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
        this.difficulty = 2;
        this.pendingTransactions = [];
        this.miningReward = 100;
        this.loadFromStorage();
    }

    createGenesisBlock() {
        return new MedicalBlock(0, "01/01/2024", {
            type: "genesis",
            message: "Healthcare Management System Blockchain Initialized",
            hospital: "Administrative Health Record Management System"
        }, "0");
    }

    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }

    addMedicalRecord(recordData) {
        const newBlock = new MedicalBlock(
            this.chain.length,
            new Date().toISOString(),
            {
                type: "medical_record",
                ...recordData,
                timestamp: new Date().toISOString(),
                blockId: this.generateBlockId()
            },
            this.getLatestBlock().hash
        );

        newBlock.mineBlock(this.difficulty);
        this.chain.push(newBlock);
        this.saveToStorage();
        return newBlock;
    }

    addVitalSigns(vitalData) {
        const newBlock = new MedicalBlock(
            this.chain.length,
            new Date().toISOString(),
            {
                type: "vital_signs",
                ...vitalData,
                timestamp: new Date().toISOString(),
                blockId: this.generateBlockId()
            },
            this.getLatestBlock().hash
        );

        newBlock.mineBlock(this.difficulty);
        this.chain.push(newBlock);
        this.saveToStorage();
        return newBlock;
    }

    addPrescription(prescriptionData) {
        const newBlock = new MedicalBlock(
            this.chain.length,
            new Date().toISOString(),
            {
                type: "prescription",
                ...prescriptionData,
                timestamp: new Date().toISOString(),
                blockId: this.generateBlockId()
            },
            this.getLatestBlock().hash
        );

        newBlock.mineBlock(this.difficulty);
        this.chain.push(newBlock);
        this.saveToStorage();
        return newBlock;
    }

    addLabResult(labData) {
        const newBlock = new MedicalBlock(
            this.chain.length,
            new Date().toISOString(),
            {
                type: "lab_result",
                ...labData,
                timestamp: new Date().toISOString(),
                blockId: this.generateBlockId()
            },
            this.getLatestBlock().hash
        );

        newBlock.mineBlock(this.difficulty);
        this.chain.push(newBlock);
        this.saveToStorage();
        return newBlock;
    }

    generateBlockId() {
        return 'BLK_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    isChainValid() {
        for (let i = 1; i < this.chain.length; i++) {
            const currentBlock = this.chain[i];
            const previousBlock = this.chain[i - 1];

            if (currentBlock.hash !== currentBlock.calculateHash()) {
                return false;
            }

            if (currentBlock.previousHash !== previousBlock.hash) {
                return false;
            }
        }
        return true;
    }

    getPatientRecords(patientId) {
        return this.chain.filter(block => 
            block.data.patientId === patientId || 
            block.data.pat_id === patientId
        );
    }

    getRecordsByType(type) {
        return this.chain.filter(block => block.data.type === type);
    }

    getAuditTrail() {
        return this.chain.map(block => ({
            blockIndex: block.index,
            timestamp: block.timestamp,
            type: block.data.type,
            hash: block.hash,
            previousHash: block.previousHash,
            dataHash: CryptoJS.SHA256(JSON.stringify(block.data)).toString()
        }));
    }

    saveToStorage() {
        try {
            localStorage.setItem('medicalBlockchain', JSON.stringify(this.chain));
        } catch (error) {
            console.error('Error saving blockchain to storage:', error);
        }
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem('medicalBlockchain');
            if (stored) {
                const chainData = JSON.parse(stored);
                if (chainData.length > 1) {
                    this.chain = chainData.map(blockData => {
                        const block = new MedicalBlock(
                            blockData.index,
                            blockData.timestamp,
                            blockData.data,
                            blockData.previousHash
                        );
                        block.hash = blockData.hash;
                        block.nonce = blockData.nonce;
                        return block;
                    });
                }
            }
        } catch (error) {
            console.error('Error loading blockchain from storage:', error);
        }
    }

    getBlockchainStats() {
        const totalBlocks = this.chain.length;
        const medicalRecords = this.getRecordsByType('medical_record').length;
        const vitalSigns = this.getRecordsByType('vital_signs').length;
        const prescriptions = this.getRecordsByType('prescription').length;
        const labResults = this.getRecordsByType('lab_result').length;

        return {
            totalBlocks,
            medicalRecords,
            vitalSigns,
            prescriptions,
            labResults,
            isValid: this.isChainValid(),
            lastBlockHash: this.getLatestBlock().hash
        };
    }

    exportBlockchain() {
        return {
            chain: this.chain,
            stats: this.getBlockchainStats(),
            exportDate: new Date().toISOString()
        };
    }
}

// Initialize global blockchain instance
window.medicalBlockchain = new MedicalBlockchain();

// Blockchain utility functions
window.BlockchainUtils = {
    addMedicalRecord: function(recordData) {
        return window.medicalBlockchain.addMedicalRecord(recordData);
    },

    addVitalSigns: function(vitalData) {
        return window.medicalBlockchain.addVitalSigns(vitalData);
    },

    addPrescription: function(prescriptionData) {
        return window.medicalBlockchain.addPrescription(prescriptionData);
    },

    addLabResult: function(labData) {
        return window.medicalBlockchain.addLabResult(labData);
    },

    getPatientRecords: function(patientId) {
        return window.medicalBlockchain.getPatientRecords(patientId);
    },

    getAuditTrail: function() {
        return window.medicalBlockchain.getAuditTrail();
    },

    getStats: function() {
        return window.medicalBlockchain.getBlockchainStats();
    },

    validateChain: function() {
        return window.medicalBlockchain.isChainValid();
    },

    exportData: function() {
        return window.medicalBlockchain.exportBlockchain();
    }
};

console.log('Medical Blockchain System Initialized');
console.log('Blockchain Stats:', window.BlockchainUtils.getStats());
