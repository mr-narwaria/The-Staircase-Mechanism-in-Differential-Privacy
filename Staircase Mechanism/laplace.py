from numbers import Real
import numpy as np
from diffprivlib.mechanisms.base import DPMechanism, TruncationAndFoldingMixin
from diffprivlib.utils import copy_docstring

#     The classical Laplace mechanism in differential privacy.
#     First proposed by Dwork, McSherry, Nissim and Smith.
#     Samples from the Laplace distribution are generated using 4 uniform variates, to prevent
#     against reconstruction attacks due to limited floating point precision.
#     Parameters
#     ----------
#     epsilon : float
#         Privacy parameter :math:`\epsilon` for the mechanism.  Must be in [0, ∞].
#     delta : float, default: 0.0
#         Privacy parameter :math:`\delta` for the mechanism.  Must be in [0, 1].  Cannot be simultaneously zero with
#         ``epsilon``.
#     sensitivity : float
#         The sensitivity of the mechanism.  Must be in [0, ∞).
#     random_state : int or RandomState, optional
#         Controls the randomness of the mechanism.  To obtain a deterministic behaviour during randomisation,
#         ``random_state`` has to be fixed to an integer.

class Laplace(DPMechanism):
    def __init__(self, *, epsilon, delta=0.0, sensitivity, random_state=None):
        super().__init__(epsilon=epsilon, delta=delta, random_state=random_state)
        self.sensitivity = self._check_sensitivity(sensitivity)
        self._scale = None

    @classmethod
    def _check_sensitivity(cls, sensitivity):
        if not isinstance(sensitivity, Real):
            raise TypeError("Sensitivity must be numeric")

        if sensitivity < 0:
            raise ValueError("Sensitivity must be non-negative")

        return float(sensitivity)

    def _check_all(self, value):
        super()._check_all(value)
        self._check_sensitivity(self.sensitivity)

        if not isinstance(value, Real):
            raise TypeError("Value to be randomised must be a number")

        return True

    def bias(self, value):
        return 0.0

    def variance(self, value):
        self._check_all(0)
        return 2 * (self.sensitivity / (self.epsilon - np.log(1 - self.delta))) ** 2

    @staticmethod
    def _laplace_sampler(unif1, unif2, unif3, unif4):
        return np.log(1 - unif1) * np.cos(np.pi * unif2) + np.log(1 - unif3) * np.cos(np.pi * unif4)


    def randomise(self, value):
        self._check_all(value)
        scale = self.sensitivity / (self.epsilon - np.log(1 - self.delta))
        standard_laplace = self._laplace_sampler(self._rng.random(), self._rng.random(), self._rng.random(), self._rng.random())
        return value + scale * standard_laplace

