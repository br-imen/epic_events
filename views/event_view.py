import logging


def validation_error_event_view(e):
    print(e)
    logging.error(e)


def success_create_event_view():
    print("event created")


def list_event_view(events):
    for event in events:
        print(event)


def success_delete_event_view():
    print("event deleted")


def error_event_not_found_view():
    print("event not found")
    logging.error("event not found")


def error_contact_client_support_not_found_view():
    print("contract or client or support not found")
    logging.error("contract or client or support not found")


def success_update_event_view():
    print("event updated")
