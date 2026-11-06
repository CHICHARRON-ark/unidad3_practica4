from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin@tienda.com', 'AdminPass123')
        self.alumno = User.objects.create_user(
            'alumno@tienda.com',
            'AlumnoPass123',
            first_name='Ana',
            last_name='López',
            telefono='6441234567',
        )

    def test_la_contrasena_no_sale_en_datos_personales_ni_en_el_listado(self):
        self.client.force_authenticate(user=self.alumno)
        me = self.client.get('/api/v1/auth/me/')
        self.assertEqual(me.status_code, 200)
        self.assertNotIn('password', me.data)
        self.assertEqual(me.data['email'], 'alumno@tienda.com')
        self.assertEqual(me.data['telefono'], '6441234567')

        self.client.force_authenticate(user=self.admin)
        listed = self.client.get('/api/v1/users/')
        self.assertEqual(listed.status_code, 200)
        for user in listed.data:
            self.assertNotIn('password', user)

    def test_editar_sin_contrasena_no_la_cambia(self):
        hash_antes = self.alumno.password
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f'/api/v1/users/{self.alumno.id}/',
            {'first_name': 'Ana María'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)
        self.assertEqual(response.data['first_name'], 'Ana María')

        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.password, hash_antes)
        self.assertTrue(self.alumno.check_password('AlumnoPass123'))
        self.assertFalse(self.alumno.check_password('AdminPass123'))

    def test_editar_con_contrasena_si_la_cambia(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            f'/api/v1/users/{self.alumno.id}/',
            {'password': 'NuevaPass123'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)
        self.alumno.refresh_from_db()
        self.assertTrue(self.alumno.check_password('NuevaPass123'))
        self.assertFalse(self.alumno.check_password('AlumnoPass123'))
