from array import array
from style import setStyle
from tot_cleaning import tot_cleaning
import os, sys, re
import ROOT

colors = setStyle()

# default parameters
ch_photek=3 # photek channel
minPh = 50 #mV 
maxPh = 100 #mV

def int_conf(cfg):
    global_conf = int(cfg.split("_")[1])
    return global_conf

def get_min_amp(ch=None,cfg=None):
    global_conf = int_conf(cfg) 
    if ch == 3: return photek_min(cfg)
    elif is_discrim(ch,cfg) : return 400
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
        elif global_conf < 180: # ETROC 11   
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
        else : #ETROC 9 amp - cold!
            if global_conf ==184 : return 110
            elif global_conf ==185 : return 170    
            elif global_conf == 186 : return 250
            elif global_conf == 187 : return 60
            elif global_conf == 190 : return 100     
            elif global_conf == 191 : return 170 
            elif global_conf == 192 : return 200 
            elif global_conf == 193 : return 320 
            else : return 50
    elif ch == 1 : 
            if global_conf == 130 : return 130
            elif global_conf == 131 : return 150
            elif global_conf == 132 : return 180
            elif global_conf == 133 : return 100
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
        if global_conf < 180 : # is UCSC warm 
            if   global_conf == 130 : return 70
            elif global_conf == 131 : return 80
            elif global_conf == 132 : return 110
            elif global_conf == 133 : return 125
            elif global_conf == 134 : return 40
            elif global_conf == 145 : return 70
            elif global_conf == 146 : return 100
            else : return 25
        else : # is UCSC cold
            if global_conf == 184 : return 50
            elif global_conf == 185 : return 70
            elif global_conf == 186 : return 100
            elif global_conf == 188 : return 40
            elif global_conf == 191 : return 20
            elif global_conf == 192 : return 15 
            elif global_conf == 193 : return 70
            else : return 25
    else : return 20

def get_max_amp(ch=None,cfg=None):
    if ch == 3: return photek_max(cfg)
    elif is_etroc_amp(ch,cfg) : return 710 # may need to set this by config
    elif is_discrim(ch,cfg) : return 1000 # may need to adjust
    else : return 340 # is UCSD may need to adjust
    
def get_min_time(ch=None,cfg=None):
    global_conf = int_conf(cfg) 
    if ch == 0 : 
        if global_conf <= 146: return 6.7e-9
        elif global_conf > 180 : return 3.6e-9
        else : return 4.0e-9
    elif ch == 1 : 
        if   global_conf <= 139: return 3.7e-9
        elif global_conf <= 146: return 3.8e-9
        elif global_conf > 180 : return 4.0e-9
        else : return 3.7e-9
    elif ch == 2 :      
        # will need to adjust for DAC threshold scans
        # 148 and 153
        if global_conf <= 146 : return 6.7e-9
        elif global_conf > 180 : return 3.4e-9
        else : return 4.2e-9
    else : return -5e-9 

def get_max_time(ch=None,cfg=None):
    global_conf = int_conf(cfg) 
    if ch == 0 : 
        if global_conf <= 146: return 7.1e-9
        elif global_conf > 180 : return 4.3e-9
        else : return 4.6e-9
    elif ch == 1 : 
        if   global_conf <= 139: return 4.2e-9
        elif global_conf <= 146: return 4.1e-9
        elif global_conf > 180 : return 5.5e-9
        else : return 4.3e-9
    elif ch == 2 :      
        # will need to adjust for DAC threshold scans
        # 148 and 153
        if global_conf <= 146 : return 7.3e-9
        elif global_conf > 180 : return 4.4e-9
        else : return 5.4e-9
    else : return 5e-9 

def is_discrim(ch=None,cfg=None):
    global_conf = int_conf(cfg) 
    if global_conf > 180 : 
        if ch == 1 : return True
    elif global_conf > 146:  
        if ch == 2 : return True
    return False

def is_etroc_amp(ch=None,cfg=None):
    global_conf = int_conf(cfg) 
    if global_conf > 180 : 
        if ch == 0 : return True
    elif global_conf > 146: 
        if ch <= 1 : return True 
    else : 
        if ch == 1 : return True
    return False

def get_amp_ch(ch=None,cfg=None):
    # returns amplifer corresponding to discriminator channel
    if is_discrim(ch,cfg): 
        global_conf = int_conf(cfg) 
        if global_conf >= 190 : return 0
        if global_conf >= 151 : return 1
        else : return 0
    else : return -1 

