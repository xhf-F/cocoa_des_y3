import getdist.plots as gplot
from getdist import MCSamples
from getdist import loadMCSamples
import os
import matplotlib
import subprocess
import matplotlib.pyplot as plt
import numpy as np

# GENERAL PLOT OPTIONS
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
matplotlib.rcParams['xtick.bottom'] = True
matplotlib.rcParams['xtick.top'] = False
matplotlib.rcParams['ytick.right'] = False
matplotlib.rcParams['axes.edgecolor'] = 'black'
matplotlib.rcParams['axes.linewidth'] = '1.0'
matplotlib.rcParams['axes.labelsize'] = 'medium'
matplotlib.rcParams['axes.grid'] = True
matplotlib.rcParams['grid.linewidth'] = '0.0'
matplotlib.rcParams['grid.alpha'] = '0.18'
matplotlib.rcParams['grid.color'] = 'lightgray'
matplotlib.rcParams['legend.labelspacing'] = 0.77
matplotlib.rcParams['savefig.bbox'] = 'tight'
matplotlib.rcParams['savefig.format'] = 'pdf'

# ADDING NEFF AS DERIVED PARAMETER
parameter = [u'omegam_growth',u'DES_DZ_S1',u'DES_DZ_S2',u'DES_DZ_S3',u'DES_DZ_S4']
chaindir=r'.'

analysissettings={'smooth_scale_1D':0.35,'smooth_scale_2D':0.35,'ignore_rows': u'0.35',
'range_confidence' : u'0.025'}

analysissettings2={'smooth_scale_1D':0.35,'smooth_scale_2D':0.35,'ignore_rows': u'0.0',
'range_confidence' : u'0.025'}

root_chains = ('EXAMPLE_MCMC6', 'EXAMPLE_MCMC5','EXAMPLE_MCMC2', 'EXAMPLE_MCMC1', 
'EXAMPLE_MCMC8', 'EXAMPLE_MCMC7')

# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[0],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\\Omega_m h}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P5v3_TMP1')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[1],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P5v3_TMP2')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[2],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P5v3_TMP3')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[3],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P5v3_TMP4')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[4],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P5v3_TMP5')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[5],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P5v3_TMP6')
# --------------------------------------------------------------------------------

#GET DIST PLOT SETUP
g=gplot.getSubplotPlotter(chain_dir=chaindir,
analysis_settings=analysissettings2,width_inch=7.5)
g.settings.lw_contour = 1.2
g.settings.legend_rect_border = False
g.settings.figure_legend_frame = False
g.settings.axes_fontsize = 14.0
g.settings.legend_fontsize = 12.75
g.settings.alpha_filled_add = 0.7
g.settings.lab_fontsize=17
g.legend_labels=False

param_3d = None
g.triangle_plot(['.VM_P5v3_TMP1', '.VM_P5v3_TMP2','.VM_P5v3_TMP3', '.VM_P5v3_TMP4', 
  '.VM_P5v3_TMP5', '.VM_P5v3_TMP6'],parameter,
plot_3d_with_param=param_3d,line_args=[
{'lw': 1.0,'ls': 'solid', 'color':'royalblue'},
{'lw': 1.0,'ls': 'solid', 'color':'firebrick'},
{'lw': 2.0,'ls': '--', 'color':'royalblue'},
{'lw': 2.0,'ls': '--', 'color':'firebrick'},
{'lw': 2.5,'ls': '-.', 'color':'royalblue'},
{'lw': 2.5,'ls': '-.', 'color':'firebrick'}],
contour_colors=['royalblue','firebrick','royalblue','firebrick','royalblue','firebrick'],
filled=True,shaded=False,
legend_labels=[
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + DES-Y3', 
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + DES-Y1',
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + SN (JLA) + DES-Y3', 
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + SN (JLA) + DES-Y1',
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + SN (Roman) + DES-Y3', 
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + SN (Roman) + DES-Y1'],
legend_loc=(0.3,0.81),
imax_shaded=0)
g.export()