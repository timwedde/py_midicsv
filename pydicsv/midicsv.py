from io import StringIO
from events import midi_to_csv_map
from midi.fileio import read_midifile

# input is a string, file or file-like object of type stringIO or bytesIO
# output is file-like object of type stringIO containing the CSV data
def parse(file):
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

def main(file):
    print(parse(file).getvalue())

if __name__ == '__main__':
    main("out.mid")
