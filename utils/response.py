from typing import Any

def success_response(msg: str = "success", data: Any = None) -> dict:
    return {"code": 200, "msg": msg, "data": data}

def error_response(code: int = 400, msg: str = "error", data: Any = None) -> dict:
    return {"code": code, "msg": msg, "data": data}