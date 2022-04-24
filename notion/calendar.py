from notifications import Notification
from notion import notion
from datetime import datetime


def get_todays_events():
    """
    Return a list of dictionaries with keys 'title' and 'time'. These are the events for the day.
    If the event has an associated time, 'time' will be something like '2022-04-24T03:00:00.000+01:00'
    Otherwise, it will be something like '2022-04-24'
    """
    calendar_id = 'c2a2670497f7460eb85759da81dbc1f9'
    query = {"property": "Date", "date": {"equals": datetime.strftime(datetime.today(), '%Y-%m-%d')}}
    events = notion.databases.query(calendar_id, filter=query)['results']

    events = [{'title': event['properties']['Name']['title'][0]['text']['content'],
               'time': event['properties']['Date']['date']['start']} for event in events]

    return events


def get_event_notifications() -> list:
    """
    Final wrapper function to get todays events as Notification objects
    """

    events = get_todays_events()

    notifications = []
    for event in events:

        if 'T' in event['time']:
            notification = Notification(title='Upcoming event', message=event['title'] + f' at {event["time"][11:16]}')
        else:
            notification = Notification(title='Upcoming event', message=event['title'])

        notifications.append(notification)

    return notifications


def send_event_notifications():
    """
    Send all event notifications for the day
    """

    for notification in get_event_notifications():
        notification.send()

