class MacVendorsError(Exception):
    """Base exception for MacVendors client."""
    pass

class VendorNotFoundError(MacVendorsError):
    """Raised when a MAC address vendor is not found."""
    pass

class APIRequestError(MacVendorsError):
    """Raised when an HTTP or connection error occurs."""
    pass