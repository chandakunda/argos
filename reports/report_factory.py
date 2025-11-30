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
