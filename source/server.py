import os
import sys

from settings import config
from call_external import execute
import frigate

from flask import Flask, render_template, request, send_from_directory

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
        print(f"It already exists: {output_path}")
        return send_from_directory(directory=clip_output_dir, path=clip_filename, as_attachment=True)

    frigate.load_recordings()
    start = frigate.find_nearest_recording(camera_name, start_date, start_time)
    end = frigate.find_nearest_recording(camera_name, end_date, end_time)
    recordings = frigate.get_recordings(camera_name, start['key'], end['key'])

    appended_filenames = ' + '.join(recordings)
    merge_command = f'mkvmerge --append-mode file -o "{output_path}" {appended_filenames}'
    execute(merge_command)

    return send_from_directory(directory=clip_output_dir, path=clip_filename, as_attachment=True)
