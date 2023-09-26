# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.data.deliveries_repository import DeliveriesRespository

from actions.data.dtos.delivery import Address, Delivery, Package
from actions.services.platform import MEDIUM_PACKAGE, SMALL_PACKAGE, PlatformService

logging.basicConfig(level=logging.DEBUG)


delivery_repository = DeliveriesRespository()

#
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "utter_greet"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        logging.info(domain)
        dispatcher.utter_message(text="Hello World!")

        return None
    

class StartDeliveryRequest(Action):

    def name(self) -> Text:
        return "start_delivery_request"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        logging.info("Start delivery Request")

        delivery = Delivery()
        delivery_repository.create(delivery)
        logging.info("Save delivery " + str(delivery))

        dispatcher.utter_message(text="Qual o endereço de coleta da entrega?")

        return None
    

class SavePickupAddress(Action):

    def name(self) -> Text:
        return "save_pickup_address"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        
        print('get_latest_entity_values', tracker.get_latest_entity_values("address"))
        print('get_slot', tracker.get_slot("address"))
        last_delivery = delivery_repository.get_last()
        last_delivery.pickup_address = Address(
            (tracker.latest_message)['text']
        )

        logging.info("Save pickup address " + str(last_delivery))

        delivery_repository.update(last_delivery.tracking_code, last_delivery)

        dispatcher.utter_message(text="Onde devo entregar?")

        return None
    

class SaveDeliveryAddress(Action):

    def name(self) -> Text:
        return "save_delivery_address"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        
        print('get_latest_entity_values', tracker.get_latest_entity_values("address"))
        print('get_slot', tracker.get_slot("address"))
        last_delivery = delivery_repository.get_last()
        last_delivery.delivery_address = Address((tracker.latest_message)['text'])

        logging.info("Save delivery address " + str(last_delivery))

        delivery_repository.update(last_delivery.tracking_code, last_delivery)

        dispatcher.utter_message(text="Seu pacote pesa mais que 50 kilos?")

        return None
    

class AddSmallPackage(Action):

    def name(self) -> Text:
        return "add_small_package"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        last_delivery = delivery_repository.get_last()
        last_delivery.package = SMALL_PACKAGE

        logging.info("Save package " + str(last_delivery))

        delivery_repository.update(last_delivery.tracking_code, last_delivery)

        dispatcher.utter_message(text="Quer entregar agora ou agendar?")

        return None
    

class AddMediumPackage(Action):
        def name(self) -> Text:
            return "add_medium_package"
    
        def run(self, 
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
    
            last_delivery = delivery_repository.get_last()
            last_delivery.package = MEDIUM_PACKAGE
    
            logging.info("Save package " + str(last_delivery))
    
            delivery_repository.update(last_delivery.tracking_code, last_delivery)
    
            dispatcher.utter_message(text="Quer entregar agora ou agendar?")
    
            return None
        

class AddLargePackage(Action):
    def name(self) -> Text:
        return "add_big_package"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:

        last_delivery = delivery_repository.get_last()
        last_delivery.package = LARGE_PACKAGE

        logging.info("Save package " + str(last_delivery))

        delivery_repository.update(last_delivery.tracking_code, last_delivery)

        dispatcher.utter_message(text="Quer entregar agora ou agendar?")

        return None


class SavePackageWeight(Action):

    def name(self) -> Text:
        return "save_package_weight"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        
        print('get_latest_entity_values', tracker.get_latest_entity_values("weight"))
        print('get_slot', tracker.get_slot("weight"))
        last_delivery = delivery_repository.get_last()
        last_delivery.package = Package(
            weight=tracker.get_slot("weight"),
            width=50,
            height=50,
            depth=50,
            value=50,
        )

        logging.info("Save package " + str(last_delivery))

        delivery_repository.update(last_delivery.tracking_code, last_delivery)

        dispatcher.utter_message(text="Quer entregar agora ou agendar?")

        return None



class ScheduleDelivery(Action):

    def name(self) -> Text:
        return "schedule_delivery"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        
        print('get_latest_entity_values', tracker.get_latest_entity_values("time"))
        print('get_slot', tracker.get_slot("time"))
        last_delivery = delivery_repository.get_last()
        last_delivery.scheduled_time = tracker.get_slot("time")

        logging.info("Schedule delivery " + str(last_delivery))

        delivery_repository.update(last_delivery.tracking_code, last_delivery)

        dispatcher.utter_message(text="Muito obrigado sua entrega foi agendada para " + last_delivery.scheduled_time)

        return None
    

class AskDelivery(Action):

    def name(self) -> Text:
        return "ask_delivery"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
        ) -> List[Dict[Text, Any]]:
        
        last_delivery = delivery_repository.get_last()

        logging.info("Asking Delivery " + str(last_delivery))
        quotes = PlatformService().get_quote(last_delivery)

        PlatformService().ask_delivery(quotes[0], last_delivery)

        dispatcher.utter_message(text="O motorista está a caminho para coletar o seu pedido")

        return None