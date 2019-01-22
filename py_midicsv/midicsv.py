### System ###
from io import StringIO

### Local ###
from .events import midi_to_csv_map
from .midi.fileio import read_midifile


def parse(file):
    """
    Input is a string, file or file-like object of type stringIO or bytesIO.
    Output is a list of strings containing the CSV data.
    """
    csv_file = []
    pattern = read_midifile(file)
    csv_file.append("0, 0, Header, {}, {}, {}\n".format(pattern.format, len(pattern), pattern.resolution))
    for index, track in enumerate(pattern):
        csv_file.append("{}, {}, Start_track\n".format(index + 1, 0))
        abstime = 0
        for event in track:
            abstime += event.tick
            csv_file.append(midi_to_csv_map[type(event)](index + 1, abstime, event))
    csv_file.append("0, 0, End_of_file")
    return csv_file
