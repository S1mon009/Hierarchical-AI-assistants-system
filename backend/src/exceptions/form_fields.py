"""
Form fields custom exceptions.

This module defines custom exception classes used by the
routers and services. These exceptions help distinguish between specific
error cases such as missing form fields during.
"""
class MissingFormFieldsException(Exception):
    """Exception raised when one or more required form fields are missing.

    This exception includes the list of missing fields, allowing the API
    to return precise information about which form parameters were not
    provided by the client.

    Attributes:
        missing_fields (list[str]): List of missing form field names.
        message (str): Explanation of the error.
    """

    def __init__(self, missing_fields: list[str]):
        self.missing_fields = missing_fields
        self.message = (
            "Missing required form fields: " + ", ".join(missing_fields)
        )
        super().__init__(self.message)