def version(run):
    run = int(run)
    if run == 28252 : return "v1"
    elif run == 28253 : return "v1"
    elif run == 28256 : return "v1"
    elif run > 29072 and run < 29201: return "v6" 
    elif run > 28232 and run <= 28271: return "v3"
    elif run > 27821: return "v5" 
    elif run > 27424 and run < 27690: return "v2"
    else : return "v1"

def get_mean_amplitude_channel(tree,cfg,ch,outfile):
   
    minAmp = 30 # for this plot only
    if cfg == "config_133" : minAmp = 50
    histMax = 500
    if is_discrim(ch,cfg): histMax = 1000
    elif is_etroc_amp(ch,cfg) : histMax = 700
    
    #landau hist
    hist = ROOT.TH1D("h_amplitude","",50,0,histMax)
    tree.Project("h_amplitude","amp[%i]"%ch,"amp[%i]>%f&&amp[%i]>%f"%(ch,minAmp,ch_photek,minPh))

    f1 = ROOT.TF1("f_amplitude","landau",0,histMax)
    hist.Fit(f1,"Q")

    c = ROOT.TCanvas()
    hist.SetTitle(";Amplitude [mV];Events")
    hist.Draw()
    f1.Draw("same")

    c.Print("plots/configs/{}_ch{}_amp.pdf".format(cfg,ch))

    outfile.cd()
    hist.Write()
    f1.Write()

    return 

def get_charge_channel(tree,cfg,ch,outfile):
       
    # ignore if discriminator
    if is_discrim(ch,cfg): return 

    minAmp = get_min_amp(ch,cfg)
    transimpedance = 4700
    if is_etroc_amp(ch,cfg): transimpedance = 33000 # SF to make charge match UCSC 
    #if is_etroc_amp(ch,cfg): transimpedance = 33000 * 6.0/9.0 #SF to make charge match UCSC 

    hist = ROOT.TH1D("h_charge","",50,0,100)
    # Qin = Qout / transimpedance 
    # Q_out is the pulse area with units of volts * times 50 ohms, 
    # because it is terminated at 50 ohms
    # transimpedance UCSC = 470 * 10 (second stage)
    # transimpedance ETROC = 4400 (default gain)  * 0.8 (buffer) * 12 (second stage) * SF

    tree.Project("h_charge","-1000*integral[%i]*1e9*50/%f"%(ch,transimpedance),"amp[%i]>%f&&amp[3]>%i"%(ch,minAmp,minPh))
    
    f1 = ROOT.TF1("f_charge","landau",0,100)
    hist.Fit(f1,"Q")

    c = ROOT.TCanvas()
    hist.SetTitle(";Integrated charge [fC];Events")
    hist.Draw()
    f1.Draw("same")

    outfile.cd()
    hist.Write()
    f1.Write()

    c.Print("plots/configs/{}_ch{}_charge.pdf".format(cfg,ch))

    return 

def get_slew_rate_channel(tree,cfg,ch,outfile):
    if is_discrim(ch,cfg): return 

    minAmp = get_min_amp(ch,cfg)

    hist = ROOT.TH1D("h_slewrate","",60,0,600e9)
    tree.Project("h_slewrate","abs(risetime[%i])"%ch,"amp[%i]>%f"%(ch,minAmp))  ### mV/ s

    c = ROOT.TCanvas()
    hist.Draw()
    outfile.cd()
    hist.Write()

    c.Print("plots/configs/{}_ch{}_slewrate.pdf".format(cfg,ch))

    return 

def get_risetime_channel(tree,cfg,ch,outfile):
    if is_discrim(ch,cfg): return 

    minAmp = get_min_amp(ch,cfg)

    hist = ROOT.TH1D("h_risetime","",150,0,3)
    tree.Project("h_risetime","1e9*abs(amp[%i]/risetime[%i])"%(ch,ch),"amp[%i]>%i"%(ch,minAmp))  ### mV/ s

    c = ROOT.TCanvas()
    hist.Draw()
    outfile.cd()
    hist.Write()
    c.Print("plots/configs/{}_ch{}_risetime.pdf".format(cfg,ch))

    return 

def get_baseline_RMS_channel(tree,cfg,ch,outfile):
    hist = ROOT.TH1F("h_baselineRMS","",20,-1000,1000)
    tree.Project("h_baselineRMS","baseline_RMS[%i]"%ch,"")
    outfile.cd()
    hist.Write()
    return 

