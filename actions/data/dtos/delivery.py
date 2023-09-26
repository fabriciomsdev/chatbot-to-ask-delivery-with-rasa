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
    
    @staticmethod
    def from_dict(self, data: dict):
        delivery = Delivery()
        delivery.tracking_code = data.get('tracking_code')
        delivery.pickup_address = Address(**data.get('pickup_address')) if data.get('pickup_address') else None
        delivery.delivery_address = Address(**data.get('delivery_address')) if data.get('delivery_address') else None
        delivery.customer = Customer(**data.get('customer')) if data.get('customer') else None
        delivery.package = Package(**data.get('package')) if data.get('package') else None

        return delivery
    
    def to_dict(self) -> dict:
        data = self.__dict__

        if self.pickup_address:
            data['pickup_address'] = self.pickup_address.__dict__

        if self.delivery_address:
            data['delivery_address'] = self.delivery_address.__dict__

        if self.customer:
            data['customer'] = self.customer.__dict__

        if self.package:
            data['package'] = self.package.__dict__

        return data

@dataclass
class Quote:
    id: int = secrets.randbelow(100)
    eta: int = 0
    price: float = 0

    def __str__(self) -> str:
        return f'Opção {self.id} - Entrega em {self.eta} dias por R$ {self.price}'
    
