# py_midicsv
A Python library inspired by the midicsv tool (originally found [here](http://www.fourmilab.ch/webtools/midicsv/)).

## Disclaimer
This library is currently in Beta. This means that the interface might change and that the encoding scheme is not yet finalised. Expect slight inconsistencies.

## Installation
py_midicsv is available from PyPI, so you can install via `pip`:
```bash
$ pip install py_midicsv
```

## Usage
```python
import py_midicsv

# Load the MIDI file and parse it into CSV format
csv_string = py_midicsv.midi_to_csv("example.mid")

# Parse the CSV output of the previous command back into a MIDI file
midi_object = py_midicsv.csv_to_midi(csv_string)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = py_midicsv.FileWriter(output_file)
    midi_writer.write(midi_object)
```

## Differences
This library adheres as much as possible to how the original library works, however generated files are not guaranteed to be entirely identical when compared bit-by-bit.  
This is mostly due to the handling of meta-event data, especially lyric events, since the encoding scheme has changed. The original library did not encode some of the characters in the Latin-1 set, while this version does.
