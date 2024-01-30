from abc import ABC
from fastapi import Request, HTTPException


class BasePermission(ABC):
    """
    A base class from which all permission classes should inherit.
    """
    STATUS_CODE = 401
    DETAIL = "Not authenticated"

    def has_permission(self, request: Request):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def __call__(self, request: Request):
        if not self.has_permission(request):
            raise HTTPException(status_code=self.STATUS_CODE, detail=self.DETAIL)


class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, request: Request):
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request: Request):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    STATUS_CODE = 403
    DETAIL = "Permission denied"

    def has_permission(self, request: Request):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


allow_any = AllowAny()
is_authenticated = IsAuthenticated()
is_admin = IsAdmin()
