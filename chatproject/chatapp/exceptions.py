from rest_framework import exceptions, status

class CustomException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "result": False,
        "msg": "There seems to be a problem, please try again later.",
    }
    default_code = "Error Occurred"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        super().__init__(detail=detail, code=code)
