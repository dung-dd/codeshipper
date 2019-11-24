# coding: utf-8


class Secure():
    @staticmethod
    def preprocess_input(data, data_type, require=False):
        if not isinstance (data, data_type):
            return { state: 0, message: "Kiểu dữ liệu không hợp lệ" }

        if require:
            if not data:
                return { state: 0, message: "Dữ liệu không hợp lệ"}

        return { state: 1, message: "" }
