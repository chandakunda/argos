#!/usr/bin/env bash
set -e

echo "=== PHASE 8: REPORTING SYSTEM (FULL AUTOMATION) ==="

mkdir -p reports
mkdir -p reports/base
mkdir -p reports/implementations
mkdir -p reports/outputs
mkdir -p tests/reports

##########################################
# 1. BASE REPORT INTERFACE + ENUMS
##########################################
echo "--- Creating base report interface ---"

cat << 'PYEOF' > reports/base/base_report.py
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict

class ReportFormat(Enum):
    JSON = "json"
    CSV = "csv"

class ReportScope(Enum):
    GLOBAL = "global"
    COURSE = "course"
    USER = "user"

class Reportable(ABC):
    """
    Base report interface.
    """

    @abstractmethod
    def generate(self, format: ReportFormat, scope: ReportScope) -> Any:
        pass
PYEOF

##########################################
# 2. ADMIN SUMMARY REPORT
##########################################
echo "--- Creating AdminSummaryReport ---"

cat << 'PYEOF' > reports/implementations/admin_summary_report.py
import json
import csv
from io import StringIO
from reports.base.base_report import Reportable, ReportFormat, ReportScope

class AdminSummaryReport(Reportable):
    """
    High-level summary for system administrators.
    """

    def __init__(self, stats: dict):
        self.stats = stats

    def generate(self, format: ReportFormat, scope: ReportScope):
        if format == ReportFormat.JSON:
            return json.dumps(self.stats, indent=4)

        if format == ReportFormat.CSV:
            output = StringIO()
            writer = csv.writer(output)
            for k, v in self.stats.items():
                writer.writerow([k, v])
            return output.getvalue()

        raise ValueError("Unsupported format")
PYEOF

##########################################
# 3. LECTURER COURSE PERFORMANCE REPORT
##########################################
echo "--- Creating LecturerCoursePerformanceReport ---"

cat << 'PYEOF' > reports/implementations/lecturer_course_performance_report.py
import json
import csv
from io import StringIO
from reports.base.base_report import Reportable, ReportFormat, ReportScope

class LecturerCoursePerformanceReport(Reportable):
    """
    Report for lecturers showing grade distributions, dropout rates, etc.
    """

    def __init__(self, course_id: str, stats: dict):
        self.course_id = course_id
        self.stats = stats

    def generate(self, format: ReportFormat, scope: ReportScope):
        data = {
            "course_id": self.course_id,
            "metrics": self.stats
        }

        if format == ReportFormat.JSON:
            return json.dumps(data, indent=4)

        if format == ReportFormat.CSV:
            output = StringIO()
            writer = csv.writer(output)
            for k, v in self.stats.items():
                writer.writerow([k, v])
            return output.getvalue()

        raise ValueError("Unsupported format")
PYEOF

##########################################
# 4. COMPLIANCE AUDIT REPORT
##########################################
echo "--- Creating ComplianceAuditReport ---"

cat << 'PYEOF' > reports/implementations/compliance_audit_report.py
import json
import csv
from io import StringIO
from reports.base.base_report import Reportable, ReportFormat, ReportScope

class ComplianceAuditReport(Reportable):
    """
    Security and compliance audit summary report.
    """

    def __init__(self, violations: list, passed: list):
        self.violations = violations
        self.passed = passed

    def generate(self, format: ReportFormat, scope: ReportScope):
        data = {
            "violations": self.violations,
            "checks_passed": self.passed
        }

        if format == ReportFormat.JSON:
            return json.dumps(data, indent=4)

        if format == ReportFormat.CSV:
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["Passed Checks"])
            for p in self.passed:
                writer.writerow([p])
            writer.writerow([])
            writer.writerow(["Violations"])
            for v in self.violations:
                writer.writerow([v])
            return output.getvalue()

        raise ValueError("Unsupported format")
PYEOF

##########################################
# 5. REPORT FACTORY
##########################################
echo "--- Creating ReportFactory ---"

cat << 'PYEOF' > reports/report_factory.py
from reports.implementations.admin_summary_report import AdminSummaryReport
from reports.implementations.lecturer_course_performance_report import LecturerCoursePerformanceReport
from reports.implementations.compliance_audit_report import ComplianceAuditReport

class ReportFactory:
    @staticmethod
    def admin_report(stats: dict):
        return AdminSummaryReport(stats)

    @staticmethod
    def lecturer_report(course_id: str, stats: dict):
        return LecturerCoursePerformanceReport(course_id, stats)

    @staticmethod
    def compliance_report(violations: list, passed: list):
        return ComplianceAuditReport(violations, passed)
PYEOF

##########################################
# 6. SAMPLE GENERATED OUTPUTS
##########################################
echo "--- Writing demo report outputs ---"

cat << 'EOF2' > reports/outputs/admin_demo.json
{
    "total_users": 1200,
    "active_courses": 84,
    "open_incidents": 3
}
EOF2

cat << 'EOF2' > reports/outputs/performance_demo.json
{
    "course_id": "CS101",
    "average_grade": 73.4,
    "dropout_rate": 0.12
}
EOF2

cat << 'EOF2' > reports/outputs/compliance_demo.json
{
    "checks_passed": ["encryption_enabled", "audit_log_hashchain_valid"],
    "violations": ["weak_password_policy"]
}
EOF2

##########################################
# 7. REPORT TEST SUITE
##########################################
echo "--- Creating report test suite ---"

cat << 'PYEOF' > tests/reports/test_reports.py
from reports.report_factory import ReportFactory
from reports.base.base_report import ReportFormat, ReportScope

def test_admin_report_json():
    report = ReportFactory.admin_report({"users": 10})
    output = report.generate(ReportFormat.JSON, ReportScope.GLOBAL)
    assert "users" in output

def test_lecturer_report_csv():
    report = ReportFactory.lecturer_report("CS101", {"avg": 80})
    output = report.generate(ReportFormat.CSV, ReportScope.COURSE)
    assert "avg" in output

def test_compliance_report_json():
    report = ReportFactory.compliance_report(["v1"], ["p1"])
    output = report.generate(ReportFormat.JSON, ReportScope.GLOBAL)
    assert "violations" in output
PYEOF

##########################################
# 8. SUMMARY DOCUMENT
##########################################
echo "--- Writing reporting summary document ---"

cat << 'EOF2' > reports/outputs/reporting_summary.txt
Argos Reporting System — Summary
================================

Reports Implemented:
--------------------
1. AdminSummaryReport
2. LecturerCoursePerformanceReport
3. ComplianceAuditReport

Formats Supported:
------------------
- JSON
- CSV

Features:
---------
- Runtime polymorphism (all reports implement Reportable)
- Factory-based creation
- Easily extensible to new formats (PDF, XML)
- Tests included to validate basic functionality

EOF2

echo "=== PHASE 8 COMPLETE ==="