def get_time_CFD(tree,cfg,ch,outfile):

    minAmp = get_min_amp(ch,cfg)
    maxAmp = get_max_amp(ch,cfg)
    minT = get_min_time(ch,cfg)
    maxT = get_max_time(ch,cfg)
    

    #landau hist
    hist = ROOT.TH1D("h_timeCFD","",100,minT,maxT)
    tree.Project("h_timeCFD","LP2_15[%i]-LP2_20[%i]"%(ch,ch_photek),"amp[%i]>%f && amp[%i]<%f && amp[%i]>%f && amp[%i]<%f && LP2_15[%i]!=0 && LP2_20[%i]!=0"%(ch,minAmp,ch,maxAmp,ch_photek,minPh,ch_photek,maxPh,ch,ch_photek))

    
    f1 = ROOT.TF1("f_timeCFD","gaus",minT,maxT)
    hist.Fit(f1,"Q")

    c = ROOT.TCanvas()
    hist.SetTitle(";t-t_{ref}(CFD) [s];Events")
    hist.Draw()
    f1.Draw("same")

    c.Print("plots/configs/{}_ch{}_timeCFD.pdf".format(cfg,ch))

    outfile.cd()
    hist.Write()
    f1.Write()

    return f1.GetParameter(1),f1.GetParError(1)


def get_time_walk(tree,cfg,ch,outfile):
    #(70,-3.3e-9,-1.6e-9)
    
    minAmp = get_min_amp(ch,cfg)
    maxAmp = get_max_amp(ch,cfg)
    minT = get_min_time(ch,cfg)-1e-9
    maxT = get_max_time(ch,cfg)+1e-9
    mintot,maxtot = tot_cleaning(cfg)
    #mint0 = 
    histmax = 10e-9
    if "RFSel_0" in cfg: histmax = 15e-9
    if "190_IBSel_0b000_RFSel_3_DAC_424" in cfg and ch==0: 
        histmax = 6e-9
        minT = 3.5e-9
        maxT = 4.5e-9
    
    #print("minAmp = {}".format(minAmp))
    #print("maxAmp = {}".format(maxAmp))
    #print("minPh  = {}".format(minPh ))
    #print("maxPh  = {}".format(maxPh ))
    #print("minT   = {}".format(minT  ))
    #print("maxT   = {}".format(maxT  ))

    hist = ROOT.TH2D("h_timewalk","",100,0,histmax,100,minT,maxT)
    

    tree.Project("h_timewalk","t0_30[%i]-LP2_20[%i]:tot_30[%i]"%(ch,ch_photek,ch),"amp[%i]>%i && amp[%i]>%i && amp[%i]<%i && LP2_20[%i]!=0 && t0_30[%i]!=0 && tot_30[%i]>%f *1e-9 && tot_30[%i]<%f * 1e-9"%(ch,minAmp,ch_photek,minPh,ch_photek,maxPh,ch_photek,ch, ch,mintot, ch,maxtot),"COLZ")

    c = ROOT.TCanvas()
    hist.Draw("COLZ")
    
    profile = hist.ProfileX("h_timewalkprof")
    spread  = hist.ProfileX("h_timewalkspread",1,-1,"s")
    
    profile.Draw("same")
    profile.SetMarkerStyle(20);
    profile.SetMarkerSize(0.8);
    profile.SetMarkerColor(ROOT.kBlack);
    profile.SetLineColor(ROOT.kBlack);
    profile.SetLineWidth(1);
    spread.SetFillColorAlpha(ROOT.kBlack,0.2);
    spread.Draw("e2sames");
    
    profile.GetXaxis().SetRangeUser(0,maxtot) 
    spread .GetXaxis().SetRangeUser(0,maxtot)
    profile.GetYaxis().SetRangeUser(minT,maxT) 
    spread .GetYaxis().SetRangeUser(minT,maxT)
    profile.GetYaxis().SetTitle("t_{0}-t_{ref} [s]") 
    
    c.Print("plots/configs/{}_ch{}_t0_v_tot.pdf".format(cfg,ch))
    
    #fitmintot = mintot#1e-9
    #fitmaxtot = maxtot#10e-9
    # 3rd order
    f1 = ROOT.TF1("f_timewalk","pol3",0,histmax)
    hist.Fit(f1,"Q")

    profile.Draw("")
    spread.Draw("e2sames");
    f1.Draw("same")
    
    c.Print("plots/configs/{}_ch{}_t0_v_tot_fit.pdf".format(cfg,ch))
    
    outfile.cd()
    hist.Write()
    profile.Write()
    spread.Write()
    f1.Write()

    # fit should have four parameters
    #print('Run Number {}, channel {}'.format(run,ch))
    #print('p0 : {} , {} '.format(f1.GetParameter(0),f1.GetParError(0)))
    #print('p1 : {} , {} '.format(f1.GetParameter(1),f1.GetParError(1)))
    #print('p2 : {} , {} '.format(f1.GetParameter(2),f1.GetParError(2)))
    #print('p3 : {} , {} '.format(f1.GetParameter(3),f1.GetParError(3)))
    
    params = (f1.GetParameter(0), f1.GetParameter(1), f1.GetParameter(2), f1.GetParameter(3))
    return params 

