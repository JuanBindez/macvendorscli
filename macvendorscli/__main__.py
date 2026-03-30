import requests
import time
import csv
import os
from typing import List, Dict, Optional

from macvendorscli.exceptions import (
    VendorNotFoundError,
    APIRequestError,
)


class MacVendors:
    BASE_URL = "https://api.macvendors.com"

    def __init__(
        self,
        timeout: int = 5,
        rate_limit: float = 1.0,
    ) -> None:
        """
        :param timeout: HTTP timeout
        :param rate_limit: delay between API requests
        """
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.oui_db = self._load_oui()

    def _load_oui(self) -> Dict[str, str]:
        """
        Load OUI database from bundled CSV file.
        """
        db: Dict[str, str] = {}

        path = os.path.join(os.path.dirname(__file__), "oui.csv")

        if not os.path.exists(path):
            return db  # não quebra a lib se não existir

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    prefix = (
                        row.get("Assignment")
                        or row.get("Registry Assignment")
                        or row.get("MA-L")
                    )

                    vendor = row.get("Organization Name")

                    if prefix and vendor:
                        db[prefix.upper()] = vendor.strip()

        except Exception:
            return {}

        return db

    def _normalize_mac(self, mac: str) -> str:
        return mac.replace(":", "").replace("-", "").upper()

    def _get_oui_prefix(self, mac: str) -> str:
        return self._normalize_mac(mac)[:6]

    def get_vendor_offline(self, mac: str) -> Optional[str]:
        """
        Lookup vendor using local OUI database.
        """
        if not self.oui_db:
            return None

        prefix = self._get_oui_prefix(mac)
        return self.oui_db.get(prefix)

    def get_vendor_online(self, mac: str) -> str:
        """
        Lookup vendor using MacVendors API.
        """
        try:
            url = f"{self.BASE_URL}/{mac}"
            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                time.sleep(self.rate_limit)
                return response.text.strip()

            elif response.status_code == 404:
                raise VendorNotFoundError(f"Vendor not found for MAC: {mac}")

            else:
                raise APIRequestError(
                    f"HTTP error {response.status_code} for MAC: {mac}"
                )

        except requests.RequestException as e:
            raise APIRequestError(f"Connection error: {e}") from e

    def get_vendor(self, mac: str) -> str:
        """
        Try offline first, fallback to API.
        """
        vendor = self.get_vendor_offline(mac)

        if vendor:
            return vendor

        return self.get_vendor_online(mac)

    def get_vendors(self, mac_list: List[str]) -> Dict[str, str]:
        """
        Lookup multiple MAC addresses.
        """
        results: Dict[str, str] = {}

        for mac in mac_list:
            try:
                results[mac] = self.get_vendor(mac)
            except Exception as e:
                results[mac] = str(e)

        return results