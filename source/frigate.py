import os

from settings import config

from datetime import datetime

from pytz import timezone

# frigate pre 0.12 recording dir/file structure
# /media/dev-recordings/yyyy-mm/dd/hh/camera/mm.ss.mp4

# frigate post 0.12 recording dir/file structure
# /media/dev-recordings/yyyy-mm-dd/hh/camera/mm.ss.mp4

tz = timezone("America/Chicago")

def find_bound_recordings(camera_name, start_target, end_target):
    recordings = []
    start_dt = tz.localize(datetime(start_target['year'], start_target['month'], start_target['day'],
                        start_target['hour'], start_target['minute']))
    end_dt = tz.localize(datetime(end_target['year'], end_target['month'], end_target['day'],
                      end_target['hour'], end_target['minute']))
    for root, dirs, files in os.walk(config['recording_dir']):
        for f in files:
            f_path = os.path.join(root, f)
            if not camera_name in f_path:
                continue
            path_parts = f_path.split('/')
            date_parts = path_parts[-4].split('-')
            file_parts = f.split('.')
            recording = {
                'key': f_path,
                'camera_name': path_parts[-2],
                'hour': int(path_parts[-3]),
                'day': int(date_parts[2]),
                'year': int(date_parts[0]),
                'month': int(date_parts[1]),
                'minute': int(file_parts[0]),
                'second': int(file_parts[1])
            }
            recording_dt = timezone("UTC").localize(datetime(recording['year'], recording['month'], recording['day'],
                                    recording['hour'], recording['minute']))
            if recording_dt <= end_dt and recording_dt >= start_dt:
                recordings.append(recording['key'])
    recordings.sort()
    return recordings
