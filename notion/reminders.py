from notifications import Notification
from notion import notion


def get_cron(frequency: str, when: str):
    """
    Convert a frequency and when propery into args for cron job
    """

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    if frequency.lower() == 'daily':
        hour, minute = [int(t) for t in when.split(':')]
        return {'hour': hour, 'minute': minute}

    if frequency.lower() == 'weekly':
        day, time = when.split(', ')
        hour, minute = [int(t) for t in time.split(':')]
        day = days.index(day.lower())
        return {'day_of_week': day, 'hour': hour, 'minute': minute}

    if frequency.lower() == 'weekdays':
        hour, minute = [int(t) for t in when.split(':')]
        return {'day_of_week': '0-4', 'hour': hour, 'minute': minute}


def get_reminder_notifications():

    reminders = notion.databases.query('34a8bd115c80464bba3eeaa448f40593')['results']

    reminder_notifications = []

    for reminder in reminders:

        name = reminder['properties']['Name']['title']

        if len(name) > 0:
            frequency = reminder['properties']['Frequency']['multi_select'][0]['name']

            when = reminder['properties']['When']['rich_text'][0]['text']['content']

            message = name[0]['text']['content']

            reminder_notifications.append((Notification(title='Reminder!', message=message), get_cron(frequency, when)))

    return reminder_notifications