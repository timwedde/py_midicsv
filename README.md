# py_midicsv

[![CircleCI](https://circleci.com/gh/timwedde/py_midicsv.svg?style=svg)](https://circleci.com/gh/timwedde/py_midicsv)
[![Downloads](https://pepy.tech/badge/py-midicsv)](https://pepy.tech/project/py-midicsv)

A Python library inspired by the [midicsv](http://www.fourmilab.ch/webtools/midicsv/) tool created by John Walker. Its main purpose is to bidirectionally convert between the binary `MIDI` format and a human-readable interpretation of the contained data in text format, expressed as `CSV`.
If you found this library, you probably already know why you need it.


## Disclaimer

This library is currently in Beta. This means that the interface might change and that the encoding scheme is not yet finalised. Expect slight inconsistencies.


## Installation

`py_midicsv` can be installed via pip:
```bash
$ pip install py_midicsv
```

Alternatively you can build the package by cloning this repository and installing via [poetry](https://github.com/sdispater/poetry):
```bash
$ git clone https://github.com/timwedde/py_midicsv.git
$ cd py_midicsv/
$ poetry install
```


## Usage

```python
import py_midicsv as pm

# Load the MIDI file and parse it into CSV format
csv_string = pm.midi_to_csv("example.mid")

# Parse the CSV output of the previous command back into a MIDI file
midi_object = pm.csv_to_midi(csv_string)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)
```

## Differences

This library adheres as much as possible to how the original library works, however generated files are not guaranteed to be entirely identical when compared bit-by-bit.
This is mostly due to the handling of meta-event data, especially lyric events, since the encoding scheme has changed. The original library did not encode some of the characters in the Latin-1 set, while this version does.
