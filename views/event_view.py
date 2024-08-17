from config.logger import get_logger


logger = get_logger()


def validation_error_event_view(e):
    print(e)
    logger.error(e)


def success_create_event_view():
    print("event created")


def list_event_view(events):
    for event in events:
        print(event)


def success_delete_event_view():
    print("event deleted")


def error_event_not_found_view(event_id):
    print("event not found")
    logger.error(f"event not found: {event_id}")


def error_contact_client_support_not_found_view(**kwargs):
    print("contract or client or support not found")
    logger.error(f"contract or client or support not found: {kwargs}")


def success_update_event_view():
    print("event updated")
