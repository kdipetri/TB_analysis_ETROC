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

def get_charge(f):
    fit = f.Get("f_charge")
    amp = fit.GetParameter(1)
    err = fit.GetParError(1)
    return amp,err

def get_slew_rate(f):
    hist = f.Get("h_slewrate")
    rate = 1e-9 * hist.GetMean()
    err = 1e-9* hist.GetMeanError()
    return rate,err

def get_risetime(f):
    hist = f.Get("h_risetime")
    rise = hist.GetMean()
    err = hist.GetMeanError()
    return rise,err

def get_baseline_RMS(f):
    hist = f.Get("h_baselineRMS")
    rms = hist.GetMean()
    err = hist.GetMeanError()
    return rms,err

def get_tres_CFD(f):
    fit = f.Get("f_timeCFD")
    res = 1e12*fit.GetParameter(2)
    err = 1e12*fit.GetParError(2)
    return res,err
   
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

    mean_charges=[]
    err_charges=[]

    mean_slews=[]
    err_slews=[]

    mean_rises=[]
    err_rises=[]

    mean_noises=[]
    err_noises=[]

    mean_snrs=[]
    err_snrs=[]

    mean_snrs=[]
    err_snrs=[]

    tres_CFDs=[]
    err_tres_CFDs=[]

    for i,cfg in enumerate(configs):
        
        rootfile = ROOT.TFile.Open("plots/configs/root/config_{}_ch{}.root".format(cfg,ch))
        if not rootfile : print("MISSING : config_{}_ch{}".format(cfg,ch))
        print(cfg)

        mean_amplitude, err_amplitude  = get_amplitude(rootfile)
        mean_amplitudes.append(mean_amplitude) 
        err_amplitudes .append(err_amplitude)

        mean_charge, err_charge  = get_charge(rootfile)
        mean_charges.append(mean_charge)
        err_charges .append(err_charge)

        mean_rise, err_rise  = get_risetime(rootfile)
        mean_rises.append(mean_rise)
        err_rises .append(err_rise)

        mean_slew, err_slew  = get_slew_rate(rootfile)
        mean_slews.append(mean_slew)
        err_slews .append(err_slew)

        mean_noise, err_noise  = get_baseline_RMS(rootfile)
        mean_noises.append(mean_noise)
        err_noises .append(err_noise)
   
        mean_snrs.append(mean_amplitude/mean_noise)
        err_snrs.append(err_amplitude/mean_noise)

        tres_CFD, err_tres_CFD = get_tres_CFD(rootfile)
        tres_CFDs.append(tres_CFD)
        err_tres_CFDs.append(err_tres_CFD)

        #print(biases[i],mean_amplitude,tres_CFD)

        rootfile.Close()

    # open rootfile for saving graphs
    outname = "plots/scans/root/{}.root".format(scan)
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    outfile.cd()
    print(outfile)
    
    # Make Graphs in functions, print and save in rootfiles
    # graph(outfile,x,xerr,y,yerr,name)
    pre="gr_{}_".format(scan)
    graph(outfile ,biases ,bias_errs ,mean_amplitudes,err_amplitudes ,pre+"amp_v_bias")
    graph(outfile ,biases ,bias_errs ,mean_charges   ,err_charges    ,pre+"charge_v_bias")
    graph(outfile ,biases ,bias_errs ,mean_slews     ,err_slews      ,pre+"slewrate_v_bias")
    graph(outfile ,biases ,bias_errs ,mean_rises     ,err_rises      ,pre+"risetime_v_bias")
    graph(outfile ,biases ,bias_errs ,mean_noises    ,err_noises     ,pre+"noiseRMS_v_bias")
    graph(outfile ,biases ,bias_errs ,mean_snrs      ,err_snrs       ,pre+"snr_v_bias")
    graph(outfile ,biases ,bias_errs ,tres_CFDs      ,err_tres_CFDs  ,pre+"tresCFD_v_bias")
    # versus amplitude/charge
    graph(outfile ,mean_amplitudes ,err_amplitudes ,tres_CFDs ,err_tres_CFDs ,pre+"tresCFD_v_amp")
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
