from array import array
from style import setStyle
import os, sys, re
import ROOT

setStyle()
one = ROOT.TColor(2001,0.906,0.153,0.094)
two = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four =ROOT.TColor(2004,0.071,0.694,0.18)
five =ROOT.TColor(2005,0.388,0.098,0.608)
six=ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006]
#colors = setStyle()

def axis(name):  
    if   "thJitter"  in name : return "expected jitter [ps]"
    elif "slewrate"  in name : return "mean slew rate [mV/ns]" 
    elif "risetime"  in name : return "mean risetime [ns]" 
    elif "noise"     in name : return "baseline RMS [mV]" 
    elif "snr"       in name : return "signal to noise ratio" 
    elif "tresCFD"   in name : return "amplifier time res. (CFD) [ps]"
    elif "tresTOT"   in name : return "discrim. time res. (TOT) [ps]"
    elif "tresAmpTOT" in name: return "amplifier time res. (TOT) [ps]"
    elif "contribTOT" in name: return "TOT method contrib. [ps]"
    elif "contribDisc" in name: return "discrim. contrib.  [ps]"
    elif "contribTotal" in name: return "total discrim. contrib.[ps]"
    #elif "contribTOT" in name: return "#sqrt{ #sigma_{t}(amp. TOT)^2 - #sigma_{t}(amp. CFD)^2 } [ps]"
    #elif "contribDisc" in name: return "#sqrt{ #sigma_{t}(dis. TOT)^2 - #sigma_{t}(amp. TOT)^2 } [ps]"
    #elif "contribTotal" in name: return "#sqrt{ #sigma_{t}(dis. TOT)^2 - #sigma_{t}(amp. CFD)^2 } [ps]"
    elif "meanTOT"   in name : return "mean discriminator TOT [ns]"
    elif "meanAmpTOT"   in name : return "mean amplifier TOT [ns]"
    elif "charge"    in name : return "MPV collected charge [fC]"
    elif "dac"       in name : return "DAC threshold"
    elif "effDIS"    in name : return "discriminator efficiency"
    elif "amp"       in name : return "MPV amplitude [mV]" 
    elif "bias"      in name : return "bias voltage [V]"
    else : return ""

def xaxis(name):
    xstring = name.split("_v_")[1]
    return axis(xstring) 

def yaxis(name):
    ystring = name.split("_v_")[0]
    return axis(ystring) 

def colorindex(name):
    if "UCSC14"       in name : return 0
    elif "ETROC9ampLP"  in name : return 1
    elif "ETROC11ampLP" in name : return 2
    elif "ETROC9ampHP"  in name : return 3
    elif "ETROC11ampHP" in name : return 4
    elif "ETROC9disLP"  in name : return 1
    elif "ETROC11disLP" in name : return 2
    elif "ETROC9disHP"  in name : return 3
    elif "ETROC11disHP" in name : return 4
    elif "UCSC16"       in name : return 5
    else : return 0

def cosmetics(graph,ucsc=False,cold=False,dis=False):
    name = graph.GetName()
    index=colorindex(name)
    if "UCSC" in name : ucsc=True
    if "cold" in name : cold=True
    if "dis" in name: dis=True
    graph.SetLineColor(colors[index])
    graph.SetMarkerColor(colors[index])
    graph.SetMarkerSize(0.75)
    graph.SetMarkerStyle(20)
    size, style = 1.0, 20
    if ucsc : style += 1
    if cold : style += 4  
    if dis : style+=1
    graph.SetMarkerSize(size)
    graph.SetMarkerStyle(style)
    return 

def adjust(mgraph,gr_name):
    if "noiseRMS" in gr_name: mgraph.GetHistogram().GetYaxis().SetRangeUser(1.2,4.2)
    if "risetime" in gr_name: mgraph.GetHistogram().GetYaxis().SetRangeUser(0.5,2.1)
    if "slewrate" in gr_name: mgraph.GetHistogram().GetYaxis().SetRangeUser(40,640)
    if "snr"      in gr_name: mgraph.GetHistogram().GetYaxis().SetRangeUser(20,180)
    if "tresCFD_v_thJitter" in gr_name : mgraph.GetHistogram().GetYaxis().SetRangeUser(25,65)
    if "meanAmpTOT_" in gr_name : mgraph.GetHistogram().GetYaxis().SetRangeUser(2,8)
    if "meanTOT_" in gr_name : mgraph.GetHistogram().GetYaxis().SetRangeUser(2,8)
    if "tresTOT_v" in gr_name : mgraph.GetHistogram().GetYaxis().SetRangeUser(40,75)
    if "effDISC" in gr_name : mgraph.GetHistogram().GetYaxis().SetRangeUser(0,130)
    if "contrib" in gr_name : 
        mgraph.GetHistogram().GetYaxis().SetRangeUser(0,60)
        mgraph.GetHistogram().GetYaxis().SetNdivisions(505)


