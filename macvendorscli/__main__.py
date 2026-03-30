import requests
import time

class MacVendors:
    BASE_URL = "https://api.macvendors.com"

    def __init__(self, timeout=5, rate_limit=1.0):
        self.timeout = timeout
        self.rate_limit = rate_limit  # segundos entre requisições

    def get_vendor(self, mac: str) -> str:
        try:
            url = f"{self.BASE_URL}/{mac}"
            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                time.sleep(self.rate_limit)
                return response.text.strip()
            elif response.status_code == 404:
                return "Vendor não encontrado"
            else:
                return f"Erro HTTP {response.status_code}"

        except requests.RequestException as e:
            return f"Erro de conexão: {e}"

    def get_vendors(self, mac_list):
        result = {}
        for mac in mac_list:
            result[mac] = self.get_vendor(mac)
        return result