# compare two methods



# for C=0.4,r=0.255,sigma=0.5,
# for we got L=0.6447544806294948, L1=0.6447544806294638, L2=1.5574496651260241,H=1.5574496651259984, V=1.3440054417027154



C=0.4
r=0.255
sigma=0.5

from v3pricingEuro import _get_best_range
from v3pricingAmerican import uni_v3_pricing_earlyexcu_version_analytic_solution_optimize

print(_get_best_range(C, sigma, r))
print(uni_v3_pricing_earlyexcu_version_analytic_solution_optimize(r, C, sigma))
