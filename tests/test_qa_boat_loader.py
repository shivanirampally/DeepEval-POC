from pathlib import Path

from loaders.qa_boat_excel_loader import QABoatExcelLoader


INPUT_FILE = Path(
    "input/qa_boat/DeepEval-login-scenarios-2026-08-17-07-03-32.xlsx"
)


def main():

    print()
    print("=" * 60)
    print("QA BOAT EXCEL LOAD")
    print("=" * 60)

    generated_output = QABoatExcelLoader.load(
        INPUT_FILE
    )

    test_cases = generated_output[
        "testCases"
    ]

    print(
        f"Test Cases Loaded : {len(test_cases)}"
    )

    print()

    task_counts = {}

    for testcase in test_cases:

        task_id = testcase["taskId"]

        task_counts[task_id] = (
            task_counts.get(task_id, 0)
            + 1
        )

    print("Test Cases by Task")
    print("-" * 60)

    for task_id, count in task_counts.items():

        print(
            f"{task_id} → {count}"
        )

    print()

    print("First Test Case")
    print("-" * 60)

    first = test_cases[0]

    print(
        f"ID           : {first['testCaseId']}"
    )

    print(
        f"Title        : {first['testDescription']}"
    )

    print(
        f"Scenario     : {first['scenario']}"
    )

    print(
        f"Preconditions: {first['preconditions']}"
    )

    print(
        f"Steps        : {first['testSteps']}"
    )

    print(
        f"Expected     : {first['expectedResult']}"
    )

    print(
        f"Refs         : {first['refs']}"
    )


if __name__ == "__main__":
    main()