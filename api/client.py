from config import AUTH_TOKEN

import requests
import json


class BaseClient:
    headers = {"Content-Type": "application/json", "Authorization": f"Token {AUTH_TOKEN}"}
    method = None
    url = None
    data = None

    def __init__(self):
        assert self.url is not None, "endpoint must be set"
        assert self.method is not None, "method must be set"
        self.response = None
        self.do_request()

    def do_request(self):
        try:
            self.response = requests.request(
                method=self.method,
                url=self.url,
                json=self.data,
                headers=self.headers,
                timeout=15,
            )
        except Exception as exp:
            print(f"ERROR | Ошибка запроса {exp}")
            return


class GetProducts(BaseClient):
    method = "GET"

    def __init__(self, url: str):
        self.url = url
        super().__init__()


class GetShops(BaseClient):
    method = "GET"

    def __init__(self, *args, **kwargs):
        self.url = "http://127.0.0.1:8000/api/shops/"
        super().__init__()


class GetAddress(BaseClient):
    method = "GET"

    def __init__(self, *args, **kwargs):
        self.url = "http://127.0.0.1:8000/api/address/"
        super().__init__()


class GetAllProductsAndShop(BaseClient):
    method = "GET"

    def __init__(self, *args, **kwargs):
        self.url = "http://127.0.0.1:8000/api/products/all/"
        super().__init__()


class GetDetailProduct(BaseClient):
    method = "GET"

    def __init__(self, product_id: int, *args, **kwargs):
        self.url = f"http://127.0.0.1:8000/api/products/{product_id}/"
        super().__init__()


class SendBestProduct(BaseClient):
    method = "POST"

    def __init__(self, product_id: int, telegram_id: int, *args, **kwargs):
        self.url = f"http://127.0.0.1:8000/api/products/best/"
        self.data = {"product_id": product_id, "telegram_id": telegram_id}
        print(self.data)
        super().__init__()


class GetBestProduct(BaseClient):
    method = "GET"

    def __init__(self, *args, **kwargs):
        self.url = f"http://127.0.0.1:8000/api/products/best/"
        super().__init__()
