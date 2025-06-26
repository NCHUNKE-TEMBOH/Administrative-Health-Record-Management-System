#!/usr/bin/env python3
"""
Test automation script for Administrative Health Record Management System
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path


class TestRunner:
    """Test runner class for managing different types of tests"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.coverage_dir = self.project_root / "htmlcov"
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.coverage_dir.mkdir(exist_ok=True)
    
    def install_dependencies(self):
        """Install test dependencies"""
        print("📦 Installing test dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "tests/requirements.txt"
            ], check=True, cwd=self.project_root)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def run_unit_tests(self):
        """Run unit tests"""
        print("\n🧪 Running Unit Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit/",
            "-v",
            "--tb=short",
            "--cov=package",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov/unit",
            "--html=reports/unit_tests.html",
            "--self-contained-html",
            "-m", "unit or not (integration or e2e)"
        ]
        
        return self._run_command(cmd, "Unit tests")
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("\n🔗 Running Integration Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/integration/",
            "-v",
            "--tb=short",
            "--cov=package",
            "--cov-append",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov/integration",
            "--html=reports/integration_tests.html",
            "--self-contained-html",
            "-m", "integration or not (unit or e2e)"
        ]
        
        return self._run_command(cmd, "Integration tests")
    
    def run_e2e_tests(self):
        """Run end-to-end tests"""
        print("\n🌐 Running End-to-End Tests...")
        
        # Check if server is running
        if not self._check_server_running():
            print("⚠️  Server not running. Starting server...")
            if not self._start_server():
                print("❌ Failed to start server. Skipping E2E tests.")
                return False
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/e2e/",
            "-v",
            "--tb=short",
            "--html=reports/e2e_tests.html",
            "--self-contained-html",
            "-m", "e2e or not (unit or integration)"
        ]
        
        return self._run_command(cmd, "End-to-end tests")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n🚀 Running All Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--cov=package",
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=xml:coverage.xml",
            "--cov-fail-under=80",
            "--html=reports/all_tests.html",
            "--self-contained-html",
            "--junitxml=reports/junit.xml"
        ]
        
        return self._run_command(cmd, "All tests")
    
    def run_smoke_tests(self):
        """Run smoke tests for basic functionality"""
        print("\n💨 Running Smoke Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-m", "smoke",
            "--html=reports/smoke_tests.html",
            "--self-contained-html"
        ]
        
        return self._run_command(cmd, "Smoke tests")
    
    def run_security_tests(self):
        """Run security tests"""
        print("\n🔒 Running Security Tests...")
        
        # Run bandit for security analysis
        print("Running Bandit security analysis...")
        bandit_cmd = [
            sys.executable, "-m", "bandit",
            "-r", "package/", "app.py",
            "-f", "json",
            "-o", "reports/bandit_report.json"
        ]
        
        bandit_success = self._run_command(bandit_cmd, "Bandit security analysis", check=False)
        
        # Run security-marked tests
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-m", "security",
            "--html=reports/security_tests.html",
            "--self-contained-html"
        ]
        
        pytest_success = self._run_command(cmd, "Security tests")
        
        return bandit_success and pytest_success
    
    def run_performance_tests(self):
        """Run performance tests"""
        print("\n⚡ Running Performance Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-m", "performance",
            "--benchmark-only",
            "--benchmark-html=reports/benchmark.html",
            "--html=reports/performance_tests.html",
            "--self-contained-html"
        ]
        
        return self._run_command(cmd, "Performance tests")
    
    def generate_coverage_report(self):
        """Generate comprehensive coverage report"""
        print("\n📊 Generating Coverage Report...")
        
        # Generate HTML coverage report
        html_cmd = [sys.executable, "-m", "coverage", "html", "-d", "htmlcov"]
        html_success = self._run_command(html_cmd, "HTML coverage report")
        
        # Generate XML coverage report
        xml_cmd = [sys.executable, "-m", "coverage", "xml", "-o", "coverage.xml"]
        xml_success = self._run_command(xml_cmd, "XML coverage report")
        
        # Generate terminal report
        term_cmd = [sys.executable, "-m", "coverage", "report", "--show-missing"]
        term_success = self._run_command(term_cmd, "Terminal coverage report")
        
        if html_success:
            print(f"📈 Coverage report available at: {self.coverage_dir}/index.html")
        
        return html_success and xml_success and term_success
    
    def clean_reports(self):
        """Clean old test reports"""
        print("\n🧹 Cleaning old reports...")
        
        import shutil
        
        try:
            if self.reports_dir.exists():
                shutil.rmtree(self.reports_dir)
                self.reports_dir.mkdir()
            
            if self.coverage_dir.exists():
                shutil.rmtree(self.coverage_dir)
                self.coverage_dir.mkdir()
            
            # Remove coverage files
            for file in ["coverage.xml", ".coverage"]:
                file_path = self.project_root / file
                if file_path.exists():
                    file_path.unlink()
            
            print("✅ Reports cleaned successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to clean reports: {e}")
            return False
    
    def _run_command(self, cmd, description, check=True):
        """Run a command and handle errors"""
        try:
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=check, cwd=self.project_root, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {description} completed successfully")
                if result.stdout:
                    print(result.stdout)
                return True
            else:
                print(f"❌ {description} failed with return code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                if result.stdout:
                    print(f"Output: {result.stdout}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ Command not found for {description}")
            return False
    
    def _check_server_running(self):
        """Check if the Flask server is running"""
        import requests
        
        try:
            response = requests.get("http://127.0.0.1:5001", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _start_server(self):
        """Start the Flask server for E2E tests"""
        try:
            # Start server in background
            subprocess.Popen([sys.executable, "app.py"], cwd=self.project_root)
            
            # Wait for server to start
            for _ in range(30):  # Wait up to 30 seconds
                if self._check_server_running():
                    print("✅ Server started successfully")
                    return True
                time.sleep(1)
            
            print("❌ Server failed to start within timeout")
            return False
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False


def main():
    """Main function to run tests based on command line arguments"""
    parser = argparse.ArgumentParser(description="Test runner for Administrative Health Record Management System")
    
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests only")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--security", action="store_true", help="Run security tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report only")
    parser.add_argument("--clean", action="store_true", help="Clean old reports")
    parser.add_argument("--install", action="store_true", help="Install test dependencies")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    # If no specific test type is specified, run all tests
    if not any([args.unit, args.integration, args.e2e, args.smoke, 
                args.security, args.performance, args.coverage, args.clean, args.install]):
        args.all = True
    
    success = True
    
    if args.install:
        success &= runner.install_dependencies()
    
    if args.clean:
        success &= runner.clean_reports()
    
    if args.unit:
        success &= runner.run_unit_tests()
    
    if args.integration:
        success &= runner.run_integration_tests()
    
    if args.e2e:
        success &= runner.run_e2e_tests()
    
    if args.smoke:
        success &= runner.run_smoke_tests()
    
    if args.security:
        success &= runner.run_security_tests()
    
    if args.performance:
        success &= runner.run_performance_tests()
    
    if args.all:
        success &= runner.run_all_tests()
    
    if args.coverage or args.all:
        success &= runner.generate_coverage_report()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print(f"📊 Reports available in: {runner.reports_dir}")
        print(f"📈 Coverage report: {runner.coverage_dir}/index.html")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
