# macvendorscli

CLI and Python library to lookup MAC address vendors using the macvendors API.

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