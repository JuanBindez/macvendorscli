import requests
import time
from typing import List, Dict
from macvendorscli.exceptions import *


class MacVendors:
    """
    Client for querying MAC address vendor information using the MacVendors API.

    Example:
        client = MacVendors()
        vendor = client.get_vendor("00:1A:2B:3C:4D:5E")
    """

    BASE_URL = "https://api.macvendors.com"

    def __init__(self, timeout: int = 5, rate_limit: float = 1.0) -> None:
        """
        Initialize the MacVendors client.

        :param timeout: Timeout for HTTP requests in seconds.
        :param rate_limit: Delay between requests in seconds.
        """
        self.timeout = timeout
        self.rate_limit = rate_limit

    def get_vendor(self, mac: str) -> str:
        """
        Retrieve the vendor name for a single MAC address.

        :param mac: MAC address (e.g., '00:1A:2B:3C:4D:5E').
        :return: Vendor name.
        :raises VendorNotFoundError: If the MAC vendor is not found.
        :raises APIRequestError: If an HTTP or connection error occurs.
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

    def get_vendors(self, mac_list: List[str]) -> Dict[str, str]:
        """
        Retrieve vendor names for multiple MAC addresses.

        :param mac_list: List of MAC addresses.
        :return: Dictionary mapping MAC addresses to vendor names or errors.
        """
        results: Dict[str, str] = {}

        for mac in mac_list:
            try:
                results[mac] = self.get_vendor(mac)
            except MacVendorsError as e:
                results[mac] = str(e)

        return results

    def __call__(self, mac: str) -> str:
        """
        Allow the instance to be called like a function.

        Example:
            client = MacVendors()
            print(client("00:1A:2B:3C:4D:5E"))
        """
        return self.get_vendor(mac)