def get_time_TOT(tree,cfg,ch,fit_params,outfile):

    minAmp = get_min_amp(ch,cfg)
    maxAmp = get_max_amp(ch,cfg)
    mint = -1e-9
    maxt =  1e-9
    mintot,maxtot = tot_cleaning(cfg)
    histmax = 10e-9
    if "RFSel_0" in cfg: histmax = 15e-9
    if "190_IBSel_0b000_RFSel_3_DAC_424" in cfg and ch==0: 
        histmax = 6e-9
        minT = 3.5e-9
        maxT = 4.5e-9
    
    (x0,x1,x2,x3) = fit_params
    f_TOT = "{:e} + {:e}*tot_30[{}] + {:e}*tot_30[{}]**2 + {:e}*tot_30[{}]**3 - t0_30[{}] + LP2_20[3]".format(x0,x1,ch,x2,ch,x3,ch,ch) 
    
    # 2D hist to validate time walk correction
    hist2D = ROOT.TH2D("h_timewalkcorr",";TOT [s];t-t_{ref} (TOT,corr) [s]",100,0,histmax,100,mint,maxt)
    
    tree.Project("h_timewalkcorr","%s:tot_30[%i]"%(f_TOT,ch),"amp[%i]>%i && amp[%i]>%i && amp[%i]<%i && LP2_20[%i]!=0 && t0_30[%i]!=0 && tot_30[%i]>%f*1e-9 &&tot_30[%i]<%f*1e-9"%(ch,minAmp,ch_photek,minPh,ch_photek,maxPh,ch_photek,ch, ch,mintot, ch,maxtot),"COLZ")

    c = ROOT.TCanvas()
    hist2D.Draw("COLZ")
    c.Print("plots/configs/{}_ch{}_t0_v_tot_corr.pdf".format(cfg,ch))

    # 1D hist for final corrected time resolution
    hist = ROOT.TH1D("h_timeTOT",";t-t_{ref} (TOT) [s]",100,mint,maxt)
    
    tree.Project("h_timeTOT","%s"%(f_TOT),"amp[%i]>%i && amp[%i]>%i && amp[%i]<%i && LP2_20[%i]!=0 && t0_30[%i]!=0 && tot_30[%i]>%f*1e-9 && tot_30[%i]<%f*1e-9"%(ch,minAmp,ch_photek,minPh,ch_photek,maxPh,ch_photek,ch, ch,mintot, ch,maxtot))
    
    f1 = ROOT.TF1("f_timeTOT","gaus",mint,maxt)
    
    hist.Fit(f1,"Q")
    
    hist.Draw()
    f1.Draw("same")
    c.Print("plots/configs/{}_ch{}_timeTOT.pdf".format(cfg,ch))

    outfile.cd()
    hist2D.Write()
    hist.Write()
    f1.Write()

    return  

def get_tot_channel(tree,cfg,ch,outfile):

    minAmp = get_min_amp(ch,cfg)

    hist = ROOT.TH1D("h_tot","TOT [s]",150,0,10e-9)
    tree.Project("h_tot","tot_30[%i]"%(ch),"amp[%i]>%i"%(ch,minAmp))  

    c = ROOT.TCanvas()
    hist.Draw()
    outfile.cd()
    hist.Write()
    c.Print("plots/configs/{}_ch{}_risetime.pdf".format(cfg,ch))

    return 

def get_disc_eff(tree,cfg,ch,ch_amp,outfile):
    minAmp = get_min_amp(ch_amp,cfg)

    hist_den = ROOT.TH1D("h1","",2,-0.5,1.5)
    hist_num = ROOT.TH1D("h2","",2,-0.5,1.5)
    hist_den.Sumw2()
    hist_num.Sumw2()
    tree.Project("h1","amp[%i]>0"%ch,"amp[%i]>%f&&amp[%i]>%i"%(ch_amp,minAmp,ch_photek,minPh))
    tree.Project("h2","amp[%i]>400"%ch,"amp[%i]>%f&&amp[%i]>%i"%(ch_amp,minAmp,ch_photek,minPh))

    hist_eff = hist_num.Clone("h_disc_eff")
    hist_eff.Divide(hist_num, hist_den,1,1,"B");
    outfile.cd()
    hist_eff.Write()
       
    #print(cfg,ch_amp)
    #print("EFF ", hist_eff.GetBinContent(2))

    return 
    
def get_config_results(cfg,opt=""):
    
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
    tree = ROOT.TChain("pulse")
    for i,run in enumerate(runs):

        rootfile = "root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/{}/run_scope{}_converted.root".format(version(run),run)
        tree.Add(rootfile)

        testfile = ROOT.TFile.Open(rootfile)
        if not testfile : print("MISSING : {} {}".format(cfg,run))

    # Generic plots per channel for now
    # May get more specific later (by ch and cfg)
    for ch in range(0,3): # skip photek

        # for speed
        if (is_discrim(ch,cfg) or is_etroc_amp(ch,cfg)) and "IBSel" not in cfg: continue  
        if not is_discrim(ch,cfg) and not is_etroc_amp(ch,cfg) and "IBSel" in cfg: continue

        # more speed
        if "ETROC_amp" in opt and not is_etroc_amp(ch,cfg) : continue
        if "ETROC_dis" in opt and not is_discrim(ch,cfg) : continue
        if "UCSC" in opt and (is_discrim(ch,cfg) or is_etroc_amp(ch,cfg)) : continue
        
        outname = "plots/configs/root/{}_ch{}.root".format(cfg,ch)
        outfile = ROOT.TFile.Open(outname,"RECREATE")
        print(outfile)
    
        # Amplifier basics  
        get_mean_amplitude_channel(tree,cfg,ch,outfile)
        get_charge_channel(tree,cfg,ch,outfile)
        get_slew_rate_channel(tree,cfg,ch,outfile)
        get_risetime_channel(tree,cfg,ch,outfile)
        get_baseline_RMS_channel(tree,cfg,ch,outfile)
        get_time_CFD(tree,cfg,ch,outfile)

        global_conf = int_conf(cfg) 
        if global_conf > 146 and is_etroc_amp(ch,cfg) : 
            get_tot_channel(tree,cfg,ch,outfile)
            totparams = get_time_walk(tree,cfg,ch,outfile)
            get_time_TOT(tree,cfg,ch,totparams,outfile)

        # Discriminator stuffs
        if is_discrim(ch,cfg): 
            ch_amp = get_amp_ch(ch,cfg) 
            totparams = get_time_walk(tree,cfg,ch,outfile)
            get_time_TOT(tree,cfg,ch,totparams,outfile)
            get_disc_eff(tree,cfg,ch,ch_amp,outfile)
            get_tot_channel(tree,cfg,ch,outfile)
        # TODO : 
        #   timewalk 
        #   TOT
        #   time res TOT
        #   amp amp v amp TOT
        #   amp amp v dis TOT
        #   amp TOT v dis TOT
    
    return
        
def get_configurations():
    # Loop through configurations 
    cfg_list = open("configs/configurations.txt","r")
    for i,line in enumerate(cfg_list): 
     
        # for tmp debugging
        #if i > 0: break 
        #if "148_IBSel_0b111_RFSel_3_DAC_228" not in line: continue
        global_conf = int_conf(line.strip()) 
        #if global_conf > 139: continue # amplifiers only
        if global_conf < 146 : continue 
        #if global_conf > 180 : continue
        #if global_conf != 135 : continue
        #if not ("189" in line or "190" in line ): continue
        #if "185_IBSel_0b111_RFSel_3_DAC_318" not in line : continue
        #if "148_IBSel_0b111_RFSel_3_DAC_248" not in line : continue
        #if "148_IBSel_0b111_RFSel_3_DAC_228" not in line: continue
        #if "153_IBSel_0b000_RFSel_3_DAC_334" not in line : continue
        #if "153" not in line : continue
        #if "190_IBSel_0b000_RFSel_3_DAC_424" not in line : continue 
        if "151" not in line : continue

        if "#" in line: continue
        cfg = line.strip()
        get_config_results(cfg,"ETROC_amp")
        get_config_results(cfg)

# Main
if __name__ == "__main__":
    # execute only if run as a script
    #main()
    get_configurations()

