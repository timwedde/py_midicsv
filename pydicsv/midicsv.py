from io import StringIO
from midi.events import *
from events import midi_to_csv_map
from midi.fileio import read_midifile

def write_event(track, time, event, data, file):
    file.write(("{}, {}, {}" + (", {}" * len(data)) + "\n").format(track, time, midi_to_csv_map[type(event)], *data))

def data_for_event(event):
    data = None

    if isinstance(event, PitchWheelEvent):
        data = [(event.data[0] | event.data[1] << 7)]
    elif isinstance(event, SequenceNumberMetaEvent):
        data = (event.data[0] << 8) | event.data[1]
    elif isinstance(event, (ChannelPrefixEvent, PortEvent, SmpteOffsetEvent, TimeSignatureEvent)):
        data = [*event.data]
    elif isinstance(event, SetTempoEvent):
        data = [event.get_mpqn()]
    elif isinstance(event, KeySignatureEvent):
        data = [event.get_alternatives(), '"major"' if event.data[1] == 0 else '"minor"']
    elif isinstance(event, SequencerSpecificEvent):
        data = [len(event.data)].append(*event.data)
    elif isinstance(event, SysexEvent):
        data = [len(event.data)].append(*event.data)
    elif isinstance(event, (EndOfTrackEvent, TrackLoopEvent, SomethingEvent)):
        data = []

    if isinstance(event, Event):
        if data is None and len(event.data) > 0:
            data = [*event.data]
        if data:
            data.insert(0, event.channel)
    elif isinstance(event, MetaEvent):
        if data is None:
            data = ['"{}"'.format(event.text)]

    return data

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
            data = None
            if not isinstance(event, (Event, MetaEvent)):
                csv_file.write("{}, {}, Unknown_meta_event, {}\n".format(index + 1, abstime, event.metacommand, event.len))
                continue
            data = data_for_event(event)
            write_event(index + 1, abstime, event, data, csv_file)
    csv_file.write("0, 0, End_of_file")
    return csv_file

def main(file):
    print(parse(file).getvalue())

if __name__ == '__main__':
    main("test.mid")
