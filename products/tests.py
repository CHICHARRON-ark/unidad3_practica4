from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product

User = get_user_model()

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@tienda.com', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # Categoría base
        self.category = Category.objects.create(name='Electrónica')

    def test_create_category(self):
        """Prueba 1: Crear una categoría"""
        response = self.client.post('/api/v1/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        """Prueba 2: Listar categorías"""
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='productos@tienda.com', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # Datos iniciales para pruebas
        self.category = Category.objects.create(name='Electrónica')
        self.product = Product.objects.create(
            name='Laptop TUF Gaming',
            category=self.category,
            description='Laptop para desarrollo y juegos',
            price=15999.00,
            is_active=True
        )

    def test_create_product(self):
        """Prueba 3: Crear un producto"""
        data = {
            'name': 'Mouse Gamer',
            'category': self.category.id,
            'description': 'Mouse óptico RGB',
            'price': 450.00,
            'is_active': True
        }
        response = self.client.post('/api/v1/products/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        """Prueba 4: Listar productos"""
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        """Prueba 5: Actualizar un producto"""
        data = {
            'name': 'Laptop TUF Gaming V2',
            'category': self.category.id,
            'description': 'Laptop para desarrollo con más RAM',
            'price': 17500.00,
            'is_active': True
        }
        response = self.client.put(f'/api/v1/products/{self.product.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop TUF Gaming V2')

    def test_delete_product(self):
        """Prueba 6: Eliminar un producto"""
        response = self.client.delete(f'/api/v1/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)