def plot_overlay(series, scans, labels, gr_name ):

    c = ROOT.TCanvas()
    c.SetGridy()
    c.SetGridx()

    mgraph = ROOT.TMultiGraph()
    left = True 
    if "tresTOT_v_charge"   in gr_name : left = False 
    if "tresTOT_v_bias"     in gr_name : left = False 
    if "tresTOT_v_meanTOT"  in gr_name : left = False 
    if "tresCFD_v_charge"   in gr_name : left = False 
    if "tresCFD_v_bias"     in gr_name : left = False 
    if "noiseRMS_v_bias"    in gr_name : left = False
    if "thJitter_v"         in gr_name : left = False
        
    if "dac" in series : leg = ROOT.TLegend(0.17,0.81,0.85,0.88)
    elif left : leg = ROOT.TLegend(0.17,0.61,0.56,0.88)
    else      : leg = ROOT.TLegend(0.5,0.61,0.85,0.88)
    leg.SetMargin(0.15)

    for i,scan in enumerate(scans):
        outfile = ROOT.TFile.Open("plots/scans/root/{}.root".format(scan))
        graph = outfile.Get("gr_{}_{}".format(scan,gr_name))
        cosmetics(graph)
        mgraph.Add(graph)
        leg.AddEntry(graph, labels[i] ,"EP")
    
    mgraph.SetTitle("; %s; %s"%(xaxis(gr_name),yaxis(gr_name)))
    mgraph.Draw("ALEP")
    adjust(mgraph,gr_name)
    leg.Draw() 
    c.Print("plots/series/{}_{}.pdf".format(series,gr_name))
    
    return

def get_series_results(series): 
    
    
    # Open series file, get scans 
    scans = []
    labels = []

    series_file = open("series/{}.txt".format(series),"r")
    for line in series_file: 
        if "#" in line[0]: continue

        scans.append(line.split("; ")[0])
        labels.append(line.split("; ")[1])
        print( line.split("; ")[0] ) 

    series_file.close()

    
    if "dac" in series: 
        plot_overlay(series, scans, labels, "tresTOT_v_dac")
        plot_overlay(series, scans, labels, "meanTOT_v_dac")
        plot_overlay(series, scans, labels, "effDISC_v_dac")
    elif "discriminator" in series: 
        plot_overlay(series, scans, labels, "tresTOT_v_bias")
        plot_overlay(series, scans, labels, "tresTOT_v_meanTOT")
        # plots versus bias
        plot_overlay(series, scans, labels, "noiseRMS_v_bias")
        plot_overlay(series, scans, labels, "tresTOT_v_bias")
        plot_overlay(series, scans, labels, "tresAmpTOT_v_bias")
        plot_overlay(series, scans, labels, "effDISC_v_bias")
        plot_overlay(series, scans, labels, "meanTOT_v_bias")
        plot_overlay(series, scans, labels, "meanAmpTOT_v_bias")
        # plots versus charge
        plot_overlay(series, scans, labels, "tresTOT_v_charge")
        plot_overlay(series, scans, labels, "tresAmpTOT_v_charge")
        plot_overlay(series, scans, labels, "effDISC_v_charge")
        plot_overlay(series, scans, labels, "meanTOT_v_charge")
        plot_overlay(series, scans, labels, "meanAmpTOT_v_charge")
        # plots versus amplifier
        plot_overlay(series, scans, labels, "tresTOT_v_tresCFD")
        plot_overlay(series, scans, labels, "tresAmpTOT_v_tresCFD")
        plot_overlay(series, scans, labels, "tresTOT_v_tresAmpTOT")
        plot_overlay(series, scans, labels, "meanTOT_v_meanAmpTOT")
        plot_overlay(series, scans, labels, "meanTOT_v_amp")
        plot_overlay(series, scans, labels, "meanAmpTOT_v_amp")
        # contributions
        plot_overlay(series, scans, labels, "contribTotal_v_amp")
        plot_overlay(series, scans, labels, "contribTOT_v_amp")
        plot_overlay(series, scans, labels, "contribDiscs_v_amp")
        plot_overlay(series, scans, labels, "contribTotal_v_charge")
        plot_overlay(series, scans, labels, "contribTOT_v_charge")
        plot_overlay(series, scans, labels, "contribDiscs_v_charge")
        plot_overlay(series, scans, labels, "contribTotal_v_bias")
        plot_overlay(series, scans, labels, "contribTOT_v_bias")
        plot_overlay(series, scans, labels, "contribDiscs_v_bias")

    
    else : #amplifer 
        # v bias
        plot_overlay(series, scans, labels, "amp_v_bias")
        plot_overlay(series, scans, labels, "charge_v_bias")
        plot_overlay(series, scans, labels, "chargePre_v_bias")
        plot_overlay(series, scans, labels, "slewrate_v_bias")
        plot_overlay(series, scans, labels, "risetime_v_bias")
        plot_overlay(series, scans, labels, "noiseRMS_v_bias")
        plot_overlay(series, scans, labels, "snr_v_bias")
        plot_overlay(series, scans, labels, "tresCFD_v_bias")
        plot_overlay(series, scans, labels, "thJitter_v_bias")
        # v charge
        plot_overlay(series, scans, labels, "tresCFD_v_charge")
        plot_overlay(series, scans, labels, "thJitter_v_charge")
        plot_overlay(series, scans, labels, "slewrate_v_charge")
        plot_overlay(series, scans, labels, "risetime_v_charge")
        plot_overlay(series, scans, labels, "snr_v_charge")
        # test
        plot_overlay(series, scans, labels, "tresCFD_v_thJitter")
        plot_overlay(series, scans, labels, "charge_v_biasShift")
        # saturation?
        plot_overlay(series, scans, labels, "slewrate_v_amp")
        plot_overlay(series, scans, labels, "risetime_v_amp")

    return 

def get_series():
    # Loop through configurations 
    series_list = open("series/series.txt","r")
    for i,line in enumerate(series_list): 
     
        # for tmp debugging
        #if i > 0: break 
        #if "156" not in line: continue

        if "#" in line: continue
        series = line.strip()
        print(series)
        get_series_results(series)

# Main
get_series()
