from time import sleep
from typing import List
from actions.data.dtos.delivery import Delivery, Package, Quote

SMALL_PACKAGE = Package(
    weight=1,
    width=10,
    height=10,
    depth=10,
    value=100
)

MEDIUM_PACKAGE = Package(
    weight=2,
    width=20,
    height=20,
    depth=20,
    value=200
)

LARGE_PACKAGE = Package(
    weight=3,
    width=30,
    height=30,
    depth=30,
    value=300
)

class PlatformService():
    def __init__(self):
        pass

    def get_quote(self, delivery: Delivery) -> List[Quote]:
        sleep(3) # Fingindo chamada para o serviço de entrega da Any
        return [
            Quote(id=1, eta=1, price=10),
            Quote(id=2, eta=2, price=20),
            Quote(id=3, eta=3, price=30),
        ]

    def ask_delivery(self, quote: Quote, delivery: Delivery) -> Delivery:
        # TODO: realizar chamada para o serviço de entrega da Any
        sleep(5) # Fingindo chamada para o serviço de entrega da Any
        return True

    def get_status(self, tracking_code: str) -> Delivery:
        delivery = Delivery()
        delivery.tracking_code = tracking_code
        delivery.status = 'Em trânsito'

        return delivery