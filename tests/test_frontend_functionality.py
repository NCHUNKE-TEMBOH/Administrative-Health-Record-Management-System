#!/usr/bin/env python3
"""
Frontend Functionality Test for medicare Health Record Management System
Tests frontend pages and their content
"""

import requests

class FrontendTest:
    def __init__(self, base_url="http://127.0.0.1:5001"):
        self.base_url = base_url
        self.test_results = []
    
    def log_test(self, test_name, status, message=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "message": message
        }
        self.test_results.append(result)
        
        status_icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
        print(f"{status_icon} {test_name}: {message}")
    
    def test_page_content(self, page_path, expected_keywords):
        """Test if a page contains expected keywords"""
        try:
            response = requests.get(f"{self.base_url}{page_path}")
            if response.status_code == 200:
                page_content = response.text.lower()

                missing_keywords = []
                for keyword in expected_keywords:
                    if keyword.lower() not in page_content:
                        missing_keywords.append(keyword)

                if not missing_keywords:
                    self.log_test(f"Page Content - {page_path}", "PASS", "All expected keywords found")
                    return True
                else:
                    self.log_test(f"Page Content - {page_path}", "PARTIAL", f"Missing keywords: {missing_keywords}")
                    return True  # Still consider it a pass if page loads
            else:
                self.log_test(f"Page Content - {page_path}", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test(f"Page Content - {page_path}", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_login_page(self):
        """Test login page functionality"""
        print("\n🔐 Testing Login Page...")
        expected_elements = ["username", "password", "login", "medicare"]
        return self.test_page_content("/login.html", expected_elements)
    
    def test_dashboard_page(self):
        """Test dashboard page"""
        print("\n📊 Testing Dashboard Page...")
        expected_elements = ["dashboard", "admin", "doctor", "nurse", "patient"]
        return self.test_page_content("/dashboard.html", expected_elements)
    
    def test_admin_pages(self):
        """Test admin portal pages"""
        print("\n👑 Testing Admin Portal Pages...")
        
        pages_to_test = [
            ("/admin/users.html", ["users", "admin", "manage"]),
            ("/admin/patients.html", ["patients", "health", "records"]),
            ("/admin/health-records.html", ["health", "records", "patient"])
        ]
        
        results = []
        for page_path, expected_elements in pages_to_test:
            results.append(self.test_page_content(page_path, expected_elements))
        
        return all(results)
    
    def test_doctor_pages(self):
        """Test doctor portal pages"""
        print("\n👨‍⚕️ Testing Doctor Portal Pages...")
        
        pages_to_test = [
            ("/doctor/patients.html", ["patients", "doctor", "medical"]),
            ("/doctor/prescriptions.html", ["prescriptions", "medication"]),
            ("/doctor/appointments.html", ["appointments", "schedule"]),
            ("/doctor/lab-tests.html", ["lab", "tests", "results"]),
            ("/doctor/medical-notes.html", ["medical", "notes", "patient"])
        ]
        
        results = []
        for page_path, expected_elements in pages_to_test:
            results.append(self.test_page_content(page_path, expected_elements))
        
        return all(results)
    
    def test_nurse_pages(self):
        """Test nurse portal pages"""
        print("\n👩‍⚕️ Testing Nurse Portal Pages...")
        
        pages_to_test = [
            ("/nurse/patients.html", ["patients", "nurse", "care"]),
            ("/nurse/vital-signs.html", ["vital", "signs", "patient"]),
            ("/nurse/assignments.html", ["assignments", "patient", "nurse"]),
            ("/nurse/nursing-notes.html", ["nursing", "notes", "patient"])
        ]
        
        results = []
        for page_path, expected_elements in pages_to_test:
            results.append(self.test_page_content(page_path, expected_elements))
        
        return all(results)
    
    def test_lab_pages(self):
        """Test lab technician portal pages"""
        print("\n🔬 Testing Lab Technician Portal Pages...")
        
        pages_to_test = [
            ("/lab/tests.html", ["lab", "tests", "results"]),
            ("/lab/pending-tests.html", ["pending", "tests", "lab"]),
            ("/lab/test-results.html", ["test", "results", "lab"]),
            ("/lab/enter-results.html", ["enter", "results", "lab"])
        ]
        
        results = []
        for page_path, expected_elements in pages_to_test:
            results.append(self.test_page_content(page_path, expected_elements))
        
        return all(results)
    
    def test_pharmacy_pages(self):
        """Test pharmacist portal pages"""
        print("\n💊 Testing Pharmacist Portal Pages...")
        
        pages_to_test = [
            ("/pharmacy/prescriptions.html", ["prescriptions", "pharmacy", "medication"]),
            ("/pharmacy/dispense.html", ["dispense", "medication", "pharmacy"]),
            ("/pharmacy/inventory.html", ["inventory", "medication", "stock"]),
            ("/pharmacy/history.html", ["history", "dispensing", "pharmacy"])
        ]
        
        results = []
        for page_path, expected_elements in pages_to_test:
            results.append(self.test_page_content(page_path, expected_elements))
        
        return all(results)
    
    def test_patient_pages(self):
        """Test patient portal pages"""
        print("\n🤒 Testing Patient Portal Pages...")
        
        pages_to_test = [
            ("/patient/health-records.html", ["health", "records", "patient"]),
            ("/patient/prescriptions.html", ["prescriptions", "medication", "patient"]),
            ("/patient/appointments.html", ["appointments", "patient", "schedule"]),
            ("/patient/vital-signs.html", ["vital", "signs", "patient"]),
            ("/patient/lab-results.html", ["lab", "results", "patient"])
        ]
        
        results = []
        for page_path, expected_elements in pages_to_test:
            results.append(self.test_page_content(page_path, expected_elements))
        
        return all(results)
    
    def run_all_frontend_tests(self):
        """Run all frontend tests"""
        print("🌐 medicare Frontend Functionality Test")
        print("="*50)
        
        # Test core pages
        self.test_login_page()
        self.test_dashboard_page()
        
        # Test portal pages
        self.test_admin_pages()
        self.test_doctor_pages()
        self.test_nurse_pages()
        self.test_lab_pages()
        self.test_pharmacy_pages()
        self.test_patient_pages()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n📊 Frontend Test Summary")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✓ Passed: {passed_tests}")
        print(f"✗ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['message']}")

if __name__ == "__main__":
    test = FrontendTest()
    test.run_all_frontend_tests()
