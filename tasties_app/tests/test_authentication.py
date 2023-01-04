import pytest
from pytest_django.asserts import assertTemplateUsed
from authConstants import (
    VALID_EMAIL, VALID_PASSWORD, VALID_USER, INVALID_EMAIL, INVALID_PASSWORD_MISMATCH, LOGIN_PATH, REGISTER_PATH,
    MISMATCH_ERROR
)


@pytest.mark.django_db
class TestViews:
    def test_login_loaded(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assertTemplateUsed(response, LOGIN_PATH)

    def test_register_loaded(self, client):
        response = client.get('/register/')
        assert response.status_code == 200
        assertTemplateUsed(response, REGISTER_PATH)

    def test_valid_registration(self, client):
        response = client.post('/register/', data={'username': 'telhaiuser', 'email': 'user@telhai.ac.il',
                                                   'password1': 'tastiesPassword', 'password2': 'tastiesPassword'})
        assert response.status_code == 302
        assert response.url == '/login/'

    def test_invalid_email_registration(self, client):
        response = client.post('/register/', data={'username': VALID_USER, 'email': INVALID_EMAIL,
                                                   'password1': VALID_PASSWORD, 'password2': VALID_PASSWORD})
        assert response.status_code == 200
        assert response.request['PATH_INFO'] == '/register/'

    def test_invalid_password_registration(self, client):
        response = client.post('/register/', data={'username': VALID_USER, 'email': VALID_EMAIL,
                                                   'password1': VALID_PASSWORD, 'password2': INVALID_PASSWORD_MISMATCH})
        assert response.status_code == 200
        assert response.context['form'].error_messages == MISMATCH_ERROR

    def test_valid_login(self, client, signed_up_credentials):
        response = client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        assert response.status_code == 302
        assert response.url == '/'

    def test_invalid_login(self, client, signed_up_credentials):
        response = client.post('/login/', data={'username': VALID_USER, 'password': INVALID_PASSWORD_MISMATCH})
        assert response.status_code == 200
        assert response.request['PATH_INFO'] == '/login/'

    def test_logout(self, client, signed_up_credentials):
        response = client.post('/logout/')
        assert response.status_code == 302
        assert response.url == '/login/'
