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
        self.plots = {}
        #self.plots["Altitude_Thrust"] = ("GPS.Alt SENS.BaroAlt GPOS.Alt GPSP.Alt "
                       #"500.0+10.0*ATSP.ThrustSP")
        #self.plots["Altitude"] = ("GPS.Alt SENS.BaroAlt GPOS.Alt GPSP.Alt "
                                #"SENS.BaroAlt")
        #self.plots["Roll"] = "ATT.Roll ATSP.RollSP"
        #self.plots["Pitch"] =  "ATT.Pitch ATSP.PitchSP"
        #self.plots["Lat"] = "GPS.Lat GPOS.Lat GPSP.Lat"
        #self.plots["Lon"] = "GPS.Lon GPOS.Lon GPSP.Lon"
        #self.plots["Estimator_status"] = ("EST0.nStat EST0.fNaN EST0.fHealth "
                                           #"EST0.fTOut")
        #self.plots["TECS_Outer_Loop"] = ("TECS.ASP TECS.A TECS.AF "
                                          #" 100.0*TECS.FSP"
                                          #" 100.0*TECS.F 100.0*TECS.FF"
                                          #" 10.0*TECS.AsSP"
                                          #" 10.0*TECS.As"
                                          #" 10.0*TECS.AsF 10.0*TECS.AsDSP"
                                          #" 10.0*TECS.AsD 100.0*ATSP.ThrustSP"
                                          #" 180.0/pi*ATSP.PitchSP")
        #self.plots["TECS_Inner_Loop"] = ("TECS.TERSP TECS.TER TECS.EDRSP "
                                          #"TECS.EDR TECS.M")
        #self.plots["Landing"] = ("GPOS.Alt GPSP.Alt TECS.AF "
                                  #"TECS.ASP GPOS.TALT 'GPOS.TALT + 4.0' "
                                 #"'GPOS.Alt-DIST.Bottom'")
        engineFailure = "'ATTC.Thrust>0.5 and BATT.C/ATTC.Thrust<5'"
        self.plots["Motor"] = ("'40.0*ATTC.Thrust' BATT.C " + engineFailure)
        self.plots["Motor2"] = ("'0.1*BATT.C/ATTC.Thrust' ATTC.Thrust "
                                + engineFailure)

    def generatePlots(self, filename, dirname):
        """produce plots for filename in dirname"""
        print(' '.join(["Analyzing ", filename]))

        processes = []
        for plotTitle, plotFields in self.plots.items():
            plotFileName = ''.join([filename, '_', plotTitle, ".png"])
            if args.showgui:
                output = ''
            else:
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
    parser.add_argument('--legend', dest='legend', default='best',
                        action='store', help='legend position (matplotlib)')
    parser.add_argument('--gui', dest='showgui', default=False,
                        action='store_true', help='show gui plot')
    parser.add_argument(dest='filenames', default='', action='store',
                        help='Filenames of logfiles', nargs='+')

    args = parser.parse_args()

    analyzer = LogAnalyzer(args)
    analyzer.analyze()
