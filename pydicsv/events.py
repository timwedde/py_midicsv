from midi.events import *

midi_to_csv_map = {
    NoteOffEvent: "Note_off_c",
    NoteOnEvent: "Note_on_c",
    AfterTouchEvent: "Poly_aftertouch_c",
    ControlChangeEvent: "Control_c",
    ProgramChangeEvent: "Program_c",
    ChannelAfterTouchEvent: "Channel_aftertouch_c",
    PitchWheelEvent: "Pitch_bend_c",
    SequenceNumberMetaEvent: "Sequence_number",
    ProgramNameEvent: "Program_name_t",
    TextMetaEvent: "Text_t",
    CopyrightMetaEvent: "Copyright_t",
    TrackNameEvent: "Title_t",
    InstrumentNameEvent: "Instrument_name_t",
    LyricsEvent: "Lyric_t",
    MarkerEvent: "Marker_t",
    CuePointEvent: "Cue_point_t",
    ChannelPrefixEvent: "Channel_prefix",
    PortEvent: "MIDI_port",
    EndOfTrackEvent: "End_track",
    SomethingEvent: "Something",
    TrackLoopEvent: "Loop_track",
    SetTempoEvent: "Tempo",
    SmpteOffsetEvent: "SMPTE_offset",
    TimeSignatureEvent: "Time_signature",
    KeySignatureEvent: "Key_signature",
    SequencerSpecificEvent: "Sequencer_specific",
    SysexEvent: "System_exclusive",
}

csv_to_midi_map = {v: k for k, v in midi_to_csv_map.items()}
