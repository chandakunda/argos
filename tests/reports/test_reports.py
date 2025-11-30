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
