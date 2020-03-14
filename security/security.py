

class SecurityManager:

    def __init__(self):
        pass

    def check_sql_injection(self, request_data):

        if ";" in request_data:
            request_data.replace(";", "#double_colon#")

        if "'" in request_data:
            request_data.replace("'", "#single#")
