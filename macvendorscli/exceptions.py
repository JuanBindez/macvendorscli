class MacVendorsError(Exception):
    """Base exception for MacVendors client."""
    pass

class VendorNotFoundError(MacVendorsError):
    """Raised when a MAC address vendor is not found."""
    pass