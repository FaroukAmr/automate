import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

home = os.path.expanduser("~")
source_folder = home+"/Downloads/"

# extensions
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".txt"]
coding_extensions = [".java", ".html", ".py",
                     ".cpp", ".js", ".css", ".php", ".ts"]

# destination folders
folders = {
    'audio': home+"/Desktop/audio/",
    'video': home+"/Desktop/video/",
    'image': home+"/Desktop/image/",
    'docs': home+"/Desktop/docs/",
    'code': home+"/Desktop/code/",
    'other': home+"/Desktop/other/"
}

# create the folders if they don't exist
for key in folders:
    if not os.path.exists(folders[key]):
        os.makedirs(folders[key])


class handler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_folder) as entries:
            for entry in entries:
                name = entry.name
                # check if entry is an image
                if name.endswith(tuple(image_extensions)):
                    move(source_folder, folders['image'], name)
                    continue
                # check if entry is a video
                if name.endswith(tuple(video_extensions)):
                    move(source_folder, folders['video'], name)
                    continue
                # check if entry is an audio
                if name.endswith(tuple(audio_extensions)):
                    move(source_folder, folders['audio'], name)
                    continue
                # check if entry is a document
                if name.endswith(tuple(document_extensions)):
                    move(source_folder, folders['docs'], name)
                    continue
                # check if entry is a coding file
                if name.endswith(tuple(coding_extensions)):
                    move(source_folder, folders['code'], name)
                    continue
                # move everything else to other folder
                move(source_folder, folders['other'], name)


def move(source, dest, name):
    os.rename(source+name, dest+name)
    logging.info("Moved "+name + " to " + dest)


def init():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_folder
    event_handler = handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    init()
