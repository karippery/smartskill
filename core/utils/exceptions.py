
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        error_details = response.data

        # Customize the error response format
        response.data = {
            "error": {
                "status_code": response.status_code,
                "message": "An error occurred" if response.status_code >= 500 else "Bad request",
                "details": {
                    #"detail": error_details.get('detail', 'No additional details provided.'),
                    #"code": error_details.get('code', 'unknown_error'),
                   #"message": error_details.get('message', error_details)
                    "message": format_error_messages(error_details)
                    #"message": error_details.get('message', error_details.get('non_field_errors', 'No additional message provided.'))
                }
            }
        }
    else:
        # If the exception was not handled by DRF's default handler, return a generic error
        response = {
            "error": {
                "status_code": 500,
                "message": "An unexpected error occurred",
                "details": {
                    "detail": str(exc),
                    "code": "unexpected_error"
                }
            }
        }

    return response


def format_error_messages(error_details):
    """
    Formats the error details to fit the expected structure.
    """
    formatted_errors = []

    if isinstance(error_details, dict):
        for key, messages in error_details.items():
            if isinstance(messages, list):
                formatted_errors.extend(messages)

    return formatted_errors