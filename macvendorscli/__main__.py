import csv
import os
from typing import List, Dict

from macvendorscli.exceptions import VendorNotFoundError


class MacVendors:
    """
    Offline MAC address vendor lookup using IEEE OUI database.
    """

    def __init__(self) -> None:
        self.oui_db = self._load_oui()

    def _load_oui(self) -> Dict[str, str]:
        """
        Load OUI database from bundled CSV file.
        """
        db: Dict[str, str] = {}

        path = os.path.join(os.path.dirname(__file__), "oui.csv")

        if not os.path.exists(path):
            raise RuntimeError("OUI database file (oui.csv) not found in package")

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

        except Exception as e:
            raise RuntimeError(f"Failed to load OUI database: {e}") from e

        return db

    def _normalize_mac(self, mac: str) -> str:
        """
        Normalize MAC address to uppercase without separators.
        """
        return mac.replace(":", "").replace("-", "").upper()

    def _get_oui_prefix(self, mac: str) -> str:
        """
        Extract OUI prefix (first 6 hex characters).
        """
        normalized = self._normalize_mac(mac)

        if len(normalized) < 6:
            raise ValueError(f"Invalid MAC address: {mac}")

        return normalized[:6]

    def get_vendor(self, mac: str) -> str:
        """
        Get vendor for a single MAC address.

        :param mac: MAC address (e.g. 00:1A:2B:3C:4D:5E)
        :return: Vendor name
        :raises VendorNotFoundError: if vendor is not found
        """
        prefix = self._get_oui_prefix(mac)

        vendor = self.oui_db.get(prefix)

        if not vendor:
            raise VendorNotFoundError(f"Vendor not found for MAC: {mac}")

        return vendor

    def get_vendors(self, mac_list: List[str]) -> Dict[str, str]:
        """
        Get vendors for multiple MAC addresses.

        :param mac_list: list of MAC addresses
        :return: dict mapping MAC -> vendor or error message
        """
        results: Dict[str, str] = {}

        for mac in mac_list:
            try:
                results[mac] = self.get_vendor(mac)
            except Exception as e:
                results[mac] = str(e)

        return results

    def __call__(self, mac: str) -> str:
        """
        Allow instance to be called like a function.
        """
        return self.get_vendor(mac)