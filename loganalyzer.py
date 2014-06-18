#!/usr/bin/env python
import argparse
import os
import subprocess


class LogAnalyzer():
    """A class that helps anaylze logs"""

    def __init__(self, filenames):
        """Constructor"""
        self.filenames = filenames
        self.mavgraph = "~/src/mavlink/pymavlink/tools/mavgraph.py"
        self.plots = {"Altitude": "GPS.Alt SENS.BaroAlt GPOS.Alt GPSP.Alt",
                      "Roll": "ATT.Roll ATSP.RollSP"}

    def generatePlots(self, filename, dirname):
        """produce plots for filename in dirname"""
        print(' '.join(["Analyzing ", filename]))

        for plotTitle, plotFields in self.plots.iteritems():
            plotFileName = ''.join([filename, '_', plotTitle, ".png"])
            output = "--output=" + dirname + "/" + plotFileName
            subprocess.Popen(' '.join(["python2", self.mavgraph, output,
                                      plotFields, filename]), shell=True)

    def createOutputdir(self, filename):
        """Creates the output directory given the filename"""
        dirname = filename[:-4]
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        else:
            print(' '.join([dirname, "already exists, continuing..."]))

        return dirname

    def analyze(self):
        """runs analysis for each file in filenams"""
        for f in self.filenames:
            # create output dir
            dirname = self.createOutputdir(f)

            # generate a set of plots
            self.generatePlots(f, dirname)


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Log analyzation tool')
    parser.add_argument(dest='filenames', default='', action='store',
                        help='Filenames of logfiles', nargs='+')

    args = parser.parse_args()

    analyzer = LogAnalyzer(args.filenames)
    analyzer.analyze()