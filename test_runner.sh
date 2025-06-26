#!/bin/bash

# Test Runner Script for Administrative Health Record Management System
# This script provides easy commands to run different types of tests

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="$PROJECT_ROOT/reports"
COVERAGE_DIR="$PROJECT_ROOT/htmlcov"

# Ensure directories exist
mkdir -p "$REPORTS_DIR"
mkdir -p "$COVERAGE_DIR"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    print_status "Using Python: $(python3 --version)"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing test dependencies..."
    
    if [ -f "tests/requirements.txt" ]; then
        python3 -m pip install -r tests/requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_warning "tests/requirements.txt not found, skipping dependency installation"
    fi
}

# Function to check if server is running
check_server() {
    if curl -s http://127.0.0.1:5001 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start server
start_server() {
    print_status "Starting Flask server..."
    
    if check_server; then
        print_warning "Server is already running"
        return 0
    fi
    
    # Start server in background
    python3 app.py &
    SERVER_PID=$!
    
    # Wait for server to start
    for i in {1..30}; do
        if check_server; then
            print_success "Server started successfully (PID: $SERVER_PID)"
            return 0
        fi
        sleep 1
    done
    
    print_error "Failed to start server within 30 seconds"
    return 1
}

# Function to stop server
stop_server() {
    if [ ! -z "$SERVER_PID" ]; then
        print_status "Stopping server (PID: $SERVER_PID)..."
        kill $SERVER_PID 2>/dev/null || true
        wait $SERVER_PID 2>/dev/null || true
        print_success "Server stopped"
    fi
}

# Function to run unit tests
run_unit_tests() {
    print_status "Running Unit Tests..."
    
    python3 -m pytest tests/unit/ \
        -v \
        --tb=short \
        --cov=package \
        --cov-report=term-missing \
        --cov-report=html:htmlcov/unit \
        --html=reports/unit_tests.html \
        --self-contained-html \
        -m "unit or not (integration or e2e)"
    
    if [ $? -eq 0 ]; then
        print_success "Unit tests completed successfully"
        return 0
    else
        print_error "Unit tests failed"
        return 1
    fi
}

# Function to run integration tests
run_integration_tests() {
    print_status "Running Integration Tests..."
    
    python3 -m pytest tests/integration/ \
        -v \
        --tb=short \
        --cov=package \
        --cov-append \
        --cov-report=term-missing \
        --cov-report=html:htmlcov/integration \
        --html=reports/integration_tests.html \
        --self-contained-html \
        -m "integration or not (unit or e2e)"
    
    if [ $? -eq 0 ]; then
        print_success "Integration tests completed successfully"
        return 0
    else
        print_error "Integration tests failed"
        return 1
    fi
}

# Function to run E2E tests
run_e2e_tests() {
    print_status "Running End-to-End Tests..."
    
    # Check if server is running, start if needed
    if ! check_server; then
        start_server
        if [ $? -ne 0 ]; then
            print_error "Cannot run E2E tests without server"
            return 1
        fi
        STARTED_SERVER=true
    fi
    
    python3 -m pytest tests/e2e/ \
        -v \
        --tb=short \
        --html=reports/e2e_tests.html \
        --self-contained-html \
        -m "e2e or not (unit or integration)"
    
    local exit_code=$?
    
    # Stop server if we started it
    if [ "$STARTED_SERVER" = true ]; then
        stop_server
    fi
    
    if [ $exit_code -eq 0 ]; then
        print_success "End-to-End tests completed successfully"
        return 0
    else
        print_error "End-to-End tests failed"
        return 1
    fi
}

# Function to run all tests
run_all_tests() {
    print_status "Running All Tests..."
    
    python3 -m pytest tests/ \
        -v \
        --tb=short \
        --cov=package \
        --cov=app \
        --cov-report=term-missing \
        --cov-report=html:htmlcov \
        --cov-report=xml:coverage.xml \
        --cov-fail-under=80 \
        --html=reports/all_tests.html \
        --self-contained-html \
        --junitxml=reports/junit.xml
    
    if [ $? -eq 0 ]; then
        print_success "All tests completed successfully"
        return 0
    else
        print_error "Some tests failed"
        return 1
    fi
}

# Function to run security tests
run_security_tests() {
    print_status "Running Security Tests..."
    
    # Run Bandit security analysis
    print_status "Running Bandit security analysis..."
    python3 -m bandit -r package/ app.py -f json -o reports/bandit_report.json || true
    
    # Run security-marked tests
    python3 -m pytest tests/ \
        -v \
        --tb=short \
        -m "security" \
        --html=reports/security_tests.html \
        --self-contained-html
    
    print_success "Security tests completed"
}

# Function to generate coverage report
generate_coverage_report() {
    print_status "Generating Coverage Report..."
    
    # Generate HTML coverage report
    python3 -m coverage html -d htmlcov
    
    # Generate XML coverage report
    python3 -m coverage xml -o coverage.xml
    
    # Generate terminal report
    python3 -m coverage report --show-missing
    
    print_success "Coverage report generated at htmlcov/index.html"
}

# Function to clean reports
clean_reports() {
    print_status "Cleaning old reports..."
    
    rm -rf "$REPORTS_DIR"/*
    rm -rf "$COVERAGE_DIR"/*
    rm -f coverage.xml .coverage
    
    print_success "Reports cleaned successfully"
}

# Function to show help
show_help() {
    echo "Test Runner for Administrative Health Record Management System"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  unit          Run unit tests only"
    echo "  integration   Run integration tests only"
    echo "  e2e           Run end-to-end tests only"
    echo "  all           Run all tests (default)"
    echo "  security      Run security tests"
    echo "  coverage      Generate coverage report only"
    echo "  clean         Clean old reports"
    echo "  install       Install test dependencies"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 unit                 # Run only unit tests"
    echo "  $0 all                  # Run all tests with coverage"
    echo "  $0 clean && $0 all      # Clean and run all tests"
    echo ""
}

# Main execution
main() {
    cd "$PROJECT_ROOT"
    
    # Check Python availability
    check_python
    
    # Parse command line arguments
    case "${1:-all}" in
        "unit")
            run_unit_tests
            ;;
        "integration")
            run_integration_tests
            ;;
        "e2e")
            run_e2e_tests
            ;;
        "all")
            run_all_tests
            generate_coverage_report
            ;;
        "security")
            run_security_tests
            ;;
        "coverage")
            generate_coverage_report
            ;;
        "clean")
            clean_reports
            ;;
        "install")
            install_dependencies
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        print_success "Test execution completed successfully!"
        echo ""
        echo "📊 Reports available in: $REPORTS_DIR"
        echo "📈 Coverage report: $COVERAGE_DIR/index.html"
    else
        print_error "Test execution failed!"
        exit 1
    fi
}

# Trap to ensure server is stopped on script exit
trap 'stop_server' EXIT

# Run main function
main "$@"
