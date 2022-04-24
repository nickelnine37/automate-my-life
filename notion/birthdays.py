from notifications import Notification
from notion import notion
import pandas as pd
from datetime import datetime


def get_birthdays_database() -> pd.DataFrame:
    """
    Get a pandas dataframe representing the birthdays database from notion
    """

    data = notion.databases.query('0ce693f0cc3b4df2b8d3b72cba3c5b59')

    df = pd.json_normalize(data['results']).rename({'properties.Send card.formula.date.start': 'Send card',
                                                    'properties.Days until.formula.number': 'Days until',
                                                    'properties.Address 1.rich_text': 'Address',
                                                    'properties.Gender.rich_text': 'Gender',
                                                    'properties.Birthday.date.start': 'Birthday',
                                                    'properties.Name.title': 'Name'}, axis=1)

    def get_text(item):

        if len(item) > 0:
            return item[0]['text']['content']
        else:
            return None

    df['Name'] = df['Name'].apply(get_text)
    df['Address'] = df['Address'].apply(get_text)
    df['Gender'] = df['Gender'].apply(get_text)

    df['Send card'] = pd.to_datetime(df['Send card'])
    df['Birthday'] = pd.to_datetime(df['Birthday'])

    return df[['id', 'Name', 'Birthday', 'Days until', 'Send card', 'Address', 'Gender']].sort_values('Birthday').reset_index(drop=True)


def increment_birthday(row: pd.Series):
    """
    Take a row of the dataframe returned by get_birthdays_database, and send
    an instruction to Notion to increment the year of the relevant birthday by one
    """

    new_date = datetime.strftime(row['Birthday'].replace(year=row['Birthday'].year + 1), '%Y-%m-%d')
    notion.pages.update(row['id'], properties={'Birthday': {'date': {'start': new_date}}})


def get_day_suffix(n: int):
    """
    Simple helper function to convert a number to 1st, 2nd, 3rd ...
    """
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def format_date(date: datetime):
    """
    Format a date nicely
    """
    th = get_day_suffix(date.day)
    return datetime.strftime(date, f'%A the {th} of %B')


def get_messages(birthdays: pd.DataFrame):
    """
    Take the birthday dataframe and convert it into a set of birthday messages
    """

    month_message = "Its {}'s birthday on {}! There's still time to get {} a present..."
    week_message = "Its {}'s birthday on {}! Time to send {} a card..."
    today_message = "Hope you got a card for {}! It's {} birthday today..."

    messages = []

    # 1 month warning
    for i, row in birthdays[birthdays['Days until'] == 28].iterrows():
        messages.append(month_message.format(row['Name'], format_date(row['Birthday']), 'him' if row['Gender'] == 'M' else 'her'))

    # 1 week warning
    for i, row in birthdays[birthdays['Days until'] == 7].iterrows():
        messages.append(week_message.format(row['Name'], format_date(row['Birthday']), 'him' if row['Gender'] == 'M' else 'her'))

    # it's today warning
    for i, row in birthdays[birthdays['Days until'] == 0].iterrows():
        messages.append(today_message.format(row['Name'], 'his' if row['Gender'] == 'M' else 'her'))
        increment_birthday(row)

    return messages


def get_birthday_notifications():
    """
    Final wrapper function to get birthdays and convert into notifications
    """

    birthdays = get_birthdays_database()
    messages = get_messages(birthdays)

    return [Notification(title='Upcoming Birthday!', message=message) for message in messages]


def send_birthday_notifications():
    """
    Send all event notifications for the day
    """

    for notification in get_birthday_notifications():
        notification.send()

