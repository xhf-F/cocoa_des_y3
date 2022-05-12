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

# ---- SET LIMITS OF THE EMULATOR (IT SEEMS ALREADY CLOSE TO THE ACTUAL POSTERIORS)
omm_min = 0.24
omm_max = 0.40 
omb_min = 0.04 
omb_max = 0.06 
ns_min = 0.92 
ns_max = 1.00 
h_min = 0.61 
h_max = 0.73 
As_min = 1.7e-9 
As_max = 2.5e-9
w_min = -1.3
w_max = -0.7

parameter = [u'omegam',u'ns',u'H0',u'SS8']
chaindir=r'.'

analysissettings={'smooth_scale_1D':0.25,'smooth_scale_2D':0.25,'ignore_rows': u'0.35',
'range_confidence' : u'0.005'}

analysissettings2={'smooth_scale_1D':0.25,'smooth_scale_2D':0.25,'ignore_rows': u'0.0',
'range_confidence' : u'0.005'}

root_chains = ('EXAMPLE_MCMC4','EXAMPLE_MCMC5','EXAMPLE_MCMC14','EXAMPLE_MCMC15',)

# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[0],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\\Omega_m h}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='SS8',label='{S_8}')
samples.thin(factor = int(len(samples.weights)/20000))
samples.deleteZeros()
samples.ranges.setRange('ns', [ns_min, ns_max])
samples.ranges.setRange('omegam_growth', [omm_min, omm_max])
samples.ranges.setRange('omegam', [omm_min, omm_max])
samples.ranges.setRange('w', [w_min, w_max])
samples.ranges.setRange('w_growth', [w_min, w_max])
samples.ranges.setRange('H0', [100*h_min, 100*h_max])
samples.saveAsText('.VM_P4_TMP1')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[1],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='SS8',label='{S_8}')
samples.thin(factor = int(len(samples.weights)/20000))
samples.deleteZeros()
samples.ranges.setRange('ns', [ns_min, ns_max])
samples.ranges.setRange('omegam_growth', [omm_min, omm_max])
samples.ranges.setRange('omegam', [omm_min, omm_max])
samples.ranges.setRange('w', [w_min, w_max])
samples.ranges.setRange('w_growth', [w_min, w_max])
samples.ranges.setRange('H0', [100*h_min, 100*h_max])
samples.saveAsText('.VM_P4_TMP2')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[2],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='SS8',label='{S_8}')
samples.thin(factor = int(len(samples.weights)/20000))
samples.deleteZeros()
samples.ranges.setRange('ns', [ns_min, ns_max])
samples.ranges.setRange('omegam_growth', [omm_min, omm_max])
samples.ranges.setRange('omegam', [omm_min, omm_max])
samples.ranges.setRange('w', [w_min, w_max])
samples.ranges.setRange('w_growth', [w_min, w_max])
samples.ranges.setRange('H0', [100*h_min, 100*h_max])
samples.saveAsText('.VM_P4_TMP3')
# --------------------------------------------------------------------------------
samples=loadMCSamples('./' + root_chains[3],settings=analysissettings)
p = samples.getParams()
samples.addDerived(p.omegam*p.H0/100.,name='gamma',label='{\Gamma}')
samples.addDerived(p.s8omegamp5/0.5477225575,name='SS8',label='{S_8}')
samples.thin(factor = int(len(samples.weights)/20000))
samples.deleteZeros()
samples.ranges.setRange('ns', [ns_min, ns_max])
samples.ranges.setRange('omegam_growth', [omm_min, omm_max])
samples.ranges.setRange('omegam', [omm_min, omm_max])
samples.ranges.setRange('w', [w_min, w_max])
samples.ranges.setRange('w_growth', [w_min, w_max])
samples.ranges.setRange('H0', [100*h_min, 100*h_max])
samples.saveAsText('.VM_P4_TMP4')
# --------------------------------------------------------------------------------

#GET DIST PLOT SETUP
g=gplot.getSubplotPlotter(chain_dir=chaindir,
analysis_settings=analysissettings2,width_inch=8.0)
g.settings.axis_tick_x_rotation=65
g.settings.lw_contour = 1.2
g.settings.legend_rect_border = False
g.settings.figure_legend_frame = False
g.settings.axes_fontsize = 14.0
g.settings.legend_fontsize = 13.
g.settings.alpha_filled_add = 0.7
g.settings.lab_fontsize=20
g.legend_labels=False

param_3d = None
g.triangle_plot(['.VM_P4_TMP1','.VM_P4_TMP2','.VM_P4_TMP3', '.VM_P4_TMP4'],parameter,
plot_3d_with_param=param_3d,line_args=[
{'lw': 2.0,'ls': 'solid', 'color':'firebrick'},
{'lw': 1.2,'ls': 'solid', 'color':'indigo'},
{'lw': 2.0,'ls': '-.', 'color': 'firebrick'},
{'lw': 2.0,'ls': '-.', 'color': 'indigo'},
],
contour_colors=['firebrick','indigo','firebrick','indigo'],
contour_ls=['solid','solid','-.','-.'], 
contour_lws=[1.0,1.0,2.0,2.0],
filled=[True,True,False,False],
shaded=False,
legend_labels=[
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (33 < $\\ell$ < 396) + DES-Y1 (Cosmic Shear)', 
'Planck low-$\\ell_{\\mathrm{EE}}$ + Planck high-$\\ell_{\\mathrm{TTTEEE}}$ (33 < $\\ell$ < 396) + DES-Y3 (Cosmic Shear)',
'SN Pantheon + BAO + BBN + DES-Y1 (Cosmic Shear)',
'SN Pantheon + BAO + BBN + DES-Y3 (Cosmic Shear)'
],
legend_loc=(0.32,0.82))

# Vertical Line - Omegam
for ax in g.subplots[:,0]:
  if ax is not None:
    ax.axvline(0.3166,color='gray', ls='--',alpha=0.3)
# Vertical Line - ns
for ax in g.subplots[:,1]:
  if ax is not None:
    ax.axvline(0.9649, color='gray', ls='--',alpha=0.3)
# Vertical Line - H0
for ax in g.subplots[:,2]:
  if ax is not None:
    ax.axvline(67.32, color='gray', ls='--',alpha=0.3)
for ax in g.subplots[:,3]:
  if ax is not None:
    ax.axvline(0.83557, color='gray', ls='--',alpha=0.3)

# Horizontal - ns
for ax in g.subplots[1,0:1]:
  if ax is not None:
    ax.axhline(0.9649, color='gray', ls='--',alpha=0.3)
for ax in g.subplots[2,0:2]:
  if ax is not None:
    ax.axhline(67.32, color='gray', ls='--',alpha=0.3)
for ax in g.subplots[3,0:3]:
  if ax is not None:
    ax.axhline(0.83557, color='gray', ls='--',alpha=0.3)

g.export()