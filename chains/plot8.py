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
parameter = [u'omegam',u'S8',u'ns',u'H0']
chaindir=r'.'

analysissettings={'smooth_scale_1D':0.35,'smooth_scale_2D':0.35,'ignore_rows': u'0.35',
'range_confidence' : u'0.015'}

analysissettings2={'smooth_scale_1D':0.35,'smooth_scale_2D':0.35,'ignore_rows': u'0.0',
'range_confidence' : u'0.015'}

root_chains = ('EXAMPLE_MCMC16','EXAMPLE_MCMC14','EXAMPLE_MCMC15','EXAMPLE_MCMC10')

# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[0],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\\Omega_m h}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P8_TMP1')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[1],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P8_TMP2')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[2],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P8_TMP3')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[3],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='S8',label='{S_8}')
samples.saveAsText('.VM_P8_TMP4')
# --------------------------------------------------------------------------------

#GET DIST PLOT SETUP
g=gplot.getSubplotPlotter(chain_dir=chaindir,
analysis_settings=analysissettings2,width_inch=7.5)
g.settings.lw_contour = 1.2
g.settings.legend_rect_border = False
g.settings.figure_legend_frame = False
g.settings.axes_fontsize = 14.0
g.settings.legend_fontsize = 13.75
g.settings.alpha_filled_add = 0.7
g.settings.lab_fontsize=17
g.legend_labels=False

param_3d = None
g.triangle_plot(['.VM_P8_TMP1', '.VM_P8_TMP2','.VM_P8_TMP3', '.VM_P8_TMP4'],parameter,
plot_3d_with_param=param_3d,line_args=[
{'lw': 1.2,'ls': 'solid', 'color':'cornflowerblue'},
{'lw': 2.0,'ls': '-.', 'color':'firebrick'},
{'lw': 2.0,'ls': '--', 'color': 'indigo'},
{'lw': 1.2,'ls': 'solid', 'color': 'darkgoldenrod'}],
contour_colors=['cornflowerblue','firebrick','indigo','darkgoldenrod'],
contour_ls=['solid','-.','--','solid'], 
contour_lws=[1.0,2.0,2.0,1.0],
filled=[True,False,False,True],
shaded=False,
legend_labels=[
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900)',
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + DES-Y3', 
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + SN (JLA)',
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (35 < $\\ell$ < 900) + SN (JLA) + DES-Y3', 
],
legend_loc=(0.315,0.81))
g.export()