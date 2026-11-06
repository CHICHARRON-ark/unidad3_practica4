from drf_yasg.inspectors import SwaggerAutoSchema


class JWTAutoSchema(SwaggerAutoSchema):
    def get_security(self):
        permissions = getattr(self.view, 'permission_classes', [])
        if any(permission.__name__ == 'AllowAny' for permission in permissions):
            return []
        return [{'Bearer': []}]
