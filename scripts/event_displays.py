import ROOT 

ROOT.gROOT.SetBatch(ROOT.kTRUE)

def event_display(f,t,evt,col):
    c = ROOT.TCanvas()
    #ROOT.gStyle.SetMarkerColor(ROOT.kRed)
    t.Draw("channel[2]:time[0]","i_evt=={}".format(evt),"l")
    #ROOT.gStyle.SetMarkerColor(ROOT.kBlue)
    t.Draw("channel[1]:time[0]","i_evt=={}".format(evt),"lsame")
    #ROOT.gStyle.SetMarkerColor(ROOT.kBlack)
    t.Draw("channel[3]:time[0]","i_evt=={}".format(evt),"lsame")
    
    #h1 = f.Get("h1")
    #h2 = f.Get("h2")
    #h3 = f.Get("h3")
    
    #h1.SetMarkerColor(ROOT.kBlue)
    #h2.SetMarkerColor(ROOT.kRed)
    #h3.SetMarkerColor(ROOT.kBlack)
    #h1.SetLineColor(ROOT.kBlue)
    #h2.SetLineColor(ROOT.kRed)
    #h3.SetLineColor(ROOT.kBlack)

    #h1.GetYaxis().SetRangeUser(-750,50)
    #h1.Draw("lsame")
    #h2.Draw("lsame")
    #h3.Draw("lsame")

    c.Print("plots/eventDisplays/{}_event{}.png".format(col,evt))

f = ROOT.TFile.Open("root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v2/run_scope27664_converted.root")

t = f.Get("pulse") 

black_events = []
black_events.append( 1993)
black_events.append( 7417)
black_events.append(14409)
black_events.append(20704)
black_events.append(23857)
black_events.append(23963)
black_events.append(24368)
black_events.append(25337)
black_events.append(25692)
black_events.append(31598)
black_events.append(32123)
black_events.append(33158)
black_events.append(34307)
black_events.append(35011)
black_events.append(35497)
black_events.append(40246)
black_events.append(41941)
black_events.append(45212)
black_events.append(46608)
black_events.append(49149)
black_events.append(51388)
black_events.append(52234)
black_events.append(54525)
black_events.append(55533)

red_events = []
red_events.append(  138) 
red_events.append( 3597) 
red_events.append( 4575) 
red_events.append( 5128) 
red_events.append( 5747) 
red_events.append( 6672) 
red_events.append( 9161) 
red_events.append(10026) 
red_events.append(11286) 
red_events.append(13437) 
red_events.append(13876) 
red_events.append(15070) 
red_events.append(16479) 
red_events.append(17941) 
red_events.append(18690) 
red_events.append(18937) 
red_events.append(19217) 
red_events.append(24455) 
red_events.append(25541) 
red_events.append(30025) 
red_events.append(31019) 
red_events.append(33764) 
red_events.append(38490) 
red_events.append(38575) 
red_events.append(41209) 
red_events.append(41979) 
red_events.append(44325) 
red_events.append(44450) 
red_events.append(44798) 
red_events.append(45842) 
red_events.append(46390) 
red_events.append(47402) 
red_events.append(47833) 
red_events.append(49838) 
red_events.append(51585) 
red_events.append(54087) 
red_events.append(54458) 
red_events.append(57467) 
normal_events=[]
normal_events.append( 35) 
normal_events.append( 36) 
normal_events.append( 44) 
normal_events.append( 54) 
normal_events.append( 65) 
normal_events.append( 70) 
normal_events.append( 75) 
normal_events.append( 79) 
normal_events.append( 96) 
normal_events.append(116) 
normal_events.append(156) 
normal_events.append(158) 
normal_events.append(162) 
normal_events.append(163) 
normal_events.append(220) 
normal_events.append(223) 
normal_events.append(226) 
normal_events.append(235) 
normal_events.append(254) 
normal_events.append(301) 
for evt in black_events:
    event_display(f,t,evt,"black")
for evt in red_events: 
    event_display(f,t,evt,"red")
for evt in normal_events:
    event_display(f,t,evt,"normal")