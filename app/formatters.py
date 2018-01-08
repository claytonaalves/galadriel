import datetime

def format_datetime(value):
    return value.strftime("%d/%m/%Y")


def format_time(value):
    return value.strftime("%H:%M:%S")


def register_formatters(app):
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['time'] = format_time
