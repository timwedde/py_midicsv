### CLI ###
import click

from .csvmidi import parse as csv_to_midi

### Local ###
from .midi.fileio import FileWriter
from .midicsv import parse as midi_to_csv


@click.command()
@click.option("-n", "--nostrict", is_flag=True, help="Do not fail on parse/validation errors.")
@click.option("-u", "--usage", is_flag=True, help="Print usage information (NOOP)")
@click.option("-v", "--verbose", is_flag=True, help="Print debug information (NOOP)")
@click.argument("input_file", type=click.File("rb"))
@click.argument("output_file", type=click.File("w"))
def midicsv(usage, nostrict, verbose, input_file, output_file):
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

    Some arguments are kept for backwards-compatibility with the original midicsv tooling.
    These are marked as NOOP in this command line interface.
    """
    csv_data = midi_to_csv(input_file, not nostrict)
    output_file.writelines(csv_data)


@click.command()
@click.option("-n", "--nostrict", is_flag=True, help="Do not fail on parse/validation errors.")
@click.option("-u", "--usage", is_flag=True, help="Print usage information (NOOP)")
@click.option("-v", "--verbose", is_flag=True, help="Print debug information (NOOP)")
@click.option("-z", "--strict-csv", is_flag=True, help="Raise exceptions on CSV errors (NOOP)")
@click.option("-x", "--no-compress", is_flag=True, help="Do not compress status bytes (NOOP)")
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("wb"))
def csvmidi(usage, nostrict, verbose, strict_csv, no_compress, input_file, output_file):
    """Convert CSV files to MIDI files.

    csvmidi reads a CSV file in the format written by midicsv and creates
    the equivalent standard MIDI file.

    Specify an input file and an output file to process it.
    Either argument can be stdin/stdout.

    Some arguments are kept for backwards-compatibility with the original csvmidi tooling.
    These are marked as NOOP in this command line interface.
    """
    midi_data = csv_to_midi(input_file, not nostrict)
    writer = FileWriter(output_file)
    writer.write(midi_data)
