from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    INPUT_DATASET,
    OUTPUT_REPORT
)

from data.excel_reader import ExcelReader
from providers.gemini_provider import GeminiProvider


def main():

    print("===== Configuration Loaded =====")
    print(f"Model         : {GEMINI_MODEL}")
    print(f"Dataset       : {INPUT_DATASET}")
    print(f"Output Report : {OUTPUT_REPORT}")

    if GEMINI_API_KEY:
        print("API Key       : Loaded")
    else:
        print("API Key       : Missing")
        return

    print("\n===== AI Test Dataset =====")

    dataframe = ExcelReader.read_dataset(INPUT_DATASET)

    provider = GeminiProvider()

    print("\n===== Sending First Prompt =====\n")

    prompt = dataframe.iloc[0]["Input"]

    print("Prompt:")
    print(prompt)

    response = provider.generate_response(prompt)

    print("\nGemini Response:\n")

    print(response)


if __name__ == "__main__":
    main()