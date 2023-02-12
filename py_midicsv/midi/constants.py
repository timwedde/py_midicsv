OCTAVE_MAX_VALUE = 12
OCTAVE_VALUES = list(range(OCTAVE_MAX_VALUE))

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
WHITE_KEYS = [0, 2, 4, 5, 7, 9, 11]
BLACK_KEYS = [1, 3, 6, 8, 10]
NOTE_PER_OCTAVE = len(NOTE_NAMES)
NOTE_VALUES = list(range(OCTAVE_MAX_VALUE * NOTE_PER_OCTAVE))
NOTE_NAME_MAP_FLAT = {}
NOTE_VALUE_MAP_FLAT = []
NOTE_NAME_MAP_SHARP = {}
NOTE_VALUE_MAP_SHARP = []

for value in range(128):
    noteidx = value % NOTE_PER_OCTAVE
    octidx = value / OCTAVE_MAX_VALUE
    name = NOTE_NAMES[noteidx]
    if len(name) == 2:
        # sharp note
        flat = NOTE_NAMES[noteidx + 1] + "b"
        NOTE_NAME_MAP_FLAT[f"{flat}_{octidx}"] = value
        NOTE_NAME_MAP_SHARP[f"{name}_{octidx}"] = value
        NOTE_VALUE_MAP_FLAT.append(f"{flat}_{octidx}")
        NOTE_VALUE_MAP_SHARP.append(f"{name}_{octidx}")
        globals()["{}_{}".format(name[0] + "#", octidx)] = value
        globals()[f"{flat}_{octidx}"] = value
    else:
        NOTE_NAME_MAP_FLAT["%s_%d" % (name, octidx)] = value
        NOTE_NAME_MAP_SHARP["%s_%d" % (name, octidx)] = value
        NOTE_VALUE_MAP_FLAT.append("%s_%d" % (name, octidx))
        NOTE_VALUE_MAP_SHARP.append("%s_%d" % (name, octidx))
        globals()["%s_%d" % (name, octidx)] = value

BEATNAMES = [
    "whole",
    "half",
    "quarter",
    "eighth",
    "sixteenth",
    "thirty-second",
    "sixty-fourth",
]
BEATVALUES = [4, 2, 1, 0.5, 0.25, 0.125, 0.0625]
WHOLE = 0
HALF = 1
QUARTER = 2
EIGHTH = 3
SIXTEENTH = 4
THIRTYSECOND = 5
SIXTYFOURTH = 6

DEFAULT_MIDI_HEADER_SIZE = 14
