import ROOT


def setStyle():
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.05,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"t")
    ROOT.gStyle.SetTitleSize(0.06,"xyz")
    ROOT.gStyle.SetTitleSize(0.06,"t")
    ROOT.gStyle.SetPadBottomMargin(0.14)
    ROOT.gStyle.SetPadLeftMargin(0.14)
    ROOT.gStyle.SetTitleOffset(1,'y')
    ROOT.gStyle.SetLegendTextSize(0.035)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridColor(14)
    ROOT.gStyle.SetOptFit(1)
    one   = ROOT.TColor(2001,0.906,0.153,0.094)
    two   = ROOT.TColor(2002,0.906,0.533,0.094)
    three = ROOT.TColor(2003,0.086,0.404,0.576)
    four  = ROOT.TColor(2004,0.071,0.694,0.18)
    five  = ROOT.TColor(2005,0.388,0.098,0.608)
    six   = ROOT.TColor(2006,0.906,0.878,0.094)
    colors = [1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006]
    return colors
