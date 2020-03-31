from array import array
from style import setStyle
from tot_cleaning import tot_cleaning
from configs import get_min_time
from configs import get_max_time
from configs import version
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

# default parameters
ch_photek=3 # photek channel
minPh = 50 #mV 
maxPh = 100 #mV


def get_min_amp(cfg,ch):
    return 50
def get_max_amp(cfg,ch):
    return 750
def get_amp_str(cfg,ch):
    minAmp = get_min_amp(cfg,ch)
    maxAmp = get_max_amp(cfg,ch)
    amp_str = "amp[{}]>{}&&amp[{}]<{}".format(ch,minAmp,ch,maxAmp)
    return amp_str

def get_slice( split ) :
    if split == 0: return 15,17
    if split == 1: return 17,18
    if split == 2: return 18,19
    if split == 3: return 19,20
    if split == 4: return 20,21
    if split == 5: return 22,23
    if split == 6: return 23,25 
    return -1,-1

def get_slice_string(split,ch): 
    
    charge_str = "-1000*integral[%i]*1e9*50/33000"%(ch)
    min_ch,max_ch = get_slice( split ) 
    slice_str = "{}>{}&&{}<{}".format(charge_str,min_ch,charge_str,max_ch)
    return slice_str
    
def get_tree(cfg):
    
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

    return tree
def get_charge_channel(tree,cfg,ch,outfile):
       
    minAmp = get_min_amp(ch,cfg)
    transimpedance = 33000 # SF to make charge match UCSC 

    hist = ROOT.TH1D("h_charge","",50,0,100)

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

    c.Print("plots/landau/{}_ch{}_charge.pdf".format(cfg,ch))

    return 

def get_amplitudes(tree,cfg,ch,outfile):

    hists = []
    means = []
    errs = []
    for i in range(0,7):
        slice_str = get_slice_string(i,ch)
        amp_str = get_amp_str(cfg,ch)

        hist = ROOT.TH1D("h_amplitude_{}".format(i),"",75,0,750)
        tree.Project("h_amplitude_{}".format(i),"amp[%i]"%ch,"{}&&{}".format(slice_str,amp_str))

        hist.SetTitle(";Amplitude [mV];Events")
        hist.SetLineColor(colors[i])
    
        outfile.cd()
        hist.Write()

        means.append(hist.GetMean())
        errs.append(hist.GetMeanError())
        hists.append(hist)

    return hists,means,errs

def get_times(tree,cfg,ch,outfile):

    minT = get_min_time(ch,cfg)
    maxT = get_max_time(ch,cfg)
    hists=[]
    means=[]
    errs=[]
    tres=[]
    tres_err=[]
    for i in range(0,7):
        slice_str = get_slice_string(i,ch)
        amp_str = get_amp_str(cfg,ch)

        hist = ROOT.TH1D("h_time_{}".format(i),"",75,minT,maxT)
        sel_str = "amp[%i]>%f && amp[%i]<%f && LP2_15[%i]!=0 && LP2_20[%i]!=0"%(ch_photek,minPh,ch_photek,maxPh,ch,ch_photek)
        tree.Project("h_time_{}".format(i),"LP2_15[%i]-LP2_20[%i]"%(ch,ch_photek),"{}&&{}&&{}".format(sel_str,slice_str,amp_str))

        hist.SetTitle(";t_{0}-t_{ref} [s];Events")
        
        f1 = ROOT.TF1("f_time_{}".format(i),"gaus",minT,maxT)
        hist.Fit(f1,"Q")

        outfile.cd()
        hist.Write()
        f1.Write()
        
        hists.append(hist)
        means.append(1e9*f1.GetParameter(1))
        errs.append(1e9*f1.GetParError(1))
        tres.append(1e12*f1.GetParameter(2))
        tres_err.append(1e12*f1.GetParError(2))
    
    return hists,means,errs,tres,tres_err

def draw_hists(cfg,ch,hists,name):
    c = ROOT.TCanvas()
    ymax = 0
    for i,hist in enumerate(hists): 
        hist.SetLineColor(colors[i])
        hist.SetLineWidth(2)
        if hist.GetMaximum() > ymax: ymax = hist.GetMaximum()
        if i==0: hist.Draw("")
        else   : hist.Draw("same")
    hists[0].SetMaximum(ymax*1.3)
    c.Print("plots/landau/{}_ch_{}_{}.pdf".format(cfg,ch,name))
    return
       
def slice_arrays(): 
    x = []
    xerr = []
    for i in range(0,7):
        minc,maxc=get_slice(i)
        x.append( (maxc+minc)/2.0 )
        xerr.append( (maxc-minc)/2.0 )
    return x,xerr
    
