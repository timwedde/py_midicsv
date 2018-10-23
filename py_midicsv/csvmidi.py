### System ###
import csv
from io import StringIO, BytesIO

### Local ###
from .midi.events import *
from .midi.containers import *
from .events import csv_to_midi_map
from .midi.fileio import FileWriter

COMMENT_DELIMITERS = ("#", ";")


def parse(file):
    """
    Input is a string, file or file-like object of type stringIO or bytesIO.
    Output is a file-like object of type bytesIO containing the binary MIDI data.
    """
    pattern = Pattern(tick_relative=False)
    for line in csv.reader(file, skipinitialspace=True):
        if line[0].startswith(COMMENT_DELIMITERS):
            continue
        tr = int(line[0])
        time = int(line[1])
        identifier = line[2].strip()
        if identifier == "Header":
            pattern.resolution = int(line[5])
        elif identifier == "End_of_file":
            continue
        elif identifier == "Start_track":
            track = Track(tick_relative=False)
            pattern.append(track)
        else:
            event = csv_to_midi_map[identifier](tr, time, identifier, line[3:])
            track.append(event)
    pattern.make_ticks_rel()
    return pattern


def main(args):
    with open(args.input, "r") as input_file:
        pattern = parse(input_file)
        with open(args.output, "wb") as output_file:
            midi_writer = FileWriter(output_file)
            midi_writer.write(pattern)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Converts a CSV file into MIDI representation.")
    parser.add_argument("-i", "--input", type=str, dest="input", required=True,
                        metavar="file", help="(required) The file to convert to MIDI")
    parser.add_argument("-o", "--output", type=str, dest="output", required=True,
                        metavar="file", help="(required) The file to write the output to")
    args = parser.parse_args()

    main(args)
