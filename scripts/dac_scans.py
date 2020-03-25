from array import array
from style import setStyle
import os, sys, re
import ROOT

colors = setStyle()
   
def axis(name):  
    if "dac" in name: return "DAC threshold"
    elif "tres" in name : return "time resolution (TOT) [ps]"
    elif "eff" in name : return "efficiency"
    else : return ""

def xaxis(name):
    xstring = name.split("_v_")[1]
    return axis(xstring) 

def yaxis(name):
    ystring = name.split("_v_")[0]
    return axis(ystring) 

def cosmetics(graph,colorindex,tb=False):
    graph.SetLineColor(colors[colorindex])
    graph.SetMarkerColor(colors[colorindex])
    graph.SetMarkerSize(1.0)
    graph.SetMarkerStyle(20)
    return 


def plot_overlay( scan ):

    outfile = ROOT.TFile.Open("plots/scans/root/{}.root".format(scan))
    gr_tres  = outfile.Get("gr_{}_tresTOT_v_dac".format(scan))
    gr_eff   = outfile.Get("gr_{}_effDISC_v_dac".format(scan))

    gr_tres.SetLineColor(ROOT.kRed+1)
    gr_tres.SetMarkerColor(ROOT.kRed+1)
    gr_tres.SetMarkerSize(1.0)
    gr_tres.SetMarkerStyle(20)

    gr_eff.SetLineColor(ROOT.kOrange+1)
    gr_eff.SetMarkerColor(ROOT.kOrange+1)
    gr_eff.SetMarkerSize(1.0)
    gr_eff.SetMarkerStyle(20)
    
    #cosmetics(gr_tres,1)
    #cosmetics(gr_eff,2)
    board = "9" 
    if "11" in scan : board = "11"

    c = ROOT.TCanvas()
    c.SetGridy()
    c.SetGridx()

    mgraph = ROOT.TMultiGraph()
    mgraph.Add(gr_tres)
    mgraph.Add(gr_eff)
    mgraph.SetTitle(";DAC threshold;")
    mgraph.Draw("AELP")
    mgraph.GetHistogram().GetYaxis().SetRangeUser(0.,200);

    leg = ROOT.TLegend(0.2,0.75,0.85,0.89)
    leg.SetMargin(0.15)
    leg.AddEntry(gr_tres, "ETROC{} time resolution (TOT) [ps]".format(board) ,"EP")
    leg.AddEntry(gr_eff , "ETROC{} discriminator eff [%]".format(board) ,"EP")
    
    leg.Draw() 
    c.Print("plots/dac_scans/ETROC{}.pdf".format(board))
    
    return


def get_scans():
    # Loop through configurations 
    scan_list = []
    scan_list.append("scan_ETROC11disLP_dac")
    scan_list.append("scan_ETROC9disLP_dac")
    for scan in scan_list: 
     
        plot_overlay(scan)

# Main
get_scans()
