import argparse
from macvendorscli import MacVendors
from macvendorscli.version import __version__


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
    results = client.get_vendors(args.macs)

    for mac, vendor in results.items():
        print(f"{mac} -> {vendor}")


if __name__ == "__main__":
    main()