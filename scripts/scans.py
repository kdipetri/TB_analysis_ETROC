from array import array
from style import setStyle
import os, sys, re
import ROOT

colors = setStyle()

def get_amplitude(f):
    fit = f.Get("f_amplitude")
    amp = fit.GetParameter(1)
    err = fit.GetParError(1)
    return amp,err

def get_tres_CFD(f):
    fit = f.Get("f_timeCFD")
    res = 1e12*fit.GetParameter(2)
    err = 1e12*fit.GetParError(2)
    return res,err
    
def title(name):
    return ""
def xaxis(name):
    return ""
def yaxis(name):
    return ""

def cosmetics(graph,colorindex,tb=False):
    graph.SetLineColor(colors[colorindex])
    graph.SetMarkerColor(colors[colorindex])
    graph.SetMarkerSize(0.75)
    graph.SetMarkerStyle(20)
    if tb:
        graph.SetMarkerSize(2)
        #graph.SetMarkerStyle(29)
    return 

def graph(outfile,x,xerr,y,yerr,name):
    g = ROOT.TGraphErrors(len(x),array("d",x),array("d",y),array("d",xerr),array("d",yerr))
    cosmetics(g,0)
    g.SetName(name)
    g.SetTitle(title(name))
    g.GetXaxis().SetTitle(xaxis(name))
    g.GetYaxis().SetTitle(yaxis(name))

    c = ROOT.TCanvas()
    g.Draw()
    c.Print("plots/scans/{}.pdf".format(name))
    
    outfile.cd()
    g.Write()

    return

def get_scan_results(scan): 
    
    
    # Open scan file, get configs 
    configs = []
    biases = []
    temps = []

    scan_file = open("scans/{}.txt".format(scan),"r")
    for line in scan_file: 
        if "#" in line: continue

        configs.append(line.split()[0])
        biases .append(int(line.split()[1]))
        temps  .append(int(line.split()[2]))
        ch = line.split()[3]

    scan_file.close()
    bias_errs = [0.1 for i in biases]

    # Get measurements per config, save to array
    mean_amplitudes=[]
    err_amplitudes=[]

    tres_CFDs=[]
    err_tres_CFDs=[]

    for i,cfg in enumerate(configs):
        
        rootfile = ROOT.TFile.Open("plots/configs/root/config_{}_ch{}.root".format(cfg,ch))
        if not rootfile : print("MISSING : config_{}_ch{}".format(cfg,ch))

        mean_amplitude, err_amplitude  = get_amplitude(rootfile)
        mean_amplitudes.append(mean_amplitude)
        err_amplitudes .append(err_amplitude)

        tres_CFD, err_tres_CFD = get_tres_CFD(rootfile)
        tres_CFDs.append(tres_CFD)
        err_tres_CFDs.append(err_tres_CFD)

        #print(biases[i],mean_amplitude,tres_CFD)

        rootfile.Close()

    # open rootfile for saving graphs
    outname = "plots/scans/root/{}_ch{}.root".format(cfg,ch)
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    outfile.cd()
    print(outfile)
    
    # Make Graphs in functions, print and save in rootfiles
    # graph(outfile,x,xerr,y,yerr,name)
    pre="gr_{}_".format(scan)
    graph(outfile,biases,bias_errs,mean_amplitudes,err_amplitudes,pre+"amp_v_bias")
    graph(outfile,biases,bias_errs,tres_CFDs      ,err_tres_CFDs ,pre+"tresCFD_v_bias")
    outfile.Close()

def get_scans():
    # Loop through configurations 
    scan_list = open("scans/scans.txt","r")
    for i,line in enumerate(scan_list): 
     
        # for tmp debugging
        #if i > 0: break 
        #if "156" not in line: continue

        if "#" in line: continue
        scan = line.strip()
        get_scan_results(scan)

# Main
get_scans()
