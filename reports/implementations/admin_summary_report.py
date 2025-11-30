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
