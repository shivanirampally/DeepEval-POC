from providers.gemini_provider import GeminiProvider
from exceptions.exception_handler import ExceptionHandler

from config.settings import MAX_TEST_CASES


class AIEvaluationService:
    """
    Generates AI responses for the test dataset.
    """

    @staticmethod
    def run(dataframe):

        provider = GeminiProvider()

        success_count = 0
        failed_count = 0

        total_test_cases = len(dataframe)
        test_cases_to_process = min(
            total_test_cases,
            MAX_TEST_CASES
        )

        rows_to_process = dataframe.head(MAX_TEST_CASES)

        print("\n===== Generating AI Responses =====\n")
        print(f"Dataset Size           : {total_test_cases}")
        print(f"Configured Execution   : {test_cases_to_process}\n")

        for index, row in rows_to_process.iterrows():

            print(f"Processing Test Case {row['ID']}...")

            attempt = 1

            while True:

                try:

                    response = provider.generate_response(
                        row["Input"]
                    )

                    dataframe.at[index, "AI_Response"] = response
                    dataframe.at[index, "Result"] = "Completed"
                    dataframe.at[index, "Remarks"] = ""

                    success_count += 1

                    print("✓ Completed")

                    break

                except Exception as error:

                    result = ExceptionHandler.handle(
                        error,
                        attempt
                    )

                    action = result["action"]
                    remarks = result["remarks"]

                    if action == "retry":

                        attempt += 1
                        continue

                    dataframe.at[index, "AI_Response"] = ""
                    dataframe.at[index, "Remarks"] = remarks

                    if action == "stop":

                        dataframe.at[index, "Result"] = "Skipped"

                        failed_count += 1

                        remaining = (
                            test_cases_to_process
                            - success_count
                            - failed_count
                        )

                        print("\nExecution stopped.")
                        print(f"Reason : {remarks}")

                        print("\n========== Execution Summary ==========")
                        print(f"Dataset Size           : {total_test_cases}")
                        print(f"Configured Execution   : {test_cases_to_process}")
                        print(f"Processed Successfully : {success_count}")
                        print(f"Failed                 : {failed_count}")
                        print(f"Remaining Not Processed: {remaining}")
                        print("=======================================\n")

                        return dataframe

                    dataframe.at[index, "Result"] = "Failed"

                    failed_count += 1

                    print(f"✗ {remarks}")

                    break

        remaining = (
            test_cases_to_process
            - success_count
            - failed_count
        )

        print("\n========== Execution Summary ==========")
        print(f"Dataset Size           : {total_test_cases}")
        print(f"Configured Execution   : {test_cases_to_process}")
        print(f"Processed Successfully : {success_count}")
        print(f"Failed                 : {failed_count}")
        print(f"Remaining Not Processed: {remaining}")
        print("=======================================\n")

        return dataframe