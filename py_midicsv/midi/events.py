### System ###
import struct
from abc import abstractmethod
from functools import total_ordering
from typing import ClassVar

# Reference: http://midi.teragonaudio.com/tech/midispec.htm


class EventRegistry:
    Events: ClassVar = {}
    MetaEvents: ClassVar = {}

    @classmethod
    def register_event(cls, event, bases):
        if (Event in bases) or (NoteEvent in bases) or (SysexEvent in bases):
            assert event.statusmsg not in cls.Events, f"Event {event.name} already registered"
            cls.Events[event.statusmsg] = event
        elif (MetaEvent in bases) or (MetaEventWithText in bases):
            assert event.metacommand not in cls.MetaEvents, f"Event {event.name} already registered"
            cls.MetaEvents[event.metacommand] = event
        else:
            raise ValueError(f"Unknown bases class in event type: {event.name}")


class AutoRegister(type):
    def __init__(cls, name, bases, dict):
        if name not in {
            "AbstractEvent",
            "Event",
            "MetaEvent",
            "NoteEvent",
            "MetaEventWithText",
        }:
            EventRegistry.register_event(cls, bases)


@total_ordering
class AbstractEvent(metaclass=AutoRegister):
    name = "Generic MIDI Event"
    length = 0
    statusmsg = 0x0

    def __init__(self, tick=0, **kwargs):
        if isinstance(self.length, int):
            self.data = [0] * self.length
        else:
            self.data = []
        self.tick = tick
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, other):
        return (self.tick, self.data) == (other.tick, other.data)

    def __lt__(self, other):
        return self.tick < other.tick

    def __repr__(self):
        return f"{self.__class__.__name__}(tick={self.tick}, data={self.data})"

    def check(self):
        if isinstance(self.length, int):
            assert len(self.data) == self.length, f"Event length mismatch for {self.__class__.__name__}"
        self.validate()

    @abstractmethod
    def validate(self):
        pass


@total_ordering
class Event(AbstractEvent):
    name = "Event"

    def __init__(self, tick=0, channel=0, **kwargs):
        self.channel = channel
        super().__init__(tick, **kwargs)

    def __eq__(self, other):
        return (self.tick, self.data, self.channel) == (
            other.tick,
            other.data,
            other.channel,
        )

    def __lt__(self, other):
        return self.tick < other.tick

    def __repr__(self):
        return f"{self.__class__.__name__}(tick={self.tick}, data={self.data}, channel={self.channel})"

    @classmethod
    def is_event(cls, statusmsg):
        return cls.statusmsg == (statusmsg & 0xF0)


class MetaEvent(AbstractEvent):
    """
    MetaEvent is a special subclass of Event that is not meant to
    be used as a concrete class.  It defines a subset of Events known
    as the Meta events.
    """

    statusmsg = 0xFF
    metacommand = 0x0
    name = "Meta Event"

    @classmethod
    def is_event(cls, statusmsg):
        return cls.statusmsg == statusmsg


class NoteEvent(Event):
    """
    NoteEvent is a special subclass of Event that is not meant to
    be used as a concrete class.  It defines the generalities of NoteOn
    and NoteOff events.
    """

    length = 2

    def get_pitch(self):
        return self.data[0]

    def set_pitch(self, val):
        self.data[0] = val

    pitch = property(get_pitch, set_pitch)

    def get_velocity(self):
        return self.data[1]

    def set_velocity(self, val):
        self.data[1] = val

    velocity = property(get_velocity, set_velocity)

    def validate(self):
        assert 0 <= self.data[0] <= 127, f"Note value is out of range: {self.data[0]}"
        assert 0 <= self.data[1] <= 127, f"Velocity value is out of range: {self.data[1]}"


class NoteOnEvent(NoteEvent):
    statusmsg = 0x90
    name = "Note On"


class NoteOffEvent(NoteEvent):
    statusmsg = 0x80
    name = "Note Off"


