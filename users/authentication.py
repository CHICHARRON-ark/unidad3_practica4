from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthentication(JWTAuthentication):
    def get_raw_token(self, header):
        parts = header.split()
        if len(parts) == 1:
            return parts[0]
        return super().get_raw_token(header)
