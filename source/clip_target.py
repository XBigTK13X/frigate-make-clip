from datetime import datetime

from pytz import timezone

def make_target(clip_date, clip_time):
    date_parts = clip_date.split('-')
    time_parts = clip_time.split('-')
    result = {
        'year': int(date_parts[0]),
        'month': int(date_parts[1]),
        'day': int(date_parts[2]),
        'hour': int(time_parts[0]),
        'minute': int(time_parts[1]),
    }

    result['dt'] = timezone("America/Chicago").localize(datetime(result['year'], result['month'], result['day'], result['hour'], result['minute']))

    return result
