from utils.framework_logger import print_banner

from utils.report_generator import (
    generate_excel_report,
    results_data,
)


def pytest_sessionstart(session):
    print_banner()


def pytest_sessionfinish(session, exitstatus):

    print("\nExecution Summary")
    print("-" * 70)

    total = session.testscollected
    completed = len(results_data)
    skipped = total - completed

    print(f"Total Test Cases : {total}")
    print(f"Completed        : {completed}")
    print(f"Skipped          : {skipped}")

    report_path = generate_excel_report(results_data)

    print("\nReport Location")
    print("-" * 70)
    print(report_path)