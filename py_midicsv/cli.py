### CLI ###
import click

### Local ###
from .midi.fileio import FileWriter
from .csvmidi import parse as csv_to_midi
from .midicsv import parse as midi_to_csv


@click.command()
@click.argument("input_file", type=click.File("rb"))
@click.argument("output_file", type=click.File("w"))
def midicsv(input_file, output_file):
    """Convert MIDI files to CSV files.

    midicsv reads a standard MIDI file and decodes it into a CSV file
    which preserves all the information in the MIDI file.
    The ASCII CSV file may be loaded into a spreadsheet or database application,
    or processed by a program to transform the MIDI data (for example, to key transpose
    a composition or extract a track from a multi-track sequence).
    A CSV file in the format created by midicsv may be converted back into a standard
    MIDI file with the csvmidi program.

    Specify an input file and an output file to process it.
    Either argument can be stdin/stdout.
    """
    csv_data = midi_to_csv(input_file)
    output_file.writelines(csv_data)


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("wb"))
def csvmidi(input_file, output_file):
    """Convert CSV files to MIDI files.

    csvmidi reads a CSV file in the format written by midicsv and creates
    the equivalent standard MIDI file.

    Specify an input file and an output file to process it.
    Either argument can be stdin/stdout.
    """
    midi_data = csv_to_midi(input_file)
    writer = FileWriter(output_file)
    writer.write(midi_data)
