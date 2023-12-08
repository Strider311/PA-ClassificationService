import logging
from pyfiglet import Figlet
from dotenv import load_dotenv
from Processors.ImageProcessor import ImageProcessor
import os
import datetime
import sys


def init_logger():

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(FORMAT)

    date = datetime.datetime.now()
    t = date.strftime("%d-%m-%Y--%H-%M-%S")
    log_file_name = f"log-"+t+".log"
    if not os.path.isdir('logs'):
        os.mkdir("logs")

    file = logging.FileHandler(filename='logs/'+log_file_name)
    file.setFormatter(formatter)
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    log = logging.getLogger()
    log.addHandler(file)
    log.setLevel(level=logging.DEBUG)


def startup_splash():

    f = Figlet(font='slant')
    print(f.renderText('Classification Service'))
    print(f"Version: {os.getenv('VERSION')}")
    print("-------------------------------------------------------")


def main():
    load_dotenv()
    startup_splash()
    init_logger()
    _ = ImageProcessor()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting, keyboard interupt")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except ConnectionError as e:
        logging.error(f"Connection issue: {e}")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
