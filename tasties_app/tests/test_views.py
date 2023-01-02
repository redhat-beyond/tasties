import pytest


class TestViews:
    @pytest.mark.django_db
    def test_base_loaded(self, client):
        response = client.get('/base/')
        assert response.status_code == 200
        assert b"tasties" in response.content
