def tot_cleaning(cfg):
    # assuming only applying to discriminator channel
    mintot=0.5
    maxtot=10
    #if   "148_IBSel_0b000_RFSel_3_DAC_333" in cfg : maxtot=6.5 
    #elif "153_IBSel_0b000_RFSel_3_DAC_334" in cfg : maxtot=7.0

    #mintot = mintot * 1e-9
    #maxtot = maxtot * 1e-9
    print(mintot,maxtot)
    return mintot,maxtot
