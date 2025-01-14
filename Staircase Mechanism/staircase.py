# Differetial  Privacy is the mathematical framework for preserving the privacy of individuals in 
# numerical datasets. It prevents the individual records by adding noise to datasets. It can provide 
# a sorority of privacy by allowing numerical data analysis without revealing sensitive information 
# of any individuals. The Staircase is another noise-adding mechanism, a geometric mixture of uniform 
# random variables. It can replace the laplacian noise-adding mechanisms in every category, such as 
# differential privacy, performance, and much improvement in the medium-low privacy regimes. 
# The staircase mechanism is the optimal noise-adding mechanism. i.e., the Staircase mechanism 
# is an optimal version of the Laplace Mechanisms.

import secrets
# from diffprivlib.mechanisms.laplace import Laplace
from laplace import Laplace
from diffprivlib.utils import copy_docstring
from numbers import Real
import numpy as np

# The staircase mechanism in differential privacy.
# The staircase mechanism is viewed as a geometric mixture of uniform random variables easily generated 
# by algorithms. The staircase mechanisms have three parameters: Є, Δ, and γ. Є – set by differential 
# privacy constraints. Δ is set by the global sensitivity of the query functions, and γ [0, 1] is a 
# free parameter related to the special cost function being considered.

# Parameters description
# epsilon : float 
#     Privacy parameter : epsilon for the mechanism.  Must be in (0, ∞].

# sensitivity : float
#     The sensitivity of the mechanism.  Must be in [0, ∞).

# gamma : float
#     Default: 1 / (1 + exp(epsilon/2))
#     Value of the tuning parameter gamma for the mechanism.  Must be in [0, 1].

# 'random-state' : int : optional
#     Controls the randomness of the mechanism. To obtain a deterministic behaviour during randomisation,
#     'random-state' has to be fixed to an integer.

# epsilon, Є: as lower the value privacy increases
# sensitivity, Δ: global 
#   Definition- Sensitivity measures the maximum change in the query function’s output that can result from 
#   altering a single element in the dataset.
# gamma, γ: 



class Staircase(Laplace):
    def __init__(self, *, epsilon, sensitivity, gamma=1, random_state=1):
        super().__init__(epsilon=epsilon, delta=0, sensitivity=sensitivity, random_state=random_state)
        self.gamma = self._check_gamma(gamma, epsilon=self.epsilon)

        if isinstance(self._rng, secrets.SystemRandom):
            self._rng = np.random.default_rng()

    @classmethod
    def _check_gamma(cls, gamma, epsilon=None):
        if gamma is None and epsilon is not None:
            gamma = 1 / (1 + np.exp(epsilon / 2))  # Calculation of gamma value

        if not isinstance(gamma, Real):
            raise TypeError("data type of gamma value is numrical")
        if not 0.0 <= gamma <= 1.0:
            raise ValueError("range of gamma value in interval [0,1]")

        return float(gamma)

    @copy_docstring(Laplace._check_all)
    def _check_all(self, value):
        super()._check_all(value)
        self._check_gamma(self.gamma)

        return True

    @classmethod
    def _check_epsilon_delta(cls, epsilon, delta):
        if not delta == 0:
            raise ValueError("the value of delta is not zero")

        return super()._check_epsilon_delta(epsilon, delta)


    @copy_docstring(Laplace.bias)
    def bias(self, value):
        return 0.0

    @copy_docstring(Laplace.variance)
    def variance(self, value):
        self._check_all(value)
        shape = self.sensitivity / self.epsilon
        variance = value ** 2 + shape * (self.lower * np.exp((self.lower - value) / shape) - self.upper * np.exp((value - self.upper) / shape))
        variance += (shape ** 2) * (2 - np.exp((self.lower - value) / shape) - np.exp((value - self.upper) / shape))
        variance -= (self.bias(value) + value) ** 2
        return variance


# staircase noise adding machanisms - Algorithms
    @copy_docstring(Laplace.randomise)
    def randomise(self, value):
        self._check_all(value)
        
        # 1. Generate a r.v. S with Pr(S=1) = Pr(S=-1) = ½. S shows the sign of noise
        # S = -1 if self._rng.random() < 0.5 else 1   
        S = np.random.choice([-1, 1])

        # 2. Generate Geometric r.v. G with Pr(G = i) = (1-b) bi. for integer i ≥ 0, b = e-Є. G shows the interval of noise lies.
        G = self._rng.geometric(1 - np.exp(- self.epsilon)) - 1

        # 3. Generate a r.v. U uniformly distributed in [0, 1]. U helps in uniform sample the subinterval
        # U = self._rng.random()
        U = np.random.uniform(0.0, 1.0)

        # 4. Generate a binary r.v. B with Pr(B=0) = γ/ (γ+(1- γ)b) and Pr(B=1) = (1- γ)b/( γ+(1- γ)b).  B shows the subinterval of noise lies.
        B = 0 if self._rng.random() < self.gamma / (self.gamma + (1 - self.gamma) * np.exp(- self.epsilon)) else 1

        # Staircase Mechanisms Noise
        X = S * ((1 - B) * ((G + self.gamma * U) * self.sensitivity) + B * ((G + self.gamma + (1 - self.gamma) * U) * self.sensitivity))

        # return Actual Value with Noise (X)
        return value + X
    
    # This is how to calculate staircase mechanisms as given in the research paper.



