from macvendorscli import MacVendors

client = MacVendors()

vendor = client.get_vendor("FC:FB:FB:01:FA:21")

print(vendor)