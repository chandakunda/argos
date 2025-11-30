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
