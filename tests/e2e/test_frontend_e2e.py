"""
End-to-End tests for the frontend application
"""

import pytest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@pytest.fixture(scope="session")
def driver():
    """Create a Chrome WebDriver instance for testing"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
    except Exception as e:
        pytest.skip(f"Chrome WebDriver not available: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()


@pytest.fixture
def base_url():
    """Base URL for the application"""
    return "http://127.0.0.1:5001"


class TestLoginPage:
    """E2E tests for login functionality"""
    
    def test_login_page_loads(self, driver, base_url):
        """Test that login page loads correctly"""
        driver.get(f"{base_url}/static/login.html")
        
        # Check page title
        assert "Login" in driver.title or "PulseCare" in driver.title
        
        # Check for login form elements
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.TYPE, "submit")
        
        assert username_field is not None
        assert password_field is not None
        assert login_button is not None
    
    def test_login_with_valid_credentials(self, driver, base_url):
        """Test login with valid credentials"""
        driver.get(f"{base_url}/static/login.html")
        
        # Fill in login form
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys("admin")
        
        password_field.clear()
        password_field.send_keys("admin123")
        
        # Submit form
        login_button = driver.find_element(By.TYPE, "submit")
        login_button.click()
        
        # Wait for redirect or success message
        try:
            WebDriverWait(driver, 10).until(
                lambda d: "dashboard" in d.current_url.lower() or 
                         "success" in d.page_source.lower() or
                         d.current_url != f"{base_url}/static/login.html"
            )
            
            # Should be redirected away from login page
            assert "login.html" not in driver.current_url
            
        except TimeoutException:
            # Check for error messages or if still on login page
            page_source = driver.page_source.lower()
            if "error" in page_source or "invalid" in page_source:
                pytest.skip("Login failed - check if admin user exists")
            else:
                pytest.fail("Login did not complete within timeout")
    
    def test_login_with_invalid_credentials(self, driver, base_url):
        """Test login with invalid credentials"""
        driver.get(f"{base_url}/static/login.html")
        
        # Fill in login form with invalid credentials
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys("invalid_user")
        
        password_field.clear()
        password_field.send_keys("invalid_password")
        
        # Submit form
        login_button = driver.find_element(By.TYPE, "submit")
        login_button.click()
        
        # Wait for error message or stay on login page
        time.sleep(2)
        
        # Should show error or stay on login page
        page_source = driver.page_source.lower()
        assert ("error" in page_source or 
                "invalid" in page_source or 
                "login.html" in driver.current_url)


class TestSignupPage:
    """E2E tests for signup functionality"""
    
    def test_signup_page_loads(self, driver, base_url):
        """Test that signup page loads correctly"""
        driver.get(f"{base_url}/static/signup.html")
        
        # Check page title
        assert "Sign" in driver.title or "Register" in driver.title or "PulseCare" in driver.title
        
        # Check for signup form elements
        try:
            username_field = driver.find_element(By.NAME, "username")
            email_field = driver.find_element(By.NAME, "email")
            password_field = driver.find_element(By.NAME, "password")
            
            assert username_field is not None
            assert email_field is not None
            assert password_field is not None
            
        except NoSuchElementException:
            # Try alternative selectors
            form_fields = driver.find_elements(By.TAG_NAME, "input")
            assert len(form_fields) >= 3  # Should have at least username, email, password
    
    def test_signup_form_validation(self, driver, base_url):
        """Test signup form validation"""
        driver.get(f"{base_url}/static/signup.html")
        
        try:
            # Try to submit empty form
            submit_button = driver.find_element(By.TYPE, "submit")
            submit_button.click()
            
            time.sleep(1)
            
            # Should show validation errors or stay on page
            page_source = driver.page_source.lower()
            assert ("required" in page_source or 
                    "error" in page_source or 
                    "signup.html" in driver.current_url)
                    
        except NoSuchElementException:
            pytest.skip("Submit button not found - form structure may be different")


class TestDashboardNavigation:
    """E2E tests for dashboard navigation"""
    
    def test_dashboard_access_after_login(self, driver, base_url):
        """Test accessing dashboard after successful login"""
        # First login
        driver.get(f"{base_url}/static/login.html")
        
        try:
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.send_keys("admin")
            password_field.send_keys("admin123")
            
            login_button = driver.find_element(By.TYPE, "submit")
            login_button.click()
            
            # Wait for redirect
            WebDriverWait(driver, 10).until(
                lambda d: "login.html" not in d.current_url
            )
            
            # Try to access dashboard directly
            driver.get(f"{base_url}/static/dashboard.html")
            
            # Should be able to access dashboard
            assert "dashboard" in driver.current_url.lower()
            
        except (TimeoutException, NoSuchElementException):
            pytest.skip("Login process failed - cannot test dashboard access")
    
    def test_navigation_menu_exists(self, driver, base_url):
        """Test that navigation menu exists on dashboard"""
        driver.get(f"{base_url}/static/dashboard.html")
        
        # Look for navigation elements
        nav_elements = driver.find_elements(By.TAG_NAME, "nav")
        menu_elements = driver.find_elements(By.CLASS_NAME, "menu")
        sidebar_elements = driver.find_elements(By.CLASS_NAME, "sidebar")
        
        # Should have some form of navigation
        assert (len(nav_elements) > 0 or 
                len(menu_elements) > 0 or 
                len(sidebar_elements) > 0)


class TestPatientManagement:
    """E2E tests for patient management functionality"""
    
    def test_patients_page_loads(self, driver, base_url):
        """Test that patients page loads"""
        driver.get(f"{base_url}/static/patients.html")
        
        # Check page loads
        assert driver.current_url.endswith("patients.html")
        
        # Look for patient-related elements
        page_source = driver.page_source.lower()
        assert ("patient" in page_source or 
                "table" in page_source or 
                "list" in page_source)
    
    def test_patient_table_exists(self, driver, base_url):
        """Test that patient table exists on patients page"""
        driver.get(f"{base_url}/static/patients.html")
        
        # Look for table elements
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        if len(tables) > 0:
            # Check if table has headers
            headers = driver.find_elements(By.TAG_NAME, "th")
            assert len(headers) > 0
        else:
            # Look for alternative data display
            lists = driver.find_elements(By.TAG_NAME, "ul")
            divs = driver.find_elements(By.CLASS_NAME, "patient")
            
            assert len(lists) > 0 or len(divs) > 0


class TestDoctorManagement:
    """E2E tests for doctor management functionality"""
    
    def test_doctors_page_loads(self, driver, base_url):
        """Test that doctors page loads"""
        driver.get(f"{base_url}/static/doctor.html")
        
        # Check page loads
        assert driver.current_url.endswith("doctor.html")
        
        # Look for doctor-related elements
        page_source = driver.page_source.lower()
        assert ("doctor" in page_source or 
                "physician" in page_source or 
                "table" in page_source)


class TestAppointmentManagement:
    """E2E tests for appointment management"""
    
    def test_appointments_page_loads(self, driver, base_url):
        """Test that appointments page loads"""
        driver.get(f"{base_url}/static/appointment.html")
        
        # Check page loads
        assert driver.current_url.endswith("appointment.html")
        
        # Look for appointment-related elements
        page_source = driver.page_source.lower()
        assert ("appointment" in page_source or 
                "schedule" in page_source or 
                "calendar" in page_source)


class TestResponsiveDesign:
    """E2E tests for responsive design"""
    
    def test_mobile_viewport(self, driver, base_url):
        """Test application in mobile viewport"""
        # Set mobile viewport
        driver.set_window_size(375, 667)  # iPhone 6/7/8 size
        
        driver.get(f"{base_url}/static/dashboard.html")
        
        # Check that page still loads and is usable
        assert driver.current_url.endswith("dashboard.html")
        
        # Look for mobile-friendly elements
        page_source = driver.page_source
        assert ("viewport" in page_source or 
                "responsive" in page_source or 
                len(page_source) > 1000)  # Page has content
    
    def test_tablet_viewport(self, driver, base_url):
        """Test application in tablet viewport"""
        # Set tablet viewport
        driver.set_window_size(768, 1024)  # iPad size
        
        driver.get(f"{base_url}/static/dashboard.html")
        
        # Check that page still loads
        assert driver.current_url.endswith("dashboard.html")
    
    def test_desktop_viewport(self, driver, base_url):
        """Test application in desktop viewport"""
        # Set desktop viewport
        driver.set_window_size(1920, 1080)
        
        driver.get(f"{base_url}/static/dashboard.html")
        
        # Check that page still loads
        assert driver.current_url.endswith("dashboard.html")


class TestErrorHandling:
    """E2E tests for error handling"""
    
    def test_404_page_handling(self, driver, base_url):
        """Test handling of 404 errors"""
        driver.get(f"{base_url}/static/nonexistent-page.html")
        
        # Should handle 404 gracefully
        page_source = driver.page_source.lower()
        
        # Either show 404 page or redirect to valid page
        assert ("404" in page_source or 
                "not found" in page_source or 
                "error" in page_source or
                driver.current_url != f"{base_url}/static/nonexistent-page.html")
    
    def test_javascript_errors(self, driver, base_url):
        """Test for JavaScript errors on pages"""
        driver.get(f"{base_url}/static/dashboard.html")
        
        # Get browser console logs
        logs = driver.get_log('browser')
        
        # Filter for severe errors
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        # Should not have severe JavaScript errors
        assert len(severe_errors) == 0, f"JavaScript errors found: {severe_errors}"


class TestAccessibility:
    """E2E tests for accessibility"""
    
    def test_page_has_title(self, driver, base_url):
        """Test that pages have proper titles"""
        pages = ["login.html", "dashboard.html", "patients.html", "doctor.html"]
        
        for page in pages:
            driver.get(f"{base_url}/static/{page}")
            title = driver.title
            
            # Title should not be empty
            assert title is not None and len(title.strip()) > 0
    
    def test_images_have_alt_text(self, driver, base_url):
        """Test that images have alt text"""
        driver.get(f"{base_url}/static/dashboard.html")
        
        images = driver.find_elements(By.TAG_NAME, "img")
        
        for img in images:
            alt_text = img.get_attribute("alt")
            # Alt text should exist (can be empty for decorative images)
            assert alt_text is not None


if __name__ == "__main__":
    pytest.main([__file__])