class AfterTouchEvent(Event):
    statusmsg = 0xA0
    length = 2
    name = "After Touch"

    def get_pitch(self):
        return self.data[0]

    def set_pitch(self, val):
        self.data[0] = val

    pitch = property(get_pitch, set_pitch)

    def get_value(self):
        return self.data[1]

    def set_value(self, val):
        self.data[1] = val

    value = property(get_value, set_value)

    def validate(self):
        assert 0 <= self.data[0] <= 127, f"Note value is out of range: {self.data[0]}"
        assert 0 <= self.data[1] <= 127, f"Pressure value is out of range: {self.data[1]}"


class ControlChangeEvent(Event):
    statusmsg = 0xB0
    length = 2
    name = "Control Change"

    def set_control(self, val):
        self.data[0] = val

    def get_control(self):
        return self.data[0]

    control = property(get_control, set_control)

    def set_value(self, val):
        self.data[1] = val

    def get_value(self):
        return self.data[1]

    def validate(self):
        assert 0 <= self.data[0] <= 127, f"Controller number is out of range: {self.data[0]}"
        assert 0 <= self.data[1] <= 127, f"Controller value is out of range: {self.data[1]}"

    value = property(get_value, set_value)


class ProgramChangeEvent(Event):
    statusmsg = 0xC0
    length = 1
    name = "Program Change"

    def set_value(self, val):
        self.data[0] = val

    def get_value(self):
        return self.data[0]

    value = property(get_value, set_value)

    def validate(self):
        assert 0 <= self.data[0] <= 127, f"Program value is out of range: {self.data[0]}"


class ChannelAfterTouchEvent(Event):
    statusmsg = 0xD0
    length = 1
    name = "Channel After Touch"

    def set_value(self, val):
        self.data[0] = val

    def get_value(self):
        return self.data[0]

    value = property(get_value, set_value)

    def validate(self):
        assert 0 <= self.data[0] <= 127, f"Pressure value is out of range: {self.data[1]}"


class PitchWheelEvent(Event):
    statusmsg = 0xE0
    length = 2
    name = "Pitch Wheel"

    def get_pitch(self):
        return ((self.data[1] << 7) | self.data[0]) - 0x2000

    def set_pitch(self, pitch):
        value = pitch + 0x2000
        self.data[0] = value & 0x7F
        self.data[1] = (value >> 7) & 0x7F

    pitch = property(get_pitch, set_pitch)


class SysexEvent(Event):
    statusmsg = 0xF0
    name = "SysEx"
    length = "varlen"

    @classmethod
    def is_event(cls, statusmsg):
        return cls.statusmsg == statusmsg or statusmsg == 0xF7


class SequenceNumberMetaEvent(MetaEvent):
    name = "Sequence Number"
    metacommand = 0x00
    length = 2


class MetaEventWithText(MetaEvent):
    def __init__(self, **kw):
        super().__init__(**kw)
        if "text" not in kw:
            self.text = b"".join(struct.pack("B", datum) for datum in self.data)

    def __repr__(self):
        return self.__baserepr__(["text"])


class TextMetaEvent(MetaEventWithText):
    name = "Text"
    metacommand = 0x01
    length = "varlen"


class CopyrightMetaEvent(MetaEventWithText):
    name = "Copyright Notice"
    metacommand = 0x02
    length = "varlen"


class TrackNameEvent(MetaEventWithText):
    name = "Track Name"
    metacommand = 0x03
    length = "varlen"


class InstrumentNameEvent(MetaEventWithText):
    name = "Instrument Name"
    metacommand = 0x04
    length = "varlen"


class LyricsEvent(MetaEventWithText):
    name = "Lyrics"
    metacommand = 0x05
    length = "varlen"


class MarkerEvent(MetaEventWithText):
    name = "Marker"
    metacommand = 0x06
    length = "varlen"


