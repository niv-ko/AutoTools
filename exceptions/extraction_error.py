from typing import Optional


class ExtractionError(RuntimeError):
    def __init__(self, extractor_name: str, parameter_name: str):
        self.extractor_name = extractor_name
        self.parameter_name = parameter_name
        message = f"Error in extractor '{extractor_name}' for parameter '{parameter_name}'."
        if self.__cause__:
            message += f" Cause: {str(self.__cause__)}"
        super().__init__(message)
