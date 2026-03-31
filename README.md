# macvendorscli

[![PyPI - Downloads](https://img.shields.io/pypi/dm/macvendorscli)](https://pypi.org/project/macvendorscli/)
![PyPI - License](https://img.shields.io/pypi/l/macvendorscli)
[![GitHub Tag](https://img.shields.io/github/v/tag/JuanBindez/macvendorscli?include_prereleases)](https://github.com/JuanBindez/macvendorscli/releases)
[![PyPI - Version](https://img.shields.io/pypi/v/macvendorscli)](https://pypi.org/project/macvendorscli/)

## CLI tool and Python3 library for offline MAC address vendor lookup using the IEEE OUI database.

## Install
    pip install macvendorscli

## Or install from source
    git clone https://github.com/JuanBindez/macvendorscli
    cd macvendorscli
    pip install .

## Usage CLI

    macvendorscli FC:FB:FB:01:FA:21

## Scripts

```python
from macvendorscli import MacVendors

client = MacVendors()

vendor = client.get_vendor("FC:FB:FB:01:FA:21")

print(vendor)
```