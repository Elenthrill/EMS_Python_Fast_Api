# dto/requests/auth.py
from pydantic import BaseModel
from domain.models.user import Role, AssignableRole


# dto/responses/user.py
class UserResponse(BaseModel):
    id: int
    login: str
    email: str
    role: str
    is_active: bool


class UpdateRoleRequest(BaseModel):
    login: str
    role: AssignableRole
