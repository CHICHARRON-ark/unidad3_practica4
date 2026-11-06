from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # write_only: se acepta al crear o cambiar, y nunca sale en la respuesta.
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'telefono',
            'password',
            'is_active',
            'is_staff',
        ]

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Este campo es obligatorio.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        if not validated_data.get('username'):
            validated_data['username'] = validated_data.get('email')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Solo se reemplaza la contraseña cuando la petición la incluye.
        if password:
            instance.set_password(password)
        instance.save()
        return instance
