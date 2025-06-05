#!/usr/bin/env python3
"""
PulseCare Hospital Management System - Comprehensive Page Testing Script
Tests all pages for accessibility, functionality, and proper loading.
"""

import requests
import time
import json
from datetime import datetime
import sys

class PulseCarePageTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Test credentials for different roles
        self.test_users = {
            'admin': {'username': 'admin', 'password': 'admin123'},
            'doctor': {'username': 'doctor.smith', 'password': 'doctor123'},
            'nurse': {'username': 'nurse.johnson', 'password': 'nurse123'},
            'lab_technician': {'username': 'lab.tech1', 'password': 'lab123'},
            'pharmacist': {'username': 'pharmacist1', 'password': 'pharm123'},
            'patient': {'username': 'patient.doe', 'password': 'patient123'}
        }
        
        # Pages to test for each role
        self.role_pages = {
            'public': [
                '/',
                '/index.html',
                '/login.html',
                '/about_us.html'
            ],
            'admin': [
                '/dashboard.html',
                '/admin/users.html',
                '/admin/patients.html',
                '/admin/health-records.html'
            ],
            'doctor': [
                '/dashboard.html',
                '/doctor/appointments.html',
                '/doctor/patients.html',
                '/doctor/prescriptions.html',
                '/doctor/lab-tests.html',
                '/doctor/medical-notes.html'
            ],
            'nurse': [
                '/dashboard.html',
                '/nurse/patients.html',
                '/nurse/vital-signs.html',
                '/nurse/assignments.html',
                '/nurse/nursing-notes.html'
            ],
            'lab_technician': [
                '/dashboard.html',
                '/lab/tests.html',
                '/lab/pending-tests.html',
                '/lab/in-progress-tests.html',
                '/lab/test-results.html',
                '/lab/enter-results.html'
            ],
            'pharmacist': [
                '/dashboard.html',
                '/pharmacy/prescriptions.html',
                '/pharmacy/dispense.html',
                '/pharmacy/inventory.html',
                '/pharmacy/history.html'
            ],
            'patient': [
                '/dashboard.html',
                '/patient/appointments.html',
                '/patient/health-records.html',
                '/patient/lab-results.html',
                '/patient/prescriptions.html',
                '/patient/vital-signs.html'
            ]
        }

    def log_test(self, test_name, status, message="", response_time=0):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        else:
            self.failed_tests += 1
            
        result = {
            'test_name': test_name,
            'status': status,
            'message': message,
            'response_time': response_time,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        # Print real-time results
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {status} ({response_time:.2f}s)")
        if message and status == "FAIL":
            print(f"   └─ {message}")

    def test_server_connectivity(self):
        """Test if the server is running"""
        print("\n🔍 Testing Server Connectivity...")
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/", timeout=5)
            response_time = time.time() - start_time

            if response.status_code == 200:
                self.log_test("Server Connectivity", "PASS", "Server is running", response_time)
                return True
            else:
                self.log_test("Server Connectivity", "FAIL", f"Server returned status {response.status_code}", response_time)
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Server Connectivity", "FAIL", f"Connection error: {str(e)}")
            # Try to test static files directly
            print("   ⚠️  Server not accessible via API, testing static files...")
            return self.test_static_files_directly()

    def test_static_files_directly(self):
        """Test static files directly from filesystem"""
        import os
        static_dir = "static"
        if os.path.exists(static_dir):
            self.log_test("Static Files Directory", "PASS", "Static directory exists")
            return True
        else:
            self.log_test("Static Files Directory", "FAIL", "Static directory not found")
            return False

    def test_public_pages(self):
        """Test public pages that don't require authentication"""
        print("\n🌐 Testing Public Pages...")
        
        for page in self.role_pages['public']:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{page}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    # Check for basic HTML structure
                    if '<html' in response.text.lower() and '</html>' in response.text.lower():
                        self.log_test(f"Public Page: {page}", "PASS", "Page loaded successfully", response_time)
                    else:
                        self.log_test(f"Public Page: {page}", "FAIL", "Invalid HTML structure", response_time)
                else:
                    self.log_test(f"Public Page: {page}", "FAIL", f"HTTP {response.status_code}", response_time)
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Public Page: {page}", "FAIL", f"Request error: {str(e)}")

    def login_as_user(self, role):
        """Attempt to login as a specific user role"""
        if role not in self.test_users:
            return False
            
        credentials = self.test_users[role]
        login_data = {
            'username': credentials['username'],
            'password': credentials['password']
        }
        
        try:
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/auth/login", 
                                       json=login_data, 
                                       timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    # Store token for subsequent requests
                    self.session.headers.update({'Authorization': f'Bearer {data["token"]}'})
                    self.log_test(f"Login as {role}", "PASS", "Authentication successful", response_time)
                    return True
                else:
                    self.log_test(f"Login as {role}", "FAIL", "No token in response", response_time)
                    return False
            else:
                self.log_test(f"Login as {role}", "FAIL", f"HTTP {response.status_code}", response_time)
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(f"Login as {role}", "FAIL", f"Request error: {str(e)}")
            return False

    def test_role_pages(self, role):
        """Test pages for a specific role"""
        print(f"\n👤 Testing {role.title()} Pages...")
        
        # Login as the role
        if not self.login_as_user(role):
            print(f"   ⚠️  Skipping {role} pages due to login failure")
            return
            
        # Test each page for this role
        for page in self.role_pages.get(role, []):
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{page}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    # Check for role-specific content
                    content = response.text.lower()
                    
                    # Check for basic HTML structure
                    if '<html' not in content or '</html>' not in content:
                        self.log_test(f"{role.title()}: {page}", "FAIL", "Invalid HTML structure", response_time)
                        continue
                    
                    # Check for authentication-related content
                    if 'login' in content and 'dashboard' not in page:
                        self.log_test(f"{role.title()}: {page}", "FAIL", "Redirected to login", response_time)
                        continue
                    
                    # Check for "coming soon" or "under development" messages
                    if 'coming soon' in content or 'under development' in content:
                        self.log_test(f"{role.title()}: {page}", "WARN", "Page shows 'coming soon' message", response_time)
                    else:
                        self.log_test(f"{role.title()}: {page}", "PASS", "Page loaded successfully", response_time)
                        
                elif response.status_code == 403:
                    self.log_test(f"{role.title()}: {page}", "FAIL", "Access forbidden", response_time)
                elif response.status_code == 404:
                    self.log_test(f"{role.title()}: {page}", "FAIL", "Page not found", response_time)
                else:
                    self.log_test(f"{role.title()}: {page}", "FAIL", f"HTTP {response.status_code}", response_time)
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"{role.title()}: {page}", "FAIL", f"Request error: {str(e)}")
        
        # Clear authentication for next role
        self.session.headers.pop('Authorization', None)

    def test_api_endpoints(self):
        """Test key API endpoints"""
        print("\n🔌 Testing API Endpoints...")
        
        # Test common endpoints without authentication
        endpoints = [
            '/common',
            '/medication',
            '/department'
        ]
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        self.log_test(f"API: {endpoint}", "PASS", f"Returned {len(data) if isinstance(data, list) else 'valid'} data", response_time)
                    except json.JSONDecodeError:
                        self.log_test(f"API: {endpoint}", "FAIL", "Invalid JSON response", response_time)
                else:
                    self.log_test(f"API: {endpoint}", "FAIL", f"HTTP {response.status_code}", response_time)
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"API: {endpoint}", "FAIL", f"Request error: {str(e)}")

    def run_all_tests(self):
        """Run all tests"""
        print("🏥 PulseCare Hospital Management System - Page Testing")
        print("=" * 60)
        print(f"Testing server at: {self.base_url}")
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test server connectivity first
        if not self.test_server_connectivity():
            print("\n❌ Server is not accessible. Aborting tests.")
            return False
        
        # Test public pages
        self.test_public_pages()
        
        # Test API endpoints
        self.test_api_endpoints()
        
        # Test role-specific pages
        for role in ['admin', 'doctor', 'nurse', 'lab_technician', 'pharmacist', 'patient']:
            self.test_role_pages(role)
        
        # Generate summary
        self.generate_summary()
        return True

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        
        if self.total_tests > 0:
            success_rate = (self.passed_tests / self.total_tests) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        # Show failed tests
        failed_tests = [test for test in self.test_results if test['status'] == 'FAIL']
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['test_name']}: {test['message']}")
        
        # Show warnings
        warning_tests = [test for test in self.test_results if test['status'] == 'WARN']
        if warning_tests:
            print(f"\n⚠️  WARNINGS ({len(warning_tests)}):")
            for test in warning_tests:
                print(f"   • {test['test_name']}: {test['message']}")
        
        print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save detailed results to file
        with open('test_results.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': self.total_tests,
                    'passed_tests': self.passed_tests,
                    'failed_tests': self.failed_tests,
                    'success_rate': (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
                },
                'results': self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results.json")

if __name__ == "__main__":
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    tester = PulseCarePageTester(base_url)
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success and tester.failed_tests == 0 else 1)
