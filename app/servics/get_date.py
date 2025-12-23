from datetime import datetime

def get_current_date():
    """
    获取当前日前作为文件前缀，格式为YYYY-MM-DD
    """
    return datetime.now().strftime("%Y-%m-%d")
