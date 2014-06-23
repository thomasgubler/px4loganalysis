#!/usr/bin/env python
import argparse
import os
import subprocess
__author__ = "Thomas Gubler"
__license__ = "BSD"
__email__ = "thomasgubler@gmail.com"


class LogAnalyzer():
    """A class that helps anaylze logs"""

    def __init__(self, args):
        """Constructor"""
        self.filenames = args.filenames
        if args.legend:
            self.legendCmd = ''.join(["--legend=\"", args.legend, '\"'])
        else:
            self.legendCmd = ''
        self.mavgraph = "~/src/mavlink/pymavlink/tools/mavgraph.py"
        self.mavgraphOptions = "--flightmode=px4"
        self.plots = {"Altitude_Thrust":
                      ("GPS.Alt SENS.BaroAlt GPOS.Alt GPSP.Alt "
                       "500.0+10.0*ATSP.ThrustSP"),
                      "Altitude": ("GPS.Alt SENS.BaroAlt GPOS.Alt GPSP.Alt "
                                   "SENS.BaroAlt"),
                      "Roll": "ATT.Roll ATSP.RollSP",
                      "Pitch": "ATT.Pitch ATSP.PitchSP",
                      "Lat": "GPS.Lat GPOS.Lat GPSP.Lat",
                      "Lon": "GPS.Lon GPOS.Lon GPSP.Lon"}

    def generatePlots(self, filename, dirname):
        """produce plots for filename in dirname"""
        print(' '.join(["Analyzing ", filename]))

        processes = []
        for plotTitle, plotFields in self.plots.iteritems():
            plotFileName = ''.join([filename, '_', plotTitle, ".png"])
            output = ''.join(["--output=", dirname, "/", plotFileName])
            cmd = ' '.join(["python2", self.mavgraph, self.mavgraphOptions,
                            self.legendCmd, output, plotFields, filename])
            processes.append(subprocess.Popen(cmd, shell=True))

        # wait for the mavgraph processes to finish before continuing
        for p in processes:
            p.wait()

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
    parser.add_argument('--legend', dest='legend', default='lower right',
                        action='store', help='legend position (matplotlib)')
    parser.add_argument(dest='filenames', default='', action='store',
                        help='Filenames of logfiles', nargs='+')

    args = parser.parse_args()

    analyzer = LogAnalyzer(args)
    analyzer.analyze()