class CuePointEvent(MetaEventWithText):
    name = "Cue Point"
    metacommand = 0x07
    length = "varlen"


class ProgramNameEvent(MetaEventWithText):
    name = "Program Name"
    metacommand = 0x08
    length = "varlen"


class DeviceNameEvent(MetaEventWithText):
    name = "Device Name"
    metacommand = 0x09
    length = "varlen"


class ChannelPrefixEvent(MetaEvent):
    name = "Channel Prefix"
    metacommand = 0x20
    length = 1


class PortEvent(MetaEvent):
    name = "MIDI Port/Cable"
    metacommand = 0x21


class TrackLoopEvent(MetaEvent):
    name = "Track Loop"
    metacommand = 0x2E


class EndOfTrackEvent(MetaEvent):
    name = "End of Track"
    metacommand = 0x2F


class SetTempoEvent(MetaEvent):
    name = "Set Tempo"
    metacommand = 0x51
    length = 3

    def set_bpm(self, bpm):
        self.mpqn = int(6e7 / bpm)

    def get_bpm(self):
        return 6e7 / self.mpqn

    bpm = property(get_bpm, set_bpm)

    def get_mpqn(self):
        assert len(self.data) == 3
        vals = [self.data[x] << (16 - (8 * x)) for x in range(3)]
        return sum(vals)

    def set_mpqn(self, val):
        self.data = [(val >> (16 - (8 * x)) & 0xFF) for x in range(3)]

    mpqn = property(get_mpqn, set_mpqn)


class SmpteOffsetEvent(MetaEvent):
    name = "SMPTE Offset"
    metacommand = 0x54
    length = 5

    def get_hr(self):
        return self.data[0]

    def set_hr(self, val):
        self.data[0] = val

    hr = property(get_hr, set_hr)

    def get_mn(self):
        return self.data[1]

    def set_mn(self, val):
        self.data[1] = val

    mn = property(get_mn, set_mn)

    def get_se(self):
        return self.data[2]

    def set_se(self, val):
        self.data[2] = val

    se = property(get_se, set_se)

    def get_fr(self):
        return self.data[3]

    def set_fr(self, val):
        self.data[3] = val

    fr = property(get_fr, set_fr)

    def get_ff(self):
        return self.data[4]

    def set_ff(self, val):
        self.data[4] = val

    ff = property(get_ff, set_ff)


class TimeSignatureEvent(MetaEvent):
    name = "Time Signature"
    metacommand = 0x58
    length = 4

    def get_numerator(self):
        return self.data[0]

    def set_numerator(self, val):
        self.data[0] = val

    numerator = property(get_numerator, set_numerator)

    def get_denominator(self):
        return 2 ** self.data[1]

    def set_denominator(self, val):
        self.data[1] = val

    denominator = property(get_denominator, set_denominator)

    def get_metronome(self):
        return self.data[2]

    def set_metronome(self, val):
        self.data[2] = val

    metronome = property(get_metronome, set_metronome)

    def get_thirtyseconds(self):
        return self.data[3]

    def set_thirtyseconds(self, val):
        self.data[3] = val

    thirtyseconds = property(get_thirtyseconds, set_thirtyseconds)


class KeySignatureEvent(MetaEvent):
    name = "Key Signature"
    metacommand = 0x59
    length = 2

    def get_alternatives(self):
        d = self.data[0]
        return d - 256 if d > 127 else d

    def set_alternatives(self, val):
        self.data[0] = 256 + val if val < 0 else val

    alternatives = property(get_alternatives, set_alternatives)

    def get_minor(self):
        return self.data[1]

    def set_minor(self, val):
        self.data[1] = val

    minor = property(get_minor, set_minor)


class SequencerSpecificEvent(MetaEvent):
    name = "Sequencer Specific"
    metacommand = 0x7F
    length = "varlen"


class SysexF7Event(SysexEvent):
    statusmsg = 0xF7
    name = "SysExF7"
