import os

from settings import config


recordings = None


def load_recordings():
    global recordings
    recordings = {
        'list': {

        },
        'lookup': {}
    }
    for root, dirs, files in os.walk(config['recording_dir']):
        for f in files:
            f_path = os.path.join(root, f)
            path_parts = f_path.split('/')
            date_parts = path_parts[-5].split('-')
            recording_key = f_path
            file_parts = f.split('.')
            recording = {
                'key': f_path,
                'camera_name': path_parts[-2],
                'hour': int(path_parts[-3]),
                'day': int(path_parts[-4]),
                'year': int(date_parts[0]),
                'month': int(date_parts[1]),
                'minute': int(file_parts[0]),
                'second': int(file_parts[1])
            }
            recordings['lookup'][recording_key] = recording
            if not recording['camera_name'] in recordings['list']:
                recordings['list'][recording['camera_name']] = []
            recordings['list'][recording['camera_name']].append(f_path)
            recordings['list'][recording['camera_name']].sort()


def find_nearest_recording(camera_name, target_date, target_time):
    global recordings
    date_parts = target_date.split('-')
    time_parts = target_time.split('-')
    target_year = int(date_parts[0])
    target_month = int(date_parts[1])
    target_day = int(date_parts[2])
    target_hour = int(time_parts[0])
    target_minute = int(time_parts[1])

    target_recording = None
    for recording_key in recordings['list'][camera_name]:
        recording = recordings['lookup'][recording_key]
        if target_recording is None:
            target_recording = recording
        else:
            if recording['year'] == target_year and recording['month'] == target_month and recording['day'] == target_day:
                if recording['hour'] <= target_hour and recording['minute'] <= target_minute:
                    target_recording = recording
                else:
                    return target_recording
            else:
                return target_recording
    return target_recording


def get_recordings(camera_name, start_key, end_key):
    global recordings
    target_recordings = []
    active = False
    for recording_key in recordings['list'][camera_name]:
        if recording_key == start_key:
            active = True
        if active == True:
            target_recordings.append('"'+recording_key+'"')
        if recording_key == end_key:
            active = False
    return target_recordings
