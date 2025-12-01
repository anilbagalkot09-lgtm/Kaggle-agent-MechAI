import requests

class SupplierOpenAPITool:
    def __init__(self, base_url: str = 'http://localhost:8081', api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key

    def place_order(self, supplier_id: str, payload: dict):
        # simplified synchronous call - in real world use async and proper error handling
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        resp = requests.post(f'{self.base_url}/orders', json={'supplier_id': supplier_id, 'order': payload}, headers=headers)
        return resp.json()