def cosmetics(graph,colorindex,tb=False):
    graph.SetLineColor(colors[colorindex])
    graph.SetMarkerColor(colors[colorindex])
    graph.SetMarkerSize(0.75)
    graph.SetMarkerStyle(20)
    if tb:
        graph.SetMarkerSize(2)
        #graph.SetMarkerStyle(29)
    return 
def draw_graph(cfg,ch,y,yerr,outfile,name):
    x,xerr = slice_arrays() 
    
    g = ROOT.TGraphErrors(len(x),array("d",x),array("d",y),array("d",xerr),array("d",yerr))
    cosmetics(g,0)
    g.SetName("gr_{}".format(name))
    g.GetXaxis().SetTitle("charge [fC]")
    g.GetYaxis().SetTitle(name)

    c = ROOT.TCanvas()
    g.Draw()
    c.Print("plots/landau/graph_{}_ch{}_{}.pdf".format(cfg,ch,name))

    outfile.cd()
    g.Write()

    return

def plot_overlay(outfile, grs, biases, boards, temps, configs, name): 
    c = ROOT.TCanvas()
    c.SetGridy()
    c.SetGridx()

    mgraph = ROOT.TMultiGraph()
    leg = ROOT.TLegend(0.17,0.71,0.56,0.88)
    leg.SetMargin(0.15)

    for i,graph in enumerate(grs):
        cosmetics(graph,i)
        mgraph.Add(graph)
        label = "ETROC#{}, {}V, {}C".format(boards[i],biases[i],temps[i])
        if "0b000" in configs[i]: label = label + " High power"
        if "0b111" in configs[i]: label = label + " Low power"
        leg.AddEntry(graph, label ,"EP")
    
    yaxis=""
    if "amp" in name: yaxis = "MPV amplitude [mV]"
    if "tdiff" in name: yaxis = "mean t_{0} - t_{ref} (CFD) [ns]"
    if "tres" in name: yaxis = "amplifier time res. (CFD) [ns]"
    mgraph.SetTitle("; collected charge [fC]; %s"%(yaxis) )
    mgraph.Draw("ALEP")
    adjust(mgraph,gr_name)
    leg.Draw() 
    c.Print("plots/landau/series_{}.pdf".format(name))
    
    return

def get_configs():

    configs = []
    biases = []
    boards = []
    chans = []
    temps = []
    

    gr_amps = []
    gr_tdiffs = []
    gr_tress = []
    cfg_list = open("configs/configurations_landau.txt","r")
    for line in cfg_list: 
        if "#" in line: continue
        lin = line.split()
        cfg = lin[0]
        ch = int(lin[3])
        configs.append( cfg )
        biases.append( lin[1] )
        temps.append( lin[2] )
        chans.append( ch )
        boards.append( lin[4] )

        tree = get_tree(cfg) 
        outname = "plots/configs/root/{}_ch{}.root".format(cfg,ch)
        outfile = ROOT.TFile.Open(outname,"RECREATE")
        print(outfile)

        get_charge_channel(tree,cfg,ch,outfile) 
        hists_amp,mean_amps,err_amps = get_amplitudes(tree,cfg,ch,outfile)
        hists_time,mean_times,err_times,tres,err_tres = get_times(tree,cfg,ch,outfile)
        
        # draw
        draw_hists(cfg,ch,hists_amp,"amplitude")
        draw_hists(cfg,ch,hists_time,"time")

        # graph
        gr_amp   = draw_graph(cfg,ch,mean_amps ,err_amps ,outfile,"amp")
        gr_tdiff = draw_graph(cfg,ch,mean_times,err_times,outfile,"tdiff")
        gr_tres  = draw_graph(cfg,ch,tres      ,err_tres ,outfile,"tres")
    
        gr_amps.append(gr_amp)
        gr_tdiffs.append(gr_tdiff)
        gr_tress.append(gr_tres)

    # done with cfgs
    plot_overlay(outfile, gr_amps  , biases, boards, temps, cfg, "amp") 
    plot_overlay(outfile, gr_tdiffs, biases, boards, temps, cfg, "tdiff") 
    plot_overlay(outfile, gr_tress , biases, boards, temps, cfg, "tres") 
    return 

get_configs()

#153_IBSel_0b111_RFSel_3_DAC_221 220 20 1 9
#153_IBSel_0b000_RFSel_3_DAC_334 220 20 1 9
#149_IBSel_0b111_RFSel_3_DAC_228 220 20 0 11
#149_IBSel_0b000_RFSel_3_DAC_333 220 20 0 11
