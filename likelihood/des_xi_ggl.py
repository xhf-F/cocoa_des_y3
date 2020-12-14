from cobaya.likelihoods.des_y3._cosmolike_prototype_base import _cosmolike_prototype_base
import cosmolike_des_y3_interface as ci

class des_xi_ggl(_cosmolike_prototype_base):
	# ------------------------------------------------------------------------
	# ------------------------------------------------------------------------
	# ------------------------------------------------------------------------

	def initialize(self):
		super(des_xi_ggl,self).initialize(probe="xi_ggl")

	# ------------------------------------------------------------------------
	# ------------------------------------------------------------------------
	# ------------------------------------------------------------------------

	def logp(self, **params_values):
		self.set_cosmo_related()

		self.set_lens_related(**params_values)

		self.set_source_related(**params_values)

		datavector = ci.compute_data_vector()

		return self.compute_logp(datavector)

