from array import array
from style import setStyle
import os, sys, re
import ROOT

colors = setStyle()

def int_conf(cfg):
    global_conf = int(cfg.split("_")[0])
    return global_conf

def get_amp_ch(ch=None,cfg=None):
    # returns amplifer corresponding to discriminator channel
    global_conf = int_conf(cfg) 
    if global_conf >= 180 : return 0
    if global_conf >= 151 : return 1
    else : return 0

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

def get_tres_TOT(f):
    fit = f.Get("f_timeTOT")
    res = 1e12*fit.GetParameter(2)
    err = 1e12*fit.GetParError(2)
    return res,err

def get_TOT(f): #return in ns
    hist = f.Get("h_tot")
    res = 1e9 * hist.GetMean()
    err = 1e9 * hist.GetMeanError()
    return res,err

def get_disc_eff(f):
    hist = f.Get("h_disc_eff")
    eff = 100*hist.GetBinContent(2)
    #err = 100*hist.GetBinError(2)
    err = 0.1 #tmp annoyingness
    return eff,err

def get_slew_rate(f):
    hist = f.Get("h_slewrate")
    rate = 1e-9 * hist.GetMean()
    err = 1e-9 * hist.GetMeanError()
    return rate,err
   
def axis(name):  
    if   "thJitter"  in name : return "expected jitter [ps]"
    elif "slewrate"  in name : return "mean slew rate [mV/ns]" 
    elif "risetime"  in name : return "mean risetime [ns]" 
    elif "noise"     in name : return "baseline RMS [mV]" 
    elif "snr"       in name : return "signal to noise ratio" 
    elif "tresCFD"   in name : return "time resolution (CFD) [ps]"
    elif "tresTOT"   in name : return "time resolution (TOT) [ps]"
    elif "meanTOT"   in name : return "mean discriminator TOT [ns]"
    elif "meanAmpTOT" in name : return "mean amplifier TOT [ns]"
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

    if "dac_v_meanTOT" in name: 
        g.GetXaxis().SetRangeUser(2.0,7.0)
        g.GetYaxis().SetRangeUser(210,340)
    
    outfile.cd()
    g.Write()

    return

def get_scan_results(scan): 
    
    
    # Open scan file, get configs 
    configs = []
    biases = []
    temps = []
    dacs = []
    scan_file = open("scans/{}.txt".format(scan),"r")
    for line in scan_file: 
        if "#" in line: continue

        config = line.split()[0]
        configs.append(config)
        biases .append(int(line.split()[1]))
        temps  .append(int(line.split()[2]))
        ch = line.split()[3]
        if "DAC" in config: 
            dacs.append(int(config.split("_")[6])) 

    scan_file.close()
    bias_errs = [0.1 for i in biases]
    dac_errs = [0.01 for i in dacs]

    if "cold" in scan : shift_biases = biases
    else : shift_biases = [i - 40 for i in biases]
 

    # Get measurements per config, save to array
    mean_amplitudes=[]
    err_amplitudes=[]

    mean_charges_pre=[]
    err_charges_pre=[]

    mean_charges=[]
    err_charges=[]

    mean_slews=[]
    err_slews=[]

    mean_rises=[]
    err_rises=[]

    mean_noises=[]
    err_noises=[]

    mean_disnoises=[]
    err_disnoises=[]

    mean_snrs=[]
    err_snrs=[]

    exp_jitters=[]
    err_jitters=[]

    tres_CFDs=[]
    err_tres_CFDs=[]

    tres_TOTs=[]
    err_tres_TOTs=[]
    
    eff_discs=[]
    err_effs_discs=[]

    mean_TOTs=[]
    err_TOTs=[]

    mean_ampTOTs=[]
    err_ampTOTs=[]

    for i,cfg in enumerate(configs):

        # Say where we are
        print(cfg)
        
        # open config root files
        rootfile = ROOT.TFile.Open("plots/configs/root/config_{}_ch{}.root".format(cfg,ch))
        if not rootfile : print("MISSING : config_{}_ch{}".format(cfg,ch))
        print(cfg)

        if "dis" in scan : 
            ch_amp = get_amp_ch(ch,cfg)
            rootfile = ROOT.TFile.Open("plots/configs/root/config_{}_ch{}.root".format(cfg,ch_amp))
            if not rootfile : print("MISSING : config_{}_ch{}".format(cfg,ch_amp))
            rootfile_dis = ROOT.TFile.Open("plots/configs/root/config_{}_ch{}.root".format(cfg,ch))
            if not rootfile_dis : print("MISSING : config_{}_ch{}".format(cfg,ch))
            print( cfg, ch, ch_amp ) 
        

        # Plots we want for everything
        mean_amplitude, err_amplitude  = get_amplitude(rootfile)
        mean_amplitudes.append(mean_amplitude) 
        err_amplitudes .append(err_amplitude)

        mean_charge_pre, err_charge_pre  = get_charge(rootfile)
        mean_charges_pre.append(mean_charge_pre)
        err_charges_pre .append(err_charge_pre)

        sf = 1.0 
        if "UCSC" in scan: sf = 6.0/9.0
        mean_charges.append(mean_charge_pre * sf)
        err_charges .append(err_charge_pre * sf)

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
    
        exp_jitter = mean_noise/mean_slew * 1000# noise in mV, slew in mV/ns, convert ns to ps 
        err_jitter = err_noise/mean_slew *1000 # bs
        exp_jitters.append(exp_jitter)
        err_jitters.append(err_jitter)

        if "dis" in scan:  

            mean_disnoise, err_disnoise  = get_baseline_RMS(rootfile_dis)
            mean_disnoises.append(mean_disnoise)
            err_disnoises .append(err_disnoise)

            tres_TOT, err_tres_TOT = get_tres_TOT(rootfile_dis)
            tres_TOTs.append(tres_TOT)
            err_tres_TOTs.append(err_tres_TOT)
            
            eff_disc, err_eff_disc = get_disc_eff(rootfile_dis) 
            eff_discs.append(eff_disc)
            err_effs_discs.append(err_eff_disc)

            mean_TOT, err_TOT = get_TOT(rootfile_dis)
            mean_TOTs.append(mean_TOT)
            err_TOTs.append(err_TOT)

            mean_ampTOT, err_ampTOT = get_TOT(rootfile)
            mean_ampTOTs.append(mean_ampTOT)
            err_ampTOTs.append(err_ampTOT)
            #print(tres_TOT, err_tres_TOT, eff_disc, err_eff_disc)

            

        rootfile.Close()
        if "dis" in scan: rootfile_dis.Close()

    # open rootfile for saving graphs
    outname = "plots/scans/root/{}.root".format(scan)
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    outfile.cd()
    print(outfile)
    
    # Make Graphs in functions, print and save in rootfiles
    # graph(outfile,x,xerr,y,yerr,name)
    pre="gr_{}_".format(scan)
    if "dac" in scan: 
        graph(outfile ,dacs ,dac_errs ,tres_TOTs    ,err_tres_TOTs  ,pre+"tresTOT_v_dac")
        graph(outfile ,dacs ,dac_errs ,eff_discs    ,err_effs_discs ,pre+"effDISC_v_dac")
        graph(outfile ,dacs ,dac_errs ,mean_TOTs    ,err_TOTs       ,pre+"meanTOT_v_dac")
        graph(outfile ,mean_TOTs    ,err_TOTs      ,dacs ,dac_errs  ,pre+"dac_v_meanTOT")
    elif "dis" in scan: 
        # plots versus bias
        graph(outfile,biases ,bias_errs ,mean_disnoises, err_disnoises ,pre+"noiseRMS_v_bias")
        graph(outfile,biases ,bias_errs ,tres_TOTs     ,err_tres_TOTs  ,pre+"tresTOT_v_bias")
        graph(outfile,biases ,bias_errs ,eff_discs     ,err_effs_discs ,pre+"effDISC_v_bias")
        graph(outfile,biases ,bias_errs ,mean_TOTs     ,err_TOTs       ,pre+"meanTOT_v_bias")
        graph(outfile,biases ,bias_errs ,mean_ampTOTs  ,err_ampTOTs    ,pre+"meanAmpTOT_v_bias")
        # plots versus charge
        graph(outfile,mean_charges,err_charges,tres_TOTs   ,err_tres_TOTs ,pre+"tresTOT_v_charge")
        graph(outfile,mean_charges,err_charges,eff_discs   ,err_effs_discs,pre+"effDISC_v_charge")
        graph(outfile,mean_charges,err_charges,mean_TOTs   ,err_TOTs      ,pre+"meanTOT_v_charge")
        graph(outfile,mean_charges,err_charges,mean_ampTOTs,err_ampTOTs   ,pre+"meanAmpTOT_v_charge")
        # plots versus amplifier
        graph(outfile,tres_CFDs   , err_tres_CFDs,tres_TOTs,err_tres_TOTs,pre+"tresTOT_v_tresCFD")
        graph(outfile,mean_ampTOTs, err_ampTOTs  ,mean_TOTs,err_TOTs     ,pre+"meanTOT_v_meanAmpTOT")
    else : 
        # versus bias
        graph(outfile,biases,bias_errs,mean_amplitudes ,err_amplitudes ,pre+"amp_v_bias")
        graph(outfile,biases,bias_errs,mean_noises     ,err_noises     ,pre+"noiseRMS_v_bias")
        graph(outfile,biases,bias_errs,mean_charges_pre,err_charges_pre,pre+"chargePre_v_bias")
        graph(outfile,biases,bias_errs,mean_charges    ,err_charges    ,pre+"charge_v_bias")
        graph(outfile,biases,bias_errs,mean_snrs       ,err_snrs       ,pre+"snr_v_bias")
        graph(outfile,biases,bias_errs,mean_slews      ,err_slews      ,pre+"slewrate_v_bias")
        graph(outfile,biases,bias_errs,mean_rises      ,err_rises      ,pre+"risetime_v_bias")
        graph(outfile,biases,bias_errs,tres_CFDs       ,err_tres_CFDs  ,pre+"tresCFD_v_bias")
        graph(outfile,biases,bias_errs,exp_jitters     ,err_jitters    ,pre+"thJitter_v_bias")
        # temp shift
        graph(outfile,shift_biases,bias_errs,mean_charges,err_charges,pre+"charge_v_biasShift")
        # versus amplitude/charge
        graph(outfile,mean_charges,err_charges,mean_snrs  ,err_snrs     ,pre+"snr_v_charge")
        graph(outfile,mean_charges,err_charges,mean_slews ,err_slews    ,pre+"slewrate_v_charge")
        graph(outfile,mean_charges,err_charges,mean_rises ,err_rises    ,pre+"risetime_v_charge")
        graph(outfile,mean_charges,err_charges,tres_CFDs  ,err_tres_CFDs,pre+"tresCFD_v_charge")
        graph(outfile,mean_charges,err_charges,exp_jitters,err_jitters  ,pre+"thJitter_v_charge")
        # cross check
        graph(outfile,exp_jitters,err_jitters,tres_CFDs ,err_tres_CFDs,pre+"tresCFD_v_thJitter")
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
