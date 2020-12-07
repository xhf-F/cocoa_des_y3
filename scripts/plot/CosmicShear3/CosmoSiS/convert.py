import os
import numpy as np

def main():
  try :
    name = "chain_1x2final.txt"
    CHAIN = np.loadtxt(name,skiprows=0)
  except IOError :
    print "error reading file"
    exit(1)
  np.savetxt('gd_chain_1x2final.txt',CHAIN,delimiter=' ')

  try :
    name = "chain_3x2pt_lcdm.txt"
    CHAIN = np.loadtxt(name,skiprows=0)
  except IOError :
    print "error reading file"
    exit(1)
  np.savetxt('gd_chain_3x2pt_lcdm.txt',CHAIN,delimiter=' ')

if __name__ == "__main__": main()
