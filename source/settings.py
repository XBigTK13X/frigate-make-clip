import os

config = {
    'recording_dir': os.getenv('FMC_RECORDING_DIR', '/media/dev-recordings'),
    'clip_output_dir': os.getenv('FMC_CLIP_OUTPUT_DIR', '/home/kretst/frigate-make-clip'),
    'camera_names': [
        'green-room',
        'yellow-room',
        'play-north',
        'play-south',
        'blue-room',
        'purple-room',
        'dining-room',
        'kitchen',
        'basement-north',
        'basement-south',
        'garage',
        'outside-east',
        'outside-west',
        'patio',
        'front-door'
    ]
}
