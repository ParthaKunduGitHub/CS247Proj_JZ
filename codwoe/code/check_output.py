# Summary: 
# This script verifies the format and structure of a submission JSON file for NLP tasks.
# It performs checks on the file to ensure proper track identification (e.g., "revdict" or "defmod"),
# valid language codes, unique item IDs, and the presence of required fields (e.g., "id", "gloss").
# It logs details of any issues found and validates the submission for further processing.

import argparse  # For handling command-line arguments
import collections  # For creating named tuple structures
import json  # For loading JSON data
import logging  # For setting up logging functionality
import pathlib  # For handling file paths
import sys  # For interacting with the system for inputs/outputs

# Set up a logger for the script to output debug and error information
logger = logging.getLogger(pathlib.Path(__file__).name)
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG for detailed information
handler = logging.StreamHandler(sys.stdout)  # Direct log output to the console
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
logger.addHandler(handler)  # Add the handler to the logger

# Function to parse command-line arguments
def get_parser(
    parser=argparse.ArgumentParser(
        description="Verify the output format of a submission"
    ),
):
    # Add an argument for the path to the submission file
    parser.add_argument("submission_file", type=pathlib.Path, help="file to check")
    return parser

# Main function to verify the submission file
def main(filename):
    try:
        # Attempt to open and load the JSON file
        with open(filename, "r") as istr:
            items = json.load(istr)
        print(f"File '{filename}' successfully loaded. Found {len(items)} items.")
    except Exception as e:
        # If the file cannot be opened, raise a ValueError
        print(f"Error: {e}")
        raise ValueError(f'File "{filename}": could not open, submission will fail.')
    else:
        for item in items:
            # Check if each item contains an "id" key
            if "id" not in item:
                raise ValueError(
                    f'File "{filename}": one or more items do not contain an id, submission will fail.'
                )
        # Extract and sort item IDs
        ids = sorted([item["id"] for item in items])
        print(f"Extracted IDs: {ids}")
        ids = [i.split(".") for i in ids]  # Split IDs by periods to process further
        langs = {i[0] for i in ids}  # Extract the language from the first part of the ID
        print(f"Languages found: {langs}")
        if len(langs) != 1:
            raise ValueError(
                f'File "{filename}": ids do not identify a unique language, submission will fail.'
            )
        tracks = {i[-2] for i in ids}  # Extract the track from the second-to-last part of the ID
        print(f"Tracks found: {tracks}")
        if len(tracks) != 1:
            raise ValueError(
                f'File "{filename}": ids do not identify a unique track, submission will fail.'
            )
        track = next(iter(tracks))
        print(f"Track identified: {track}")
        if track not in ("revdict", "defmod"):
            raise ValueError(
                f'File "{filename}": unknown track identified {track}, submission will fail.'
            )
        lang = next(iter(langs))
        print(f"Language identified: {lang}")
        if lang not in ("en", "es", "fr", "it", "ru"):
            raise ValueError(
                f'File "{filename}": unknown language {lang}, submission will fail.'
            )
        serials = list(sorted({int(i[-1]) for i in ids}))  # Extract and sort serial numbers
        print(f"Serial numbers found: {serials}")
        if serials != list(range(1, len(ids) + 1)):
            raise ValueError(
                f'File "{filename}": ids do not identify all items in dataset, submission will fail.'
            )
        if track == "revdict":
            # Extract vector architectures for "revdict" track
            vec_archs = set(items[0].keys()) - {
                "id",
                "gloss",
                "word",
                "pos",
                "concrete",
                "example",
                "f_rnk",
                "counts",
                "polysemous",
            }
            print(f"Vector architectures found: {vec_archs}")
            if len(vec_archs) == 0:
                raise ValueError(
                    f'File "{filename}": no vector architecture was found, revdict submission will fail.'
                )
            for item in items:
                if not all(v in item for v in vec_archs):
                    raise ValueError(
                        f'File "{filename}": some items do not contain all the expected vectors, revdict submission will fail.'
                    )
            if len(vec_archs - {"sgns", "char", "electra"}):
                raise ValueError(
                    f'File "{filename}": unknown vector architecture(s), revdict submission will fail.'
                )
        if track == "defmod" and any("gloss" not in i for i in items):
            raise ValueError(
                f'File "{filename}": some items do not contain a gloss, defmod submission will fail.'
            )

        # Compose a success message if all checks pass
        ok_message = (
            f'File "{filename}": no problems were identified.\n'
            + f"The submission will be understood as follows:\n"
            + f"\tSubmission on track {track} for language {lang}, {len(ids)} predictions.\n"
        )
        if track == "revdict":
            vec_archs = tuple(sorted(vec_archs))
            ok_message += (
                f'\tSubmission predicts these embeddings: {", ".join(vec_archs)}.'
            )
        else:
            vec_archs = None
        logger.debug(ok_message)  # Log the success message
        print(ok_message)  # Print the success message to the console
        # Create a summary of the checks
        CheckSummary = collections.namedtuple(
            "CheckSummary", ["filename", "track", "lang", "vec_archs"]
        )
        return CheckSummary(filename, track, lang, vec_archs)

# Entry point of the script
if __name__ == "__main__":
    print("Starting submission file verification...")
    summary = main(get_parser().parse_args().submission_file)
    print(f"Verification completed: {summary}")
