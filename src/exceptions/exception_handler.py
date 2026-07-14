import time


class ExceptionHandler:
    """
    Handles Gemini API and DeepEval exceptions.
    """

    MAX_RETRIES = 3
    RETRY_DELAY = 10  # seconds

    @staticmethod
    def handle(error, attempt):
        """
        Returns:
            action  : retry | stop | fail
            remarks : Friendly message
        """

        error_message = str(error)

        # Uncomment during debugging if needed
        # print(f"\nRAW ERROR: {error_message}\n")

        # ---------------------------------
        # 429 - Quota Exhausted
        # ---------------------------------
        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):

            return {
                "action": "stop",
                "remarks": "Gemini API quota exhausted."
            }

        # ---------------------------------
        # 503 - Service Busy
        # ---------------------------------
        elif (
            "503" in error_message
            or "UNAVAILABLE" in error_message
        ):

            if attempt < ExceptionHandler.MAX_RETRIES:

                print(
                    f"Server busy. Retrying "
                    f"({attempt}/{ExceptionHandler.MAX_RETRIES})..."
                )

                time.sleep(ExceptionHandler.RETRY_DELAY)

                return {
                    "action": "retry",
                    "remarks": "Gemini service temporarily unavailable."
                }

            return {
                "action": "fail",
                "remarks": "Gemini service unavailable after retries."
            }

        # ---------------------------------
        # 401 - Invalid API Key
        # ---------------------------------
        elif (
            "401" in error_message
            or "UNAUTHENTICATED" in error_message
        ):

            return {
                "action": "stop",
                "remarks": "Invalid Gemini API Key."
            }

        # ---------------------------------
        # 403 - Permission Denied
        # ---------------------------------
        elif (
            "403" in error_message
            or "PERMISSION_DENIED" in error_message
        ):

            return {
                "action": "stop",
                "remarks": "Permission denied for Gemini API."
            }

        # ---------------------------------
        # 404 - Invalid Model
        # ---------------------------------
        elif (
            "404" in error_message
            or "NOT_FOUND" in error_message
        ):

            return {
                "action": "stop",
                "remarks": "Configured Gemini model not found."
            }

        # ---------------------------------
        # 400 - Bad Request
        # ---------------------------------
        elif (
            "400" in error_message
            or "INVALID_ARGUMENT" in error_message
        ):

            return {
                "action": "fail",
                "remarks": "Invalid request sent to Gemini."
            }

        # ---------------------------------
        # Network / Connection Issues
        # ---------------------------------
        elif (
            "connection" in error_message.lower()
            or "network" in error_message.lower()
        ):

            return {
                "action": "retry",
                "remarks": "Network connection issue."
            }

        # ---------------------------------
        # Timeout
        # ---------------------------------
        elif "timeout" in error_message.lower():

            if attempt < ExceptionHandler.MAX_RETRIES:

                print(
                    f"Timeout. Retrying "
                    f"({attempt}/{ExceptionHandler.MAX_RETRIES})..."
                )

                time.sleep(ExceptionHandler.RETRY_DELAY)

                return {
                    "action": "retry",
                    "remarks": "Request timeout."
                }

            return {
                "action": "fail",
                "remarks": "Request timed out."
            }

        # ---------------------------------
        # Unknown Error
        # ---------------------------------
        return {
            "action": "fail",
            "remarks": f"Unexpected Error: {error_message}"
        }