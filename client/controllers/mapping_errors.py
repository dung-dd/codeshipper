# coding: utf-8
class ERRORS_CODE:
    SUCCESS = 0
    SUPER_SECRET_INVALID = 1
    SUPER_SECRET_NOT_EXIST = 2
    PROJECT_CODE_NOT_EXIST = 100
    UNKNOW_ERROR = 9999


MAPPING_ERRORS = {
    ERRORS_CODE.SUCCESS: "Thành công",
    ERRORS_CODE.SUPER_SECRET_INVALID: "Mã kết nối không hợp lệ",
    ERRORS_CODE.SUPER_SECRET_NOT_EXIST: "Mã kết nối không tồn tại trên máy khách",
    ERRORS_CODE.PROJECT_CODE_NOT_EXIST: "Project Code không xác định",
    ERRORS_CODE.UNKNOW_ERROR: "Lỗi không xác định",
}


def mapping_errors(error_key):
    return {"code": error_key, "message": MAPPING_ERRORS[error_key]}
