def success_response(msg: str = "success", data: dict | None = None) -> dict:
    return {"code": 200, "msg": msg, "data": data}
