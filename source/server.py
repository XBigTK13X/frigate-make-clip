from flask import Flask, render_template, request, send_from_directory
import frigate
from call_external import execute
import os
import sys

from settings import config
from clip_target import make_target
import pprint
print("Current settings")
pprint.pprint(config)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', camera_names=config['camera_names'])


@app.route('/api/clip/download')
def api_clip_download():
    camera_name = request.args.get('camera_name')
    start_date = request.args.get('start_date')
    start_time = request.args.get('start_time')
    end_date = request.args.get('end_date')
    end_time = request.args.get('end_time')

    clip_output_dir = config['clip_output_dir']
    clip_filename = f'{camera_name} from {start_date} {start_time} until {end_date} {end_time}.mp4'

    output_path = f'{clip_output_dir}/{clip_filename}'

    if os.path.isfile(output_path):
        return send_from_directory(directory=clip_output_dir, path=clip_filename, as_attachment=True)

    print("Trying to create " + output_path, flush=True)

    start_target = make_target(start_date, start_time)
    end_target = make_target(end_date, end_time)

    if start_target['dt'] >= end_target['dt']:
        return "End time must be after start time"

    print("Finding bound recordings", flush=True)
    recordings = frigate.find_bound_recordings(camera_name, start_target, end_target)
    if recordings is None or len(recordings) == 0:
        return "No recordings found for timespan"

    appended_filenames = ' + '.join(recordings)
    merge_command = f'mkvmerge --append-mode file -o "{output_path}" {appended_filenames}'
    print(f"Merging {len(recordings)} recordings", flush=True)
    execute(merge_command)
    print("All done", flush=True)
    return send_from_directory(directory=clip_output_dir, path=clip_filename, as_attachment=True)
