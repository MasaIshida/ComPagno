import uuid

def create_uuid():
    """
    UUIDを生成する
    32桁 16進数
    :return: uuid
    """
    return str(uuid.uuid4()).replace("-", "")