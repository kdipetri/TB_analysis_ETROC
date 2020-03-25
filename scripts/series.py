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
    if   "amp"       in name : return "MPV amplitude [mV]" 
    elif "slewrate"  in name : return "mean slew rate [mV/ns]" 
    elif "risetime"  in name : return "mean risetime [ns]" 
    elif "noise"     in name : return "baseline RMS [mV]" 
    elif "snr"       in name : return "signal to noise ratio" 
    elif "tresCFD"   in name : return "time resolution (CFD) [ps]"
    elif "charge"    in name : return "integrated charge [fC]"
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
    elif "UCSC16"       in name : return 5
    else : return 0

def cosmetics(graph,ucsc=False,cold=False):
    name = graph.GetName()
    index=colorindex(name)
    if "UCSC" in name : ucsc=True
    if "cold" in name : cold=True
    graph.SetLineColor(colors[index])
    graph.SetMarkerColor(colors[index])
    graph.SetMarkerSize(0.75)
    graph.SetMarkerStyle(20)
    size, style = 1.0, 20
    if ucsc : style += 1
    if cold : style += 4  
    graph.SetMarkerSize(size)
    graph.SetMarkerStyle(style)
    return 


def plot_overlay(series, scans, labels, gr_name ):

    c = ROOT.TCanvas()
    c.SetGridy()
    c.SetGridx()

    mgraph = ROOT.TMultiGraph()
    left = True 
    if "tresCFD_v_charge"  in gr_name : left = False 
    if "tresCFD_v_bias" in gr_name : left = False 
        
    if left : leg = ROOT.TLegend(0.17,0.62,0.56,0.86)
    else    : leg = ROOT.TLegend(0.5,0.62,0.85,0.86)
    leg.SetMargin(0.15)

    for i,scan in enumerate(scans):
        outfile = ROOT.TFile.Open("plots/scans/root/{}.root".format(scan))
        graph = outfile.Get("gr_{}_{}".format(scan,gr_name))
        cosmetics(graph)
        mgraph.Add(graph)
        leg.AddEntry(graph, labels[i] ,"EP")
    
    mgraph.SetTitle("; %s; %s"%(xaxis(gr_name),yaxis(gr_name)))
    mgraph.Draw("AEP")
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

    plot_overlay(series, scans, labels, "amp_v_bias")
    plot_overlay(series, scans, labels, "charge_v_bias")
    plot_overlay(series, scans, labels, "chargePre_v_bias")
    plot_overlay(series, scans, labels, "slewrate_v_bias")
    plot_overlay(series, scans, labels, "risetime_v_bias")
    plot_overlay(series, scans, labels, "noiseRMS_v_bias")
    plot_overlay(series, scans, labels, "snr_v_bias")
    plot_overlay(series, scans, labels, "tresCFD_v_bias")
    # v charge
    plot_overlay(series, scans, labels, "tresCFD_v_charge")
    plot_overlay(series, scans, labels, "slewrate_v_charge")
    plot_overlay(series, scans, labels, "risetime_v_charge")
    plot_overlay(series, scans, labels, "snr_v_charge")

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
