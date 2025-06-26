#!/usr/bin/env python3
"""
Test report generator for Administrative Health Record Management System
"""

import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import subprocess
import sys


class TestReportGenerator:
    """Generate comprehensive test reports"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.coverage_dir = self.project_root / "htmlcov"
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.coverage_dir.mkdir(exist_ok=True)
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive test report"""
        print("📊 Generating Comprehensive Test Report...")
        
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "project": "Administrative Health Record Management System",
            "test_summary": self._get_test_summary(),
            "coverage_summary": self._get_coverage_summary(),
            "test_results": self._get_test_results(),
            "security_analysis": self._get_security_analysis(),
            "recommendations": self._get_recommendations()
        }
        
        # Generate JSON report
        json_report_path = self.reports_dir / "comprehensive_test_report.json"
        with open(json_report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate Markdown report
        markdown_report_path = self.reports_dir / "COMPREHENSIVE_TEST_REPORT.md"
        self._generate_markdown_report(report_data, markdown_report_path)
        
        print(f"✅ Comprehensive report generated:")
        print(f"   📄 JSON: {json_report_path}")
        print(f"   📝 Markdown: {markdown_report_path}")
        
        return report_data
    
    def _get_test_summary(self):
        """Get test execution summary"""
        summary = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "execution_time": "0s"
        }
        
        # Try to parse JUnit XML report
        junit_path = self.reports_dir / "junit.xml"
        if junit_path.exists():
            try:
                tree = ET.parse(junit_path)
                root = tree.getroot()
                
                summary["total_tests"] = int(root.get("tests", 0))
                summary["failed"] = int(root.get("failures", 0))
                summary["errors"] = int(root.get("errors", 0))
                summary["skipped"] = int(root.get("skipped", 0))
                summary["passed"] = summary["total_tests"] - summary["failed"] - summary["errors"] - summary["skipped"]
                summary["execution_time"] = root.get("time", "0s")
                
            except Exception as e:
                print(f"Warning: Could not parse JUnit report: {e}")
        
        return summary
    
    def _get_coverage_summary(self):
        """Get code coverage summary"""
        coverage_summary = {
            "total_coverage": 0,
            "line_coverage": 0,
            "branch_coverage": 0,
            "files_covered": 0,
            "lines_covered": 0,
            "lines_total": 0
        }
        
        # Try to parse coverage XML report
        coverage_xml_path = self.project_root / "coverage.xml"
        if coverage_xml_path.exists():
            try:
                tree = ET.parse(coverage_xml_path)
                root = tree.getroot()
                
                # Get overall coverage
                for coverage_elem in root.findall(".//coverage"):
                    coverage_summary["line_coverage"] = float(coverage_elem.get("line-rate", 0)) * 100
                    coverage_summary["branch_coverage"] = float(coverage_elem.get("branch-rate", 0)) * 100
                    coverage_summary["total_coverage"] = coverage_summary["line_coverage"]
                
                # Count files and lines
                packages = root.findall(".//package")
                for package in packages:
                    classes = package.findall(".//class")
                    coverage_summary["files_covered"] += len(classes)
                    
                    for class_elem in classes:
                        lines = class_elem.findall(".//line")
                        coverage_summary["lines_total"] += len(lines)
                        coverage_summary["lines_covered"] += len([l for l in lines if l.get("hits", "0") != "0"])
                
            except Exception as e:
                print(f"Warning: Could not parse coverage report: {e}")
        
        return coverage_summary
    
    def _get_test_results(self):
        """Get detailed test results by category"""
        results = {
            "unit_tests": {"status": "unknown", "count": 0, "passed": 0, "failed": 0},
            "integration_tests": {"status": "unknown", "count": 0, "passed": 0, "failed": 0},
            "e2e_tests": {"status": "unknown", "count": 0, "passed": 0, "failed": 0},
            "security_tests": {"status": "unknown", "count": 0, "passed": 0, "failed": 0}
        }
        
        # Check for individual test reports
        test_reports = {
            "unit_tests": "unit_tests.html",
            "integration_tests": "integration_tests.html",
            "e2e_tests": "e2e_tests.html",
            "security_tests": "security_tests.html"
        }
        
        for test_type, report_file in test_reports.items():
            report_path = self.reports_dir / report_file
            if report_path.exists():
                results[test_type]["status"] = "completed"
                # Could parse HTML reports for more detailed info
            else:
                results[test_type]["status"] = "not_run"
        
        return results
    
    def _get_security_analysis(self):
        """Get security analysis results"""
        security_analysis = {
            "bandit_scan": {"status": "not_run", "issues": []},
            "dependency_check": {"status": "not_run", "vulnerabilities": []},
            "security_tests": {"status": "not_run", "passed": 0, "failed": 0}
        }
        
        # Check for Bandit report
        bandit_report_path = self.reports_dir / "bandit_report.json"
        if bandit_report_path.exists():
            try:
                with open(bandit_report_path, 'r') as f:
                    bandit_data = json.load(f)
                
                security_analysis["bandit_scan"]["status"] = "completed"
                security_analysis["bandit_scan"]["issues"] = bandit_data.get("results", [])
                
            except Exception as e:
                print(f"Warning: Could not parse Bandit report: {e}")
        
        return security_analysis
    
    def _get_recommendations(self):
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Get test and coverage data
        test_summary = self._get_test_summary()
        coverage_summary = self._get_coverage_summary()
        
        # Coverage recommendations
        if coverage_summary["total_coverage"] < 80:
            recommendations.append({
                "category": "Coverage",
                "priority": "High",
                "issue": f"Code coverage is {coverage_summary['total_coverage']:.1f}%, below the 80% target",
                "recommendation": "Add more unit tests to increase code coverage, focusing on untested modules"
            })
        elif coverage_summary["total_coverage"] < 90:
            recommendations.append({
                "category": "Coverage",
                "priority": "Medium",
                "issue": f"Code coverage is {coverage_summary['total_coverage']:.1f}%, good but could be improved",
                "recommendation": "Consider adding edge case tests and integration tests"
            })
        
        # Test failure recommendations
        if test_summary["failed"] > 0:
            recommendations.append({
                "category": "Test Failures",
                "priority": "High",
                "issue": f"{test_summary['failed']} tests are failing",
                "recommendation": "Fix failing tests before deployment. Review test logs for specific issues"
            })
        
        # Test count recommendations
        if test_summary["total_tests"] < 50:
            recommendations.append({
                "category": "Test Count",
                "priority": "Medium",
                "issue": f"Only {test_summary['total_tests']} tests found, may not be sufficient",
                "recommendation": "Consider adding more comprehensive test cases for all modules"
            })
        
        # Security recommendations
        security_analysis = self._get_security_analysis()
        if security_analysis["bandit_scan"]["status"] == "not_run":
            recommendations.append({
                "category": "Security",
                "priority": "Medium",
                "issue": "Security analysis not performed",
                "recommendation": "Run security scans using tools like Bandit to identify potential vulnerabilities"
            })
        
        # Performance recommendations
        recommendations.append({
            "category": "Performance",
            "priority": "Low",
            "issue": "Performance testing not implemented",
            "recommendation": "Add performance tests to ensure API response times meet requirements"
        })
        
        return recommendations
    
    def _generate_markdown_report(self, report_data, output_path):
        """Generate a Markdown test report"""
        
        markdown_content = f"""# 🧪 Comprehensive Test Report

**Generated:** {report_data['generated_at']}  
**Project:** {report_data['project']}

## 📊 Test Summary

| Metric | Value |
|--------|-------|
| Total Tests | {report_data['test_summary']['total_tests']} |
| Passed | ✅ {report_data['test_summary']['passed']} |
| Failed | ❌ {report_data['test_summary']['failed']} |
| Skipped | ⏭️ {report_data['test_summary']['skipped']} |
| Errors | 🚨 {report_data['test_summary']['errors']} |
| Execution Time | ⏱️ {report_data['test_summary']['execution_time']} |

## 📈 Coverage Summary

| Metric | Value |
|--------|-------|
| Total Coverage | {report_data['coverage_summary']['total_coverage']:.1f}% |
| Line Coverage | {report_data['coverage_summary']['line_coverage']:.1f}% |
| Branch Coverage | {report_data['coverage_summary']['branch_coverage']:.1f}% |
| Files Covered | {report_data['coverage_summary']['files_covered']} |
| Lines Covered | {report_data['coverage_summary']['lines_covered']} / {report_data['coverage_summary']['lines_total']} |

## 🧪 Test Results by Category

### Unit Tests
- **Status:** {report_data['test_results']['unit_tests']['status']}
- **Count:** {report_data['test_results']['unit_tests']['count']}
- **Passed:** {report_data['test_results']['unit_tests']['passed']}
- **Failed:** {report_data['test_results']['unit_tests']['failed']}

### Integration Tests
- **Status:** {report_data['test_results']['integration_tests']['status']}
- **Count:** {report_data['test_results']['integration_tests']['count']}
- **Passed:** {report_data['test_results']['integration_tests']['passed']}
- **Failed:** {report_data['test_results']['integration_tests']['failed']}

### End-to-End Tests
- **Status:** {report_data['test_results']['e2e_tests']['status']}
- **Count:** {report_data['test_results']['e2e_tests']['count']}
- **Passed:** {report_data['test_results']['e2e_tests']['passed']}
- **Failed:** {report_data['test_results']['e2e_tests']['failed']}

### Security Tests
- **Status:** {report_data['test_results']['security_tests']['status']}
- **Count:** {report_data['test_results']['security_tests']['count']}
- **Passed:** {report_data['test_results']['security_tests']['passed']}
- **Failed:** {report_data['test_results']['security_tests']['failed']}

## 🔒 Security Analysis

### Bandit Scan
- **Status:** {report_data['security_analysis']['bandit_scan']['status']}
- **Issues Found:** {len(report_data['security_analysis']['bandit_scan']['issues'])}

### Dependency Check
- **Status:** {report_data['security_analysis']['dependency_check']['status']}
- **Vulnerabilities:** {len(report_data['security_analysis']['dependency_check']['vulnerabilities'])}

## 💡 Recommendations

"""
        
        for i, rec in enumerate(report_data['recommendations'], 1):
            priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(rec['priority'], "⚪")
            markdown_content += f"""### {i}. {rec['category']} {priority_emoji}

**Priority:** {rec['priority']}  
**Issue:** {rec['issue']}  
**Recommendation:** {rec['recommendation']}

"""
        
        markdown_content += f"""## 📁 Report Files

- **HTML Coverage Report:** `htmlcov/index.html`
- **XML Coverage Report:** `coverage.xml`
- **JUnit Test Report:** `reports/junit.xml`
- **HTML Test Reports:** `reports/`
- **JSON Report:** `reports/comprehensive_test_report.json`

## 🚀 Next Steps

1. **Address High Priority Issues:** Focus on fixing failing tests and improving coverage
2. **Review Security Findings:** Investigate and resolve any security vulnerabilities
3. **Enhance Test Suite:** Add more comprehensive tests for better coverage
4. **Automate Testing:** Integrate tests into CI/CD pipeline
5. **Monitor Performance:** Add performance benchmarks and monitoring

---

**Report Generated by:** Administrative Health Record Management System Test Suite  
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def generate_coverage_badge(self):
        """Generate a coverage badge"""
        coverage_summary = self._get_coverage_summary()
        coverage_percent = coverage_summary["total_coverage"]
        
        # Determine badge color
        if coverage_percent >= 90:
            color = "brightgreen"
        elif coverage_percent >= 80:
            color = "green"
        elif coverage_percent >= 70:
            color = "yellow"
        elif coverage_percent >= 60:
            color = "orange"
        else:
            color = "red"
        
        badge_url = f"https://img.shields.io/badge/coverage-{coverage_percent:.1f}%25-{color}"
        
        badge_markdown = f"![Coverage Badge]({badge_url})"
        
        badge_file = self.reports_dir / "coverage_badge.md"
        with open(badge_file, 'w', encoding='utf-8') as f:
            f.write(badge_markdown)
        
        print(f"📛 Coverage badge generated: {badge_file}")
        return badge_url


def main():
    """Main function to generate test reports"""
    generator = TestReportGenerator()
    
    print("🎯 Generating Test Reports...")
    
    # Generate comprehensive report
    report_data = generator.generate_comprehensive_report()
    
    # Generate coverage badge
    badge_url = generator.generate_coverage_badge()
    
    print("\n✅ Test report generation completed!")
    print(f"📊 Coverage: {report_data['coverage_summary']['total_coverage']:.1f}%")
    print(f"🧪 Tests: {report_data['test_summary']['passed']}/{report_data['test_summary']['total_tests']} passed")
    
    if report_data['test_summary']['failed'] > 0:
        print(f"❌ {report_data['test_summary']['failed']} tests failed - review and fix")
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
