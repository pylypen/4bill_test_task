import http
from src import app, redis_connect


class TestAmount:
    def test_set_single_correct_amount(self):
        redis_connect.flushall()
        client = app.test_client()
        resp = client.get('/request/100')
        assert resp.status_code == http.HTTPStatus.CREATED

    def test_set_multiple_correct_amount(self):
        client = app.test_client()
        resp = client.get('/request/100')
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = client.get('/request/200')
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = client.get('/request/455')
        assert resp.status_code == http.HTTPStatus.CREATED
        redis_connect.flushall()

    def test_set_not_correct_amount(self):
        client = app.test_client()
        resp = client.get('/request/999999999999999999999')
        assert resp.status_code == http.HTTPStatus.SERVICE_UNAVAILABLE

    def test_set_not_correct_url(self):
        client = app.test_client()
        resp = client.get('/request/')
        assert resp.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
