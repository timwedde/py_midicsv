from io import StringIO
from midi.events import *
from events import csv_to_midi_map
from midi.fileio import read_midifile

def write_event(event, file):
    pass

def parse(file):
    pass

def main(file):
    print(parse(file).getvalue())

if __name__ == '__main__':
    # TODO: Set up argparse
    main("test.csv")
