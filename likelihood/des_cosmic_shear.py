from cobaya.likelihoods.des_y3._cosmolike_prototype_base import _cosmolike_prototype_base
import cosmolike_des_y3_interface as ci

class des_cosmic_shear(_cosmolike_prototype_base):
  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------

  def initialize(self):
    super(des_cosmic_shear,self).initialize(probe="xi")

  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------
  # ------------------------------------------------------------------------

  def logp(self, **params_values):
    self.set_cosmo_related()

    self.set_source_related(**params_values)

    if self.create_baryon_pca:
      self.generate_baryonic_PCA(**params_values)

    datavector = ci.compute_data_vector_masked()

    return self.compute_logp(datavector)
