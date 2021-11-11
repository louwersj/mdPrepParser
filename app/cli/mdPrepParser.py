# mdPrepParser is originally intended to prepare a template md document and populate this with boilerplate .md files
# from a central library. However, mdPrepParser is very usable when you create multiple .md files and want to
# dynamically include them into a single md file by parsing the main document with mdPrepParser.
#
# When writing your .md file and you want to include another .md file do use the below shown annotation to do so;
# [include-md][./someFileName.md]
#
# Roadmap / improvements
# - at current we only support one level deep nesting, meaning you can only include/link .md files in the main file
#   which is provided to the mdPrepParser with the -i parameter. In the future is should support deeper nesting.

import sys
import getopt
import os.path


def prepParser(sourceFile, targetFile):
    print("starting MD Prep Parser (mdPrepParser)")

    source = open(sourceFile, "rt")
    target = open(targetFile, "wt")
    line_number = 0
    for line in source:
        line_number += 1
        if "[include-md]" in line:
            cleanLine = (line.replace("[include-md]", ""))
            includeFileName = cleanLine[cleanLine.find('[')+1:cleanLine.find(']')]

            includeFile = open(includeFileName, "rt")
            for includeFileLine in includeFile:
                if (len(includeFileLine)) == 1:
                    target.write("\n")
                else:
                    target.write(includeFileLine + "\n")
        else:
            target.write(line)


def main(argv):
    """
    Function main will validate if all parameters are provided and in addition it will verify if the input file is
    available. If the input file is not available it will raise an exception.

    :param argv: Takes the command line arguments as in -> sys.argv[1:]
    """
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # check if parameter is provided for inputfile and outputfile
    if len(inputfile) < 1:
        print("Error - No input file defined. Use -h for help")
        sys.exit(2)
    if len(outputfile) < 1:
        print("Error - No output file defined. Use -h for help")
        sys.exit(2)

    # check if the provided input file is available. If not we raise an error.
    if os.path.exists(inputfile) is False:
        print("Error - input file not found")
        sys.exit(2)

    # check if the output file already exists, if so we raise an error
    if os.path.exists(outputfile):
        print("Error - output file already exist")
        sys.exit(2)

    # if all the checks are passed we call the actual prepParses function wiht the needed parameters.
    prepParser(inputfile, outputfile)


if __name__ == '__main__':
    main(sys.argv[1:])
