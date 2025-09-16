import argparse
import os
import sys


# Parser functions that validate the format and type of the data
def parse_step(value):
    if value == "build":
        return value
    elif value == "upload":
        return value
    elif value == "all":
        return value
    else:
        raise argparse.ArgumentTypeError(f"the value {value} is not recognized. ")


def parse_path(value):
    return value



def parse_arguments():
    """Parse and validate command-line arguments"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="iMarina-load")

    parser.add_argument("-s", "--step", type=parse_step, required=False, default="all",
                        help="Step to perform. Valid options are build, upload and all")
    parser.add_argument("-u", "--upload", "--upload-path", type=parse_path, required=False,
                        help="Path of the file to upload")

    #new arguments for --countries-dict , --jobs-dict , --imarina-input , --a3-input
    parser.add_argument("--countries-dict", type=parse_path, required=False, default=os.path.join(root_dir, "input", "countries.xlsx"),
                        help="Path of the countries dictionary file(.xlsx)")

    parser.add_argument(
                       "--jobs-dict", type=parse_path, required=False, default=os.path.join(root_dir, "input", "Job_Descriptions.xlsx"),
                        help="Path of the jobs dictionary file(.xlsx)")

    parser.add_argument("--imarina-input", type=parse_path, required=False, default=os.path.join(root_dir, "input", "iMarina.xlsx"),
                         help="Path of the iMarina input file(.xlsx)")

    parser.add_argument("--a3-input", type=parse_path, required=False, default=os.path.join(root_dir, "input" , "A3.xlsx"),
                        help="Path to A3 input file(.xlsx)")

    args = parser.parse_args()
    return args


def process_parse_arguments():
    common = ("Error parsing arguments. Program aborting. The arguments are: "
              + str(sys.argv) + "The program is in a uninitialized state and cannot proceed. This error will be "
                                "notified to the admin via log file. We can't create log file in user author folder "
                                "because user author could not be parsed.")
    try:
        args = parse_arguments()

    except argparse.ArgumentTypeError as e:
        print("Arguments could not have been parsed. Internal error is " + e.__str__())
        print(common)
        exit(5)

    if args.step != "upload" and args.upload is not None:
        print("Supplied an upload path but upload path can only be used in conjunction with --step upload")
        exit(1)

    return args
