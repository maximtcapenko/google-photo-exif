import argparse
import json
import piexif
import os

from datetime import UTC, datetime
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--path', dest='path', required=True, type=str)

def get_metadata_files(entries: list[Path]):
    return [entry for entry in entries if entry.is_file() and entry.name.endswith('.json')]

def get_image_files(entries: list[Path]):
    return [entry for entry in entries if entry.is_file() and entry.name.endswith('.jpg')]

class Json:
    def __init__(self, json):
        self._json = json

    def __getattr__(self, name):
        value = self._json.get(name, None)
        if value and isinstance(value, dict):
            return Json(value)
        return value

class ImageMetaPair:
    def __init__(self, image: Path, metadata: Path):
        self.image = image
        self.metadata = metadata

def process_file(metadata, file_path: Path):
    if metadata.photoTakenTime:
        print(f'Process [photoTakenTime] metadata for {file_path}')
        date = datetime.fromtimestamp(int(metadata.photoTakenTime.timestamp), UTC)
        exif_dict = {'Exif': {piexif.ExifIFD.DateTimeOriginal: f'{date}'}}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, f'{file_path}')

def walk(path):
    metadata_files = get_metadata_files(Path(path).iterdir())
    image_files = get_image_files(Path(path).iterdir())
    dirs = [entry.name for entry in Path(path).iterdir() if entry.is_dir()]

    files = list(map(lambda x: ImageMetaPair(x, next(filter(lambda m: m.name.startswith(x.name), metadata_files), None)), image_files))
    
    for file in files:
        if file.metadata:
            metadata = json.loads(file.metadata.read_bytes())
            process_file(Json(metadata), file.image)

    for dir in dirs:
        walk(dir)

def main():
    args = parser.parse_args()
    if not os.path.exists(args.path):
        print('Path does not exist')
        return

    if os.path.isdir(args.path):
        # get files from dir
        walk(args.path)
    else:
     print('Enter a directory path')

main()
