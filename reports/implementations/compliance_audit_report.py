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
