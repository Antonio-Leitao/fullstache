"""main module for fullstache module

functions here should really just take care of files and directory handling everything else should be on compile

"""


import os
import argparse
from compiler import Fullstache
from loaders import loadParser, loadTemplate, loadUserData


def buildCompiler(data_path):
    fullstache_parser = loadParser(
        "fullstache.grammar.txt",
        transformer=Fullstache(user_data=loadUserData(data_path)),
    )
    return fullstache_parser


def colapseFile(file_path, fullstache_parser):
    # get user data

    # load template given directory
    template = loadTemplate(file_path)
    #colapsed = fullstache_parser.parse(template)

    with open("__fullstache_cache__.txt", "w") as f:
         f.write(template)

     # collapse template with fullstache
    with open("__fullstache_cache__.txt") as f:
         colapsed = fullstache_parser.parse(f.read())

    with open(file_path, "w") as f:
        f.write(colapsed)


def cycleDir(target, exclude, only):
    if only is not None:
        for r, d, f in os.walk(target):
            for name in f:
                if name in only:
                    # you can also add target to get full path
                    yield {"name": name, "path": os.path.join(r, name)}

    else:
        for r, d, f in os.walk(target):
            for name in f:
                if name not in exclude:
                    # you can also add target to get full path
                    yield {"name": name, "path": os.path.join(r, name)}


def main(target, data, only, exclude, scan):

    fullstache_parser = buildCompiler(data)

    targets = cycleDir(
        target=target,
        exclude=exclude if exclude is not None else [],
        only=only,
    )

    if scan is None:
        for element in targets:
            print(f"collapsing file: {element['name']}...")
            colapseFile(element["path"], fullstache_parser)
            print("done")
    else:
        for element in targets:
            print(f"scanning file: {element['name']}...")
            # colapseFile(element.path,fullstache_parser)
            print("done")


def cli_main():
    """{FULLSTACHE} minimal logic templating language.

    Colapse template given data, or scan template to create config file
    """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "target",
        help="""A project directory.

        The dir with files in which fullstache is going to act upon weather to collapse,
        (default behavior) or to scan if the [-s] flag is provided. To target only
        specific files, pass them into [-o] [--only] flag. To exclude files from 
        the action pass them with the [-x] or [--exclude] flag.
        """,
    )
    parser.add_argument(
        "-d",
        "--data",
        help="""
        Path to json file with user data necessary for collapsing template. Required
        unless [-s] [--scan] is passed.
        """,
        metavar="\b",
    )

    parser.add_argument(
        "-o",
        "--only",
        help="""
        Perform an action (scan/collapse) exlusively over these files. Recommended behaviour.
        """,
        metavar="\b",
        nargs="+",
    )

    parser.add_argument(
        "-x",
        "--exclude",
        help="""
        File(s) to exlude from template collapsing or scanning. Improves performance minimally.
        """,
        metavar="\b",
        nargs="+",
    )

    parser.add_argument(
        "-s",
        "--scan",
        help="""
        Scans file(s) for fullstache syntax. Addes found variables in fullstache.config file in root
        of directory. If there is already a file, updates it.
        """,
        metavar="\b",
    )
    args = vars(parser.parse_args())

    ####ERROR HANDLING#####

    # can't collapse withoutdata
    if (args["scan"] is not None) and (args["data"] is None):
        parser.error("No user data data for collapsing")

    # target needs to be a valid directory
    if not os.path.isdir(args["target"]):
        parser.error(f'The directory {args["target"]} does not exist!')

    # cant exclude and include same file
    if (args["only"] is not None) and (args["exclude"] is not None):
        intersect = [f for f in args["only"] if f in args["exclude"]]
        if len(intersect) > 0:
            s = "\n"
            for f in intersect:
                s += f"\t - {f} \n"
            parser.error("File can't be included and excluded at the same time:" + s)

    main(**args)


if __name__ == "__main__":
    # main(sys.argv[1])
    cli_main()

    # template = loadTemplate("template.txt")

    # print(parser.parse(template).pretty())
