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

analysissettings={'smooth_scale_2D':0.5,
'smooth_scale_1D': 0.4,
'ignore_rows': u'0.3',
'fine_bins_2D': u'750',
'fine_bins': u'750',
'num_bins_2D': u'450',
'num_bins': u'450',
'range_confidence' : u'0.025'
}

analysissettings2={'smooth_scale_2D':0.5,
'smooth_scale_1D': 0.4,
'ignore_rows': u'0.3',
'fine_bins_2D': u'750',
'fine_bins': u'750',
'num_bins_2D': u'450',
'num_bins': u'450',
'range_confidence' : u'0.025'
}

samples=loadMCSamples('../chains/EXAMPLE_MCMC1',settings=analysissettings)
p = samples.getParams()

samples.addDerived(10*p.ns,name='ns10',label='10 n_s',
	range=[10*samples.getLower('ns'),10*samples.getUpper('ns')])

samples.addDerived(10*p.omegam,name='omegam10',label='10 \Omega_m')

samples.addDerived(100*p.omegab,name='omegab100',label='100 \Omega_b')

samples.saveAsText('VM_TMP_P3_0')

samples=loadMCSamples('../chains/EXAMPLE_MCMC3',settings=analysissettings)
p = samples.getParams()

samples.addDerived(10*p.ns,name='ns10',label='10 n_s',
	range=[10*samples.getLower('ns'),10*samples.getUpper('ns')])

samples.addDerived(10*p.omegam,name='omegam10',label='10 \Omega_m')

samples.addDerived(100*p.omegab,name='omegab100',label='100 \Omega_b')

samples.saveAsText('VM_TMP_P3_1')

g=gplot.getSubplotPlotter(chain_dir=r'./',analysis_settings=analysissettings2,width_inch=7.25)
g.settings.lw_contour = 1.2
g.settings.legend_rect_border = False
g.settings.figure_legend_frame = False
g.settings.axes_fontsize = 9.15
g.settings.legend_fontsize = 17.5
g.settings.alpha_filled_add = 0.7
g.settings.lab_fontsize=14.5
g.legend_labels=False

roots = [
'VM_TMP_P3_0',
'VM_TMP_P3_1'
]
params = ['sigma8','s8omegamp5','omegam',
'DES_M1','DES_M2','DES_M3','DES_M4','DES_DZ_S1','DES_DZ_S2','DES_DZ_S3','DES_DZ_S4']
param_3d = None
g.triangle_plot(roots,params,
plot_3d_with_param=param_3d,
filled=True,
shaded=False,
imax_shaded=0,
line_args=[
{'lw': 1.8,'ls': '--', 'color':'royalblue'},
{'lw': 1.0,'ls': 'solid', 'color':'black'},
{'lw': 1.2,'ls': 'solid', 'color':'firebrick'}
],
legend_labels=[
'Shear, Parameterization 1',
'Shear, Parameterization 2'
],
legend_loc=(0.50,0.75),
contour_ls=['--','solid','solid'],
contour_lws=[2.0,1.0,1.2],
contour_colors=['royalblue','black','firebrick']
)

g.export()

#DELETE TMP FILES
subprocess.Popen("rm VM_TMP_P3_[0-9].*", shell=True, cwd=".")
