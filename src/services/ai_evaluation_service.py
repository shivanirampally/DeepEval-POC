from providers.gemini_provider import GeminiProvider
from providers.mock_provider import MockProvider
from evaluators.deepeval_runner import DeepEvalRunner
from exceptions.exception_handler import ExceptionHandler

from config.settings import (
    MAX_TEST_CASES,
    USE_MOCK_PROVIDER
)


class AIEvaluationService:
    """
    Generates AI responses and evaluates them using DeepEval.
    """

    @staticmethod
    def run(dataframe):

        # Select Provider
        if USE_MOCK_PROVIDER:
            provider = MockProvider()
            provider_name = "Mock Provider"
        else:
            provider = GeminiProvider()
            provider_name = "Gemini"

        success_count = 0
        failed_count = 0

        total_test_cases = len(dataframe)
        test_cases_to_process = min(
            total_test_cases,
            MAX_TEST_CASES
        )

        rows_to_process = dataframe.head(MAX_TEST_CASES)

        print("\n===== Generating AI Responses =====\n")
        print(f"Provider               : {provider_name}")
        print(f"Dataset Size           : {total_test_cases}")
        print(f"Configured Execution   : {test_cases_to_process}\n")

        for index, row in rows_to_process.iterrows():

            print(f"Processing Test Case {row['ID']}...")

            attempt = 1

            while True:

                try:

                    # Generate AI Response
                    response = provider.generate_response(
                        row["Input"]
                    )

                    # Run DeepEval Evaluation
                    evaluation = DeepEvalRunner.evaluate(
                        prompt=row["Input"],
                        expected_output=row["Expected_Output"],
                        actual_output=response,
                        context=row["Context"]
                    )

                    # Update DataFrame
                    dataframe.at[index, "AI_Response"] = response

                    dataframe.at[
                        index,
                        "Hallucination_Score"
                    ] = evaluation["hallucination_score"]

                    dataframe.at[
                        index,
                        "Answer_Relevancy_Score"
                    ] = evaluation["answer_relevancy_score"]

                    # Placeholder for future GEval implementation
                    if "Correctness_Score" in dataframe.columns:
                        dataframe.at[
                            index,
                            "Correctness_Score"
                        ] = None

                    dataframe.at[
                        index,
                        "Result"
                    ] = evaluation["result"]

                    dataframe.at[
                        index,
                        "Remarks"
                    ] = evaluation["remarks"]

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

                    # Save failure details
                    dataframe.at[index, "AI_Response"] = ""

                    dataframe.at[
                        index,
                        "Hallucination_Score"
                    ] = None

                    dataframe.at[
                        index,
                        "Answer_Relevancy_Score"
                    ] = None

                    if "Correctness_Score" in dataframe.columns:
                        dataframe.at[
                            index,
                            "Correctness_Score"
                        ] = None

                    dataframe.at[
                        index,
                        "Result"
                    ] = "Skipped"

                    dataframe.at[
                        index,
                        "Remarks"
                    ] = remarks

                    failed_count += 1

                    if action == "stop":

                        remaining = (
                            test_cases_to_process
                            - success_count
                            - failed_count
                        )

                        print("\nExecution stopped.")
                        print(f"Reason : {remarks}")

                        print("\n========== Execution Summary ==========")
                        print(f"Provider               : {provider_name}")
                        print(f"Dataset Size           : {total_test_cases}")
                        print(f"Configured Execution   : {test_cases_to_process}")
                        print(f"Processed Successfully : {success_count}")
                        print(f"Failed                 : {failed_count}")
                        print(f"Remaining Not Processed: {remaining}")
                        print("=======================================\n")

                        return dataframe

                    print(f"✗ {remarks}")

                    break

        remaining = (
            test_cases_to_process
            - success_count
            - failed_count
        )

        print("\n========== Execution Summary ==========")
        print(f"Provider               : {provider_name}")
        print(f"Dataset Size           : {total_test_cases}")
        print(f"Configured Execution   : {test_cases_to_process}")
        print(f"Processed Successfully : {success_count}")
        print(f"Failed                 : {failed_count}")
        print(f"Remaining Not Processed: {remaining}")
        print("=======================================\n")

        return dataframe