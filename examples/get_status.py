import gopay
from gopay.enums import TokenScope, Language

payments = gopay.payments(
    {
        "goid": "my goid",
        "client_id": "my id",
        "client_secret": "my secret",
        "gateway_url": "https://gw.sandbox.gopay.com/",
        "scope": TokenScope.ALL,
        "language": Language.CZECH,
    }
)

response = payments.get_status("payment id")
if response.success:
    print(f"Hooray, API returned {response}")
else:
    print(f"Oops, API returned {response.status_code}: {response}")
