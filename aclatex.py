import sys
import subprocess
import os
import time
import yaml

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


CMD_COMPILE_LATEX = 'platex'
CMD_CREATE_PDF    = 'dvipdfmx'


class EventHandler(FileSystemEventHandler):
    def __init__(self, file_name):
        self.file_name = file_name

    def get_extension(self, file_name):
        return os.path.splitext(file_name)[-1]

    def striip_extension(self, file_name):
        return file_name.split('.')[0]

    def on_modified(self, event):
        if self.get_extension(event.src_path) in ('.tex'):
            try:
                subprocess.run([CMD_COMPILE_LATEX, self.file_name])
                print('Success compiling a latex file')
                subprocess.run([CMD_CREATE_PDF, self.striip_extension(self.file_name)])
                print('Success creating a pdf file')
            except subprocess.SubprocessError as e:
                sys.stderr.write(e)


def get_data_from_yaml():
    '''
    Get data from aclatex.yaml
    file_name - a watched file
    dir_path  - directory watched file in
    interval  - watchdog timer
    '''
    f    = None
    data = None
    try:
        f = open('./aclatex.yaml', 'r')
        data = yaml.load(f)
        f.close()
    except Exception:
        sys.stderr.write('Can not read a YAML file\n')
    file_name = data['file_name']
    dir_path  = data['dir_path']
    interval  = data['interval']
    return file_name, dir_path, interval


def main():
    file_name, dir_path, interval = get_data_from_yaml()    # read data from aclatex.yaml
    event_handler = EventHandler(file_name)
    observer = Observer()
    print('Watching {}'.format(dir_path))
    observer.schedule(event_handler, dir_path)

    os.chdir(dir_path)    # Change directory to dir_path
    observer.start()      # Start watchdog

    try:
        while True:
            time.sleep(interval)
    except (Exception, KeyboardInterrupt):
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
