### System ###
from io import StringIO

### Local ###
from events import midi_to_csv_map
from midi.fileio import read_midifile


def parse(file):
    """
    Input is a string, file or file-like object of type stringIO or bytesIO.
    Output is a file-like object of type stringIO containing the CSV data.
    """
    csv_file = StringIO()
    pattern = read_midifile(file)
    csv_file.write("0, 0, Header, {}, {}, {}\n".format(pattern.format, len(pattern), pattern.resolution))
    for index, track in enumerate(pattern):
        csv_file.write("{}, {}, Start_track\n".format(index + 1, 0))
        abstime = 0
        for event in track:
            abstime += event.tick
            csv_file.write(midi_to_csv_map[type(event)](index + 1, abstime, event))
    csv_file.write("0, 0, End_of_file")
    return csv_file


def main(args):
    with open(args.input, "rb") as input_file:
        converted = parse(input_file)
        with open(args.output, "w") as output_file:
            output_file.write(converted.getvalue())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Converts a MIDI file into a CSV representation.")
    parser.add_argument("-i", "--input", type=str, dest="input", required=True,
                        metavar="file", help="(required) The file to convert to CSV")
    parser.add_argument("-o", "--output", type=str, dest="output", required=True,
                        metavar="file", help="(required) The file to write the output to")
    args = parser.parse_args()

    main(args)
