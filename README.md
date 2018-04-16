# pydicsv
A Python library inspired by the midicsv tool (originally found [here](http://www.fourmilab.ch/webtools/midicsv/)).

# THIS LIBRARY IS CURRENTLY NOT FUNCTIONAL!
This library is currently under development and will be subject to massive changes as well as bugs and errors during this time.

## Differences
This library adheres as much as possible to how the original library works, however generated files are not guaranteed to be entirely identical when compared bit-by-bit.  
This is mostly due to the handling of meta-event data, especially lyric events, since the encoding scheme has changed. The original library did not encode some of the characters in the Latin-1 set, while this version does.
