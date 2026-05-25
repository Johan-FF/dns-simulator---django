"""Critical security and service flow tests."""
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from Administradores.models import Administrador
from Clientes.models import Cliente
from Pagos.models import TarjetaCredito
from Pagos.services import PaymentService


class PublicClientRoutesTests(TestCase):
    def test_legacy_public_client_list_removed(self):
        client = Client()
        response = client.get('/clientes/')
        self.assertIn(response.status_code, (301, 302, 404))


class AdminClientListTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin_test', password='pass12345', email='admin@test.com'
        )
        Administrador.objects.create(
            user=self.admin_user,
            activo=True,
            puede_gestionar_usuarios=True,
        )

    def test_admin_client_list_requires_login(self):
        response = self.client.get(reverse('clientes:lista_clientes_admin'))
        self.assertEqual(response.status_code, 302)

    def test_admin_client_list_allowed_for_admin(self):
        self.client.login(username='admin_test', password='pass12345')
        response = self.client.get(reverse('clientes:lista_clientes_admin'))
        self.assertEqual(response.status_code, 200)


class TarjetaCreditoModelTests(TestCase):
    def test_register_card_does_not_store_pan_or_cvv(self):
        user = User.objects.create_user(username='payuser', password='pass12345')
        cliente = Cliente.objects.create(user=user)
        tarjeta = PaymentService.register_card(
            cliente,
            '4111111111111111',
            'TEST USER',
            '12/30',
        )
        self.assertEqual(tarjeta.last4, '1111')
        self.assertTrue(tarjeta.payment_token)
        self.assertFalse(hasattr(tarjeta, 'cvv'))
        field_names = {f.name for f in TarjetaCredito._meta.get_fields()}
        self.assertNotIn('numero', field_names)
        self.assertNotIn('cvv', field_names)


class AdminPermissionDecoratorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='limited', password='pass12345')
        Administrador.objects.create(
            user=self.user,
            activo=True,
            puede_gestionar_usuarios=False,
            puede_ver_estadisticas=True,
        )

    def test_gestionar_usuarios_denied_without_permission(self):
        self.client.login(username='limited', password='pass12345')
        response = self.client.get(reverse('administradores:gestionar_usuarios'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('dashboard', response.url)
