from utils.report_generator import (
    generate_excel_report,
    results_data
)

def pytest_sessionfinish(session, exitstatus):
    print("\nGenerating Excel Report...")
    generate_excel_report(results_data)