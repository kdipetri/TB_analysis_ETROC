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
    photek_min = 50 # mV
    return photek_min

def photek_max(cfg=None):
    photek_max = 100 # mV
    return photek_max

def get_min_amp(ch=None,cfg=None):
    global_conf = int(cfg.split("_")[1])
    if ch == 3: return photek_min(cfg)
    elif ch == 0 : 
        if global_conf <= 146 : # UCSD 
            if global_conf ==  130 : return 50
            elif global_conf == 131 : return 70
            elif global_conf == 132 : return 50
            elif global_conf == 133 : return 50
            elif global_conf == 135 : return 40
            elif global_conf == 136 : return 30
            elif global_conf == 137 : return 30
            elif global_conf == 144 : return 50
            elif global_conf == 145 : return 70
            else : return 20    
        else : # ETROC 11   
            if global_conf == 150 : return 50 
            elif global_conf == 151 : return 50 
            elif global_conf == 153 : return 150 
            elif global_conf == 154 : return 100 
            elif global_conf == 155 : return 50 
            elif global_conf == 156 : 
                if   "IBSel_0b000_RFSel_0" in cfg : return 100 
                elif "IBSel_0b000_RFSel_3" in cfg : return 50
                elif "IBSel_0b111_RFSel_0" in cfg : return 70
                elif "IBSel_0b111_RFSel_3" in cfg : return 50
                else : return 50
            else : return 70
    elif ch == 1 : 
            if global_conf == 130 : return 130
            elif global_conf == 131 : return 150
            elif global_conf == 132 : return 200
            elif global_conf == 133 : return 200
            elif global_conf == 134 : return 70
            elif global_conf == 142 : return 70
            elif global_conf == 143 : return 130
            elif global_conf == 144 : return 150
            elif global_conf == 145 : return 200
            elif global_conf == 146 : return 250
            elif global_conf == 148 : return 70
            elif global_conf == 153 : 
                if   "IBSel_0b000" in cfg : return 200 
                else : return 150
            elif global_conf == 154 : return 80 
            elif global_conf == 156 : 
                if   "IBSel_0b000_RFSel_0" in cfg : return 100 
                elif "IBSel_0b000_RFSel_3" in cfg : return 50
                elif "IBSel_0b111_RFSel_0" in cfg : return 70
                elif "IBSel_0b111_RFSel_3" in cfg : return 50
                else : return 20
            elif global_conf == 158 : return 125
            elif global_conf == 159 : return 70
            else : return 50
    elif ch == 2 :# not done here 
        if is_discrim(ch,cfg) : return 400
        else : return 20
    else : return 20

def get_max_amp(ch=None,cfg=None):
    if ch == 3: return photek_max(cfg)
    elif is_etroc_amp(ch,cfg) : return 720 # may need to set this by config
    elif is_discrim(ch,cfg) : return 1000 # may need to adjust
    else : return 340 # is UCSD may need to adjust
    
def get_min_time(ch=None,cfg=None):
    global_conf = int(cfg.split("_")[1])
    if ch == 0 : 
        if global_conf <= 146: return 6.7e-9
        else : return 4.0e-9
    elif ch == 1 : 
        if   global_conf <= 139: return 3.7e-9
        elif global_conf <= 146: return 3.8e-9
        else : return 3.7e-9
    elif ch == 2 :      
        # will need to adjust for DAC threshold scans
        # 148 and 153
        if global_conf <= 146 : return 6.7e-9
        else : return 4.2e-9
    else : return -5e-9 

def get_max_time(ch=None,cfg=None):
    global_conf = int(cfg.split("_")[1])
    if ch == 0 : 
        if global_conf <= 146: return 7.1e-9
        else : return 4.6e-9
    elif ch == 1 : 
        if   global_conf <= 139: return 4.2e-9
        elif global_conf <= 146: return 4.1e-9
        else : return 4.3e-9
    elif ch == 2 :      
        # will need to adjust for DAC threshold scans
        # 148 and 153
        if global_conf <= 146 : return 7.3e-9
        else : return 5.4e-9
    else : return 5e-9 

