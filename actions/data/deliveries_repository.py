import secrets
from actions.data.database import RedisDataSource
from actions.data.dtos.delivery import Address, Customer, Delivery, Package


class DeliveriesRespository:
    def __init__(self, db = RedisDataSource()):
        self.db = db

    def dict_to_entity(self, data: dict) -> Delivery:
            delivery = Delivery()
            delivery.tracking_code = data.get('tracking_code')
            delivery.pickup_address = Address(**data.get('pickup_address')) if data.get('pickup_address') else None
            delivery.delivery_address = Address(**data.get('delivery_address')) if data.get('delivery_address') else None
            delivery.customer = Customer(**data.get('customer')) if data.get('customer') else None
            delivery.package = Package(**data.get('package')) if data.get('package') else None

            return delivery

    def get_all(self):
        data = self.db.get_all()

        for d in data:
            yield self.dict_to_entity(d)

    def get_by_id(self, id):
        data = self.db.get_by_id(id)
        return self.dict_to_entity(data)

    def create(self, delivery: Delivery):
        delivery.tracking_code = secrets.token_hex(16)
        return self.db.save(delivery.__dict__)

    def update(self, id, delivery):
        return self.db.update(id, delivery.__dict__)

    def delete(self, id):
        return self.db.delete(id)
    
    def get_last(self):
        data = self.db.get_all()
        print(data)
        return self.dict_to_entity(data[-1])