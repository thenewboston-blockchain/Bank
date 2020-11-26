def standardize_notification(*, notification_type, payload):
    """Format notification correctly according to network protocol"""
    return {
        'notification_type': notification_type,
        'payload': payload
    }
