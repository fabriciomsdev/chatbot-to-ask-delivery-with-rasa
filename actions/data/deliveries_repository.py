import secrets
from actions.data.database import RedisDataSource
from actions.data.dtos.delivery import Address, Customer, Delivery, Package


class DeliveriesRespository:
    def __init__(self, db = RedisDataSource()):
        self.db = db

    def get_all(self):
        data = self.db.get_all()

        for d in data:
            yield Delivery.from_dict(d)

    def get_by_id(self, id):
        data = self.db.get_by_id(id)
        return Delivery.from_dict(data)

    def create(self, delivery: Delivery):
        delivery.tracking_code = secrets.token_hex(16)
        return self.db.save(delivery.to_dict())

    def update(self, id, delivery: Delivery):
        return self.db.update(id, delivery.to_dict())

    def delete(self, id):
        return self.db.delete(id)
    
    def get_last(self):
        data = self.db.get_all()
        print(data)
        return Delivery.from_dict(data[-1])