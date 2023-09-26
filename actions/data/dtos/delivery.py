from dataclasses import dataclass
import secrets
from time import sleep
from typing import List

@dataclass
class Address:
    address: str = None


@dataclass
class Package:
    weight: float = 0
    width: float = 0
    height: float = 0
    depth: float = 0
    value: float = 0

@dataclass
class Customer:
    name: str = None
    phone: str = None

@dataclass
class Delivery:
    tracking_code: str = secrets.token_hex(16)
    pickup_address: Address = None
    delivery_address: Address = None
    customer: Customer = None
    package: Package = None
    status: str = 'Aberta'
    scheduled_time: str = None

    def __str__(self) -> str:
        return f'Entrega {self.tracking_code} - {self.status}'

@dataclass
class Quote:
    id: int = secrets.randbelow(100)
    eta: int = 0
    price: float = 0

    def __str__(self) -> str:
        return f'Opção {self.id} - Entrega em {self.eta} dias por R$ {self.price}'
    
