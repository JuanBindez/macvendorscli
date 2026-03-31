import argparse
from macvendorscli import MacVendors
from macvendorscli.version import __version__
from macvendorscli.exceptions import (
    MacVendorsError,
    VendorNotFoundError,
)


def main():
    print(f"macvendorscli v{__version__}\n")

    parser = argparse.ArgumentParser(
        description="CLI tool to lookup MAC address vendors using the MacVendors API"
    )

    parser.add_argument(
        "macs",
        nargs="+",
        help="One or more MAC addresses (e.g. 00:1A:2B:3C:4D:5E)"
    )

    args = parser.parse_args()

    client = MacVendors()

    for mac in args.macs:
        try:
            vendor = client.get_vendor(mac)
            print(f"{mac} -> {vendor}")

        except VendorNotFoundError:
            print(f"{mac} -> Vendor not found")

        except MacVendorsError as e:
            print(f"{mac} -> Error: {e}")


if __name__ == "__main__":
    main()