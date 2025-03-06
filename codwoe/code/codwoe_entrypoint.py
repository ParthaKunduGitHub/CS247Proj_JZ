# Summary:
# This script serves as a demonstration tool for running various baseline tasks in an NLP context.
# It allows users to execute specific commands like "defmod" (definition modeling), "revdict" (reverse dictionary),
# "check-format" (verify submission file format), and "score" (evaluate submission results).
# By utilizing modular design and command-line arguments, the script enables participants to interact with the
# corresponding modules (`defmod`, `revdict`, `check_output`, and `score`) seamlessly.

# Importing necessary modules for each functionality
import defmod  # Module for definition modeling
import revdict  # Module for reverse dictionary tasks
import check_output  # Module for verifying submission file formats
import score  # Module for evaluating submissions

# Main execution block
if __name__ == "__main__":
    # Importing argparse for command-line argument handling
    import argparse

    # Creating a main argument parser
    parser = argparse.ArgumentParser(description="demo script for participants")
    
    # Adding subparsers to handle different commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Adding "defmod" subcommand for definition modeling
    parser_defmod = defmod.get_parser(
        parser=subparsers.add_parser(
            "defmod", help="run a definition modeling baseline"
        )
    )

    # Adding "revdict" subcommand for reverse dictionary tasks
    parser_revdict = revdict.get_parser(
        parser=subparsers.add_parser(
            "revdict", help="run a reverse dictionary baseline"
        )
    )

    # Adding "check-format" subcommand for verifying submission file formats
    parser_check_output = check_output.get_parser(
        parser=subparsers.add_parser(
            "check-format", help="check the format of a submission file"
        )
    )

    # Adding "score" subcommand for evaluating a submission
    parser_score = score.get_parser(
        parser=subparsers.add_parser("score", help="evaluate a submission")
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    print(f"Command chosen: {args.command}")  # Print the chosen command for clarity

    # Execute the appropriate functionality based on the chosen command
    if args.command == "defmod":
        print("Running definition modeling baseline...")
        defmod.main(args)  # Call the main function from the defmod module
    elif args.command == "revdict":
        print("Running reverse dictionary baseline...")
        revdict.main(args)  # Call the main function from the revdict module
    elif args.command == "check-format":
        print("Checking the format of the submission file...")
        check_output.main(args.submission_file)  # Call the main function from the check_output module
    elif args.command == "score":
        print("Evaluating the submission...")
        score.main(args)  # Call the main function from the score module
