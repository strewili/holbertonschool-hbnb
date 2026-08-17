from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        return fn(*args, **kwargs)
    return wrapper
