import numpy as np


class GoodnessOfFitResults:
  def __init__(self, x_cond, estimator, probabilistic_model):
    self.cond_values = x_cond

    self.time_to_fit = None
    self.time_to_predict = None

    self.ndim_x = estimator.ndim_x
    self.ndim_y = estimator.ndim_y

    self.estimator_params = estimator.get_params()
    self.probabilistic_model_params = probabilistic_model.get_params()

    if estimator.ndim_y > 1: # cannot perform KS Test -> net respective variables to None
      self.ks_stat = None
      self.ks_pval = None
    else:
      self.ks_stat = np.zeros(x_cond.shape[0])
      self.ks_pval = np.zeros(x_cond.shape[0])


    self.mean_kl = None
    self.mean_ks_stat = None
    self.mean_ks_pval = None

  def compute_means(self):
    if self.ks_stat is not None and self.ks_pval is not None:
      self.mean_ks_stat = self.ks_stat.mean()
      self.mean_ks_pval = self.ks_pval.mean()

  def report_dict(self):
    full_dict = self.__dict__
    keys_of_interest = ["n_observations", "ndim_x", "ndim_y", "mean_kl", "mean_ks_stat", "mean_ks_pval", "time_to_fit", "time_to_predict"]
    report_dict = dict([(key, full_dict[key]) for key in keys_of_interest])

    get_from_dict = lambda key: self.estimator_params[key] if key in self.estimator_params else None

    for key in ["estimator", "n_centers", "center_sampling_method"]:
      report_dict[key] = get_from_dict(key)


    report_dict["simulator"] = self.probabilistic_model_params["simulator"]

    return report_dict

  def __len__(self):
    return 1


  def __str__(self):
    return "KL-Divergence: %.4f , KS Stat: %.4f, KS pval: %.4f"%(self.mean_kl, self.mean_ks_stat, self.mean_ks_pval)