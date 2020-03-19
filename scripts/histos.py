from array import array
from style import setStyle
import os, sys, re
import ROOT

colors = setStyle()

# default parameters
ch_photek=3 # photek channel

def charge_threshold(ch=None,cfg=None):
    charge_thresh = 20 # fC
    return charge_thresh

def photek_min(cfg=None):
    photek_min = 15 # mV
    return photek_min

def photek_max(cfg=None):
    photek_max = 200 # mV
    return photek_max

def get_min_amp(ch=None,cfg=None):
    if ch == 3: return photek_min(cfg)
    else : return 20

def get_max_amp(ch=None,cfg=None):
    if ch == 3: return photek_max(cfg)
    else : return 1000

def version(run):
    #global_cfg = cfg.split("_")[1]
    #print(global_cfg)
    run = int(run)
    if   run > 29072 and run < 29201: return "v6" 
    elif run > 28233 and run < 28271: return "v3"
    elif run > 27821: return "v5" 
    elif run > 27424 and run < 27690: return "v2"
    else            : return "v1"

def get_mean_response_channel(tree,cfg,ch,outfile):
   
    minAmp = get_min_amp(ch,cfg)
    maxAmp = get_max_amp(ch,cfg)
    minPh = photek_min(cfg)
    maxPh = photek_max(cfg)
    histMax = 500
    
    #landau hist
    hist = ROOT.TH1D("h_amplitude","",50,0,histMax)
    tree.Project("h_amplitude","amp[%i]"%ch,"amp[%i]>%f&&amp[%i]>%f"%(ch,minAmp,ch_photek,minPh))

    f1 = ROOT.TF1("f_amplitude","landau",0,histMax)
    hist.Fit(f1)

    c = ROOT.TCanvas()
    hist.SetTitle(";Amplitude [mV];Events")
    hist.Draw()
    f1.Draw("same")

    c.Print("histos/plots/{}_ch{}_amp.pdf".format(cfg,ch))

    outfile.cd()
    hist.Write()
    f1.Write()

    return f1.GetParameter(1),f1.GetParError(1)

def get_config_results(cfg):
    
    # Open config file, get runs
    runs = []
    cfg_file = open("configs/{}.txt".format(cfg),"r")
    for line in cfg_file: 
        if "#" in line: continue
        run = line.strip()
        #print(run)
        runs.append(run)
    cfg_file.close()
    
    # Fill TChain
    print(cfg)
    tree = ROOT.TChain("pulse")
    for i,run in enumerate(runs):

        rootfile = "root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/{}/run_scope{}_converted.root".format(version(run),run)
        tree.Add(rootfile)

        testfile = ROOT.TFile.Open(rootfile)
        if not testfile : print("MISSING : {}".format(run))
    #tree.SetDirectory(0)

    # Generic plots per channel for now
    # May get more specific later (by ch and cfg)
    for ch in range(0,4):

        outname = "histos/root/{}_ch{}.root".format(cfg,ch)
        outfile = ROOT.TFile.Open(outname,"RECREATE")
        print(outfile)
    
        # Landau
        get_mean_response_channel(tree,cfg,ch,outfile)
    
        
def get_configurations():
    # Loop through configurations 
    cfg_list = open("configs/configurations.txt","r")
    for i,line in enumerate(cfg_list): 
     
        # for tmp debugging
        #if i > 0: break 

        if "#" in line: continue
        cfg = line.strip()
        get_config_results(cfg)

# Main
get_configurations()
