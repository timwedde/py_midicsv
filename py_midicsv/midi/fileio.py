import sys
from struct import pack, unpack

from .constants import *
from .containers import *
from .events import *
from .util import *


class ParseError(Exception):
    pass


class ValidationError(Exception):
    pass


def warn_or_error(text, strict=True, is_parse=True):
    if strict:
        if is_parse:
            raise ParseError(text)
        else:
            raise ValidationError(text)
    print(f"Warning: {text}", file=sys.stderr)


class Trackiter:
    def __init__(self, iterable, pos=0):
        self._buf = iterable
        self._it = iter(iterable)
        self._pos = pos

    def __iter__(self):
        return self

    def __next__(self):
        self._pos += 1
        return next(self._it)

    def pos(self):
        return self._pos

    def errmsg(self, msg, data):
        return f"{msg} 0x{data:02X} at position {self.pos()}"

    def assert_data_byte(self, data):
        assert data & 0x80 == 0, self.errmsg("Unexpected status byte", data)

    def assert_status_byte(self, data):
        assert data & 0x80 != 0, self.errmsg("Unexpected data byte", data)

    def get_data_byte(self, strict=True):
        byte = self.__next__()
        try:
            self.assert_data_byte(byte)
        except Exception as e:
            print(f"Warning: {e}", file=sys.stderr)
        return byte


class FileReader:
    def read(self, midifile, strict=True):
        pattern = self.parse_file_header(midifile, strict)
        Pattern.useRunningStatus = False
        for track in pattern:
            self.parse_track(midifile, track, strict)
        return pattern

    def parse_file_header(self, midifile, strict=True):
        # First four bytes are MIDI header
        magic = midifile.read(4)
        if magic != b"MThd":
            raise TypeError("Bad header in MIDI file.", magic)
        # next four bytes are header size
        # next two bytes specify the format version
        # next two bytes specify the number of tracks
        # next two bytes specify the resolution/PPQ/Parts Per Quarter
        # (in other words, how many ticks per quater note)
        data = unpack(">LHHH", midifile.read(10))
        hdrsz = data[0] + 8
        format = data[1]
        tracks = [Track() for x in range(data[2])]
        resolution = data[3]
        Pattern.useRunningStatus = False
        # XXX: the assumption is that any remaining bytes
        # in the header are padding
        if hdrsz > DEFAULT_MIDI_HEADER_SIZE:
            midifile.read(hdrsz - DEFAULT_MIDI_HEADER_SIZE)
        self.basepos = hdrsz
        return Pattern(tracks=tracks, resolution=resolution, format=format)

    def parse_track_header(self, midifile):
        # First four bytes are Track header
        magic = midifile.read(4)
        if magic != b"MTrk":
            raise TypeError("Bad track header in MIDI file: ", magic)
        # next four bytes are track size
        trksz = unpack(">L", midifile.read(4))[0]
        self.basepos += 8
        return trksz

    def parse_track(self, midifile, track, strict=True):
        self.RunningStatus = None
        trksz = self.parse_track_header(midifile)
        trackdata = Trackiter(midifile.read(trksz), pos=self.basepos)
        while True:
            try:
                event = self.parse_midi_event(trackdata, strict)
                if event:
                    track.append(event)
            except StopIteration:
                break
        self.basepos += trksz

    def parse_midi_event(self, trackdata, strict=True):
        # first datum is varlen representing delta-time
        tick = read_varlen(trackdata)
        # next byte is status message
        stsmsg = next(trackdata)
        # is the event a MetaEvent?
        if MetaEvent.is_event(stsmsg):
            cmd = trackdata.get_data_byte(strict)
            if cmd not in EventRegistry.MetaEvents:
                print(
                    f"Unknown Meta MIDI Event {cmd} at position {trackdata.pos()}",
                    file=sys.stderr,
                )
                return
            cls = EventRegistry.MetaEvents[cmd]
            datalen = read_varlen(trackdata)
            data = [next(trackdata) for x in range(datalen)]
            event = cls(tick=tick, data=data)
            try:
                event.check()
            except Exception as e:
                warn_or_error(f"{e} at position {trackdata.pos()}", strict, is_parse=False)
            return event
        # is this event a Sysex Event?
        elif SysexEvent.is_event(stsmsg):
            datalen = read_varlen(trackdata)
            data = [next(trackdata) for x in range(datalen)]
            if stsmsg not in EventRegistry.Events:
                warn_or_error(
                    f"Unknown Sysex Event {stsmsg:02x} at position {trackdata.pos()}",
                    strict,
                )
                return
            cls = EventRegistry.Events[stsmsg]
            event = cls(tick=tick, data=data)
            try:
                event.check()
            except Exception as e:
                warn_or_error(f"{e} at position {trackdata.pos()}", strict, is_parse=False)
            return event
        # not a Meta MIDI event or a Sysex event, must be a general message
        else:
            key = stsmsg & 0xF0
            if key not in EventRegistry.Events:
                if not self.RunningStatus:
                    trackdata.assert_status_byte(stsmsg)
                Pattern.useRunningStatus = True
                key = self.RunningStatus & 0xF0
                cls = EventRegistry.Events[key]
                channel = self.RunningStatus & 0x0F
                data = [stsmsg]
                for _ in range(cls.length - 1):
                    b = trackdata.get_data_byte(strict)
                    data.append(b)
                event = cls(tick=tick, channel=channel, data=data)
                try:
                    event.check()
                except Exception as e:
                    warn_or_error(f"{e} at position {trackdata.pos()}", strict, is_parse=False)
                return event
            else:
                self.RunningStatus = stsmsg
                cls = EventRegistry.Events[key]
                channel = self.RunningStatus & 0x0F
                data = []
                for _ in range(cls.length):
                    b = trackdata.get_data_byte(strict)
                    data.append(b)
                event = cls(tick=tick, channel=channel, data=data)
                try:
                    event.check()
                except Exception as e:
                    warn_or_error(f"{e} at position {trackdata.pos()}", strict, is_parse=False)
                return event
        warn_or_error(f"Unknown MIDI Event {stsmsg} at position {trackdata.pos()}", strict)


class FileWriter:
    RunningStatus = None

    def __init__(self, file):
        self.file = file

    def write(self, pattern):
        self.write_file_header(pattern, len(pattern))
        for track in pattern:
            self.write_track(track)

    def write_file_header(self, pattern, length=None):
        if length is None:
            length = len(pattern)
        # First four bytes are MIDI header
        packdata = pack(">LHHH", 6, pattern.format, length, pattern.resolution)
        self.file.write(b"MThd" + packdata)

    def write_track(self, track):
        hlen = len(self.encode_track_header(0))
        buf = bytearray(b"0" * hlen)
        for event in track:
            buf.extend(self.encode_midi_event(event))
        buf[:hlen] = self.encode_track_header(len(buf) - hlen)
        self.file.write(buf)

    def write_track_header(self, track=None):
        if track is None:
            trklen = 1
        elif isinstance(track, int):
            trklen = track
        else:
            trklen = len(track)
        self.file.write(self.encode_track_header(trklen))

    def encode_track_header(self, trklen):
        return b"MTrk" + pack(">L", trklen)

    def write_midi_event(self, event):
        # be sure to write the track and pattern headers first
        # can stream to timidity or fluidsynth this way
        self.file.write(self.encode_midi_event(event))

    def encode_midi_event(self, event):
        ret = bytearray()
        assert isinstance(event.tick, int), event.tick
        ret.extend(write_varlen(event.tick))
        # is the event a MetaEvent?
        if isinstance(event, MetaEvent):
            self.RunningStatus = None
            ret.append(event.statusmsg)
            ret.append(event.metacommand)
            ret.extend(write_varlen(len(event.data)))
            ret.extend(event.data)
        # is this event a Sysex Event?
        elif isinstance(event, SysexEvent):
            self.RunningStatus = None
            ret.append(event.statusmsg)
            ret.extend(write_varlen(len(event.data)))
            ret.extend(event.data)
        # not a Meta MIDI event or a Sysex event, must be a general message
        elif isinstance(event, Event):
            status = event.statusmsg | event.channel
            if status != self.RunningStatus or not Pattern.useRunningStatus:
                self.RunningStatus = status
                ret.append(status)
            ret.extend(event.data)
        else:
            raise ValueError("Unknown MIDI Event: " + str(event))
        return ret


def write_midifile(midifile, pattern):
    if type(midifile) in (str, str):
        with open(midifile, "wb") as out:
            return write_midifile(out, pattern)
    writer = FileWriter(midifile)
    return writer.write(pattern)


def read_midifile(midifile, strict):
    if type(midifile) in (str, bytes):
        with open(midifile, "rb") as inp:
            return read_midifile(inp, strict)
    reader = FileReader()
    return reader.read(midifile, strict)
