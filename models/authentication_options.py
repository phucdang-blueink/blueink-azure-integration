from dataclasses import dataclass

@dataclass
class AuthenticationOptions:
    endpoint: str
    grant_type: str
    scope: str
    resource: str

    client_id: str
    tenant_id: str
    client_secret: str