def is_discrim(ch=None,cfg=None):
    global_conf = int(cfg.split("_")[1])
    if ch == 2 and global_conf > 146: return True 

def is_etroc_amp(ch=None,cfg=None):
    global_conf = int(cfg.split("_")[1])
    if global_conf < 146 : 
        if ch == 1 : return True
    else : 
        if ch == 0 : return True 
        if ch == 1 : return True 
    return False

def version(run):
    run = int(run)
    if   run > 29072 and run < 29201: return "v6" 
    elif run > 28233 and run < 28271: return "v3"
    elif run > 27821: return "v5" 
    elif run > 27424 and run < 27690: return "v2"
    else            : return "v1"

def get_mean_amplitude_channel(tree,cfg,ch,outfile):
   
    minAmp = 30 # for this plot only
    if cfg == "config_133" : minAmp = 50
    minPh = photek_min(cfg)
    maxPh = photek_max(cfg)
    histMax = 500
    if is_discrim(ch,cfg): histMax = 1000
    elif is_etroc_amp(ch,cfg) : histMax = 700
    
    #landau hist
    hist = ROOT.TH1D("h_amplitude","",50,0,histMax)
    tree.Project("h_amplitude","amp[%i]"%ch,"amp[%i]>%f&&amp[%i]>%f"%(ch,minAmp,ch_photek,minPh))

    f1 = ROOT.TF1("f_amplitude","landau",0,histMax)
    hist.Fit(f1)

    c = ROOT.TCanvas()
    hist.SetTitle(";Amplitude [mV];Events")
    hist.Draw()
    f1.Draw("same")

    c.Print("plots/configs/{}_ch{}_amp.pdf".format(cfg,ch))

    outfile.cd()
    hist.Write()
    f1.Write()

    return f1.GetParameter(1),f1.GetParError(1)

def get_time_CFD(tree,cfg,ch,outfile):

    minAmp = get_min_amp(ch,cfg)
    maxAmp = get_max_amp(ch,cfg)
    minPh = photek_min(cfg)
    maxPh = photek_max(cfg)
    minT = get_min_time(ch,cfg)
    maxT = get_max_time(ch,cfg)
    
    print("minAmp = {}".format(minAmp))
    print("maxAmp = {}".format(maxAmp))
    print("minPh  = {}".format(minPh ))
    print("maxPh  = {}".format(maxPh ))
    print("minT   = {}".format(minT  ))
    print("maxT   = {}".format(maxT  ))

    #landau hist
    hist = ROOT.TH1D("h_timeCFD","",100,minT,maxT)
    tree.Project("h_timeCFD","LP2_15[%i]-LP2_20[%i]"%(ch,ch_photek),"amp[%i]>%f && amp[%i]<%f && amp[%i]>%f && amp[%i]<%f && LP2_15[%i]!=0 && LP2_20[%i]!=0"%(ch,minAmp,ch,maxAmp,ch_photek,minPh,ch_photek,maxPh,ch,ch_photek))

    
    f1 = ROOT.TF1("f_timeCFD","gaus",minT,maxT)
    hist.Fit(f1)

    c = ROOT.TCanvas()
    hist.SetTitle(";t-t_{ref}(CFD) [s];Events")
    hist.Draw()
    f1.Draw("same")

    c.Print("plots/configs/{}_ch{}_timeCFD.pdf".format(cfg,ch))

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
    for ch in range(0,3): # skip photek

        outname = "plots/configs/root/{}_ch{}.root".format(cfg,ch)
        outfile = ROOT.TFile.Open(outname,"RECREATE")
        print(outfile)
    
        # Landau
        get_mean_amplitude_channel(tree,cfg,ch,outfile)
        # Time CFD
        get_time_CFD(tree,cfg,ch,outfile)
    
        
def get_configurations():
    # Loop through configurations 
    cfg_list = open("configs/configurations.txt","r")
    for i,line in enumerate(cfg_list): 
     
        # for tmp debugging
        #if i > 0: break 
        #if "156" not in line: continue
        if "133" not in line: continue

        if "#" in line: continue
        cfg = line.strip()
        get_config_results(cfg)

# Main
get_configurations()
