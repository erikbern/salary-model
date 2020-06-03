import contextlib, math, matplotlib, numpy, random
from matplotlib import pyplot
import scipy.optimize

data = [(737, 600), (780, 555), (895, 585), (1032, 763), (1091, 740), (1230, 731), (1332, 968), (1422, 871), (1600, 877), (1676, 1085), (1751, 988), (1803, 1101), (1924, 985), (2000, 1064), (2200, 1137), (2310, 1375), (2446, 1321)]
m = 2500

# Fit curve through the points
fn_0 = lambda x, alpha, beta: alpha*x**beta
res = scipy.optimize.minimize(lambda args: sum((y - fn_0(x, *args))**2 for x, y in data), (0, 0))
fn = lambda x: fn_0(x, *res.x)
lo1, hi1, hi2 = 0.9, 1.05, 1.3
fn_lo1 = lambda x: numpy.minimum(x, lo1*fn(x))
fn_hi1 = lambda x: numpy.minimum(x, hi1*fn(x))
fn_hi2 = lambda x: numpy.minimum(x, hi2*fn(x))
xs = numpy.linspace(0, m, 1000)

@contextlib.contextmanager
def plot(fignr, title):
    print('Plotting', fignr)
    pyplot.figure(figsize=(5, 4))
    # pyplot.grid(True, 'both', 'both')
    pyplot.gca().set_xticks([])
    pyplot.gca().set_yticks([])
    #pyplot.gca().set_yticklabels([])
    #pyplot.gca().set_xticklabels([])
    for dir in ['top', 'left', 'bottom', 'right']:
        pyplot.gca().spines[dir].set_visible(False)
    pyplot.plot([0, m], [0, m], alpha=0.05, color='black')
    arrowprops = dict(arrowstyle='<|-', color='black', lw=2, capstyle='projecting', shrinkA=0, shrinkB=0)
    pyplot.annotate('productivity', (0, 0), (m, 0), arrowprops=arrowprops, va='center', ha='left')
    pyplot.annotate('salary', (0, 0), (0, m), arrowprops=arrowprops, ha='center', va='bottom')
    yield
    pyplot.gca().set_aspect('equal', adjustable='box')
    pyplot.figtext(0.5, 0.02, 'Figure %d: %s' % (fignr, title), ha='center', style='italic', fontsize='x-small')
    pyplot.tight_layout()
    pyplot.savefig('figure-%d.png' % fignr, dpi=600)

# Base scatter
with plot(1, 'Distribution of salaries at CrazyBananaCo'):
    pyplot.scatter([x for x, y in data], [y for x, y in data], alpha=0.75, s=50, color='tab:blue')

# The market
with plot(2, 'Salaries aligned with the market rate and replacement cost at CrazyBananaCo'):
    pyplot.scatter([x for x, y in data], [y for x, y in data], alpha=0.75, s=50, color='tab:blue')
    pyplot.fill_between(xs, xs*0, fn_lo1(xs), linewidth=0, alpha=0.3, color='tab:cyan')
    pyplot.annotate('below\nmarket\nrate', (m, fn_lo1(m)/2), ha='left', va='center', color='tab:cyan')
    pyplot.fill_between(xs, fn_lo1(xs), fn_hi1(xs), linewidth=0, alpha=0.3, color='tab:blue')
    pyplot.annotate('market salary\nrange', (m, (fn_lo1(m) + fn_hi1(m))/2), ha='left', va='center', color='tab:blue')
    pyplot.fill_between(xs, fn_hi1(xs), fn_hi2(xs), linewidth=0, alpha=0.3, color='tab:purple')
    pyplot.annotate('below\nreplacement\ncost', (m, (fn_hi1(m) + fn_hi2(m))/2), ha='left', va='center', color='tab:purple')
    pyplot.fill_between(xs, fn_hi2(xs), xs, linewidth=0, alpha=0.3, color='tab:red')
    pyplot.annotate('above\nreplacement\ncost', (m, (m + fn_hi2(m))/2), ha='left', va='center', color='tab:red')
    pyplot.fill_between(xs, xs, [m for x in xs], linewidth=0, alpha=0.5, color='tab:red')
    pyplot.annotate('negative value add', (m/2, m), ha='center', va='bottom', color='tab:red')

xs_sorted = sorted(x for x, y in data)
ys_sorted = sorted(y for x, y in data)
cons_data = [(x, y) for x, y in zip(xs_sorted, ys_sorted)]

# New hire
with plot(3, 'Distribution of salaries at SuperFairCo'):
    pyplot.scatter([x for x, y in cons_data], [y for x, y in cons_data], alpha=0.75, s=50, color='tab:blue')

# New hire
with plot(4, 'New potential candidate at SuperFairCo'):
    pyplot.scatter([x for x, y in cons_data], [y for x, y in cons_data], alpha=0.75, s=50, color='tab:blue')
    new_x, new_y = 1500, 1200
    pyplot.scatter([new_x], [new_y], color='tab:purple', alpha=0.75)
    pyplot.annotate('candidate', (new_x, new_y), ha='right', va='top', color='tab:purple')
    pyplot.plot([new_x, new_x], [new_y, new_x], color='tab:pink')
    pyplot.annotate('value surplus', (new_x, new_x), ha='left', va='top', color='tab:pink')

# New hire inconsistencies
with plot(5, 'Inconsistency cost of hiring the new candidate at SuperFairCo'):
    pyplot.scatter([x for x, y in cons_data], [y for x, y in cons_data], alpha=0.75, s=50, color='tab:blue')
    pyplot.scatter([new_x], [new_y], color='tab:purple', alpha=0.75)
    pyplot.plot([new_x, m], [new_y, new_y], color='black', linestyle=':')
    i_xs, i_ys = [], []
    for x2, y2 in cons_data:
        if x2 > new_x and y2 < new_y:
            pyplot.annotate(None, (x2, y2), (x2, new_y), arrowprops=dict(arrowstyle='<|-', color='tab:red', shrinkA=0, shrinkB=0))
            i_xs.append(x2)
            i_ys.append(y2)
    pyplot.scatter(i_xs, [new_y for y in i_ys], alpha=0.5, s=50, color='tab:cyan')
    pyplot.annotate('inconsistencies', (numpy.median(i_xs), numpy.min(i_ys)), ha='center', va='bottom', color='tab:red')

# New hire range
with plot(6, 'Consistency-based salary range for the new hire at SuperFairCo'):
    pyplot.scatter([x for x, y in cons_data], [y for x, y in cons_data], alpha=0.75, s=50, color='tab:blue')
    min_y = max(y2 for x2, y2 in cons_data if x2 < new_x)
    max_y = min(y2 for x2, y2 in cons_data if x2 > new_x)
    pyplot.scatter([new_x, new_x], [min_y, max_y], color='tab:purple', alpha=0.75)
    pyplot.plot([new_x, new_x], [min_y, max_y], color='tab:purple', alpha=0.75)
    pyplot.annotate('salary range', (new_x, max_y), ha='right', va='bottom', color='tab:purple')

new_data = [(x, min(y, y+3*(y-fn(x)))) for x, y in data]

# New hire
with plot(7, 'Distribution of salaries at MegaHyperCo'):
    pyplot.scatter([x for x, y in new_data], [y for x, y in new_data], alpha=0.75, s=50, color='tab:blue')

cns_adjs = []

# Salary calibration to consistency
with plot(8, 'Idealized salary calibration to bring the salaries to consistency at MegaHyperCo'):
    pyplot.scatter([x for x, y in new_data], [y for x, y in new_data], alpha=0.75, s=50, color='tab:blue')
    adjusted_data = []
    for x, y in new_data:
        min_y = max([y2 for x2, y2 in new_data if x2 <= x])
        cns_adjs.append(max(y, min_y) - y)
        if min_y > y:
            pyplot.annotate(None, (x, y), (x, min_y), arrowprops=dict(arrowstyle='<|-', color='tab:red', shrinkA=0, shrinkB=0))
            adjusted_data.append((x, min_y))
    pyplot.scatter([x for x, y in adjusted_data], [y for x, y in adjusted_data], alpha=0.5, s=50, color='tab:cyan')

mkt_adjs = []

# Salary calibration to market/replacement
with plot(9, 'Calibrating salaries against market rate and replacement cost is at MegaHyperCo'):
    pyplot.scatter([x for x, y in new_data], [y for x, y in new_data], alpha=0.75, s=50, color='tab:blue')
    pyplot.fill_between(xs, fn_lo1(xs), fn_hi1(xs), linewidth=0, alpha=0.3, color='tab:blue')
    pyplot.annotate('market salary\nrange', (m, (fn_lo1(m) + fn_hi1(m))/2), ha='left', va='center', color='tab:blue')
    for x, y in new_data:
        mkt_adjs.append(max(fn_lo1(x), y) - y)
        if y < fn_lo1(x):
            pyplot.annotate(None, (x, y), (x, fn_lo1(x)), arrowprops=dict(arrowstyle='<|-', color='tab:red', shrinkA=0, shrinkB=0))
            pyplot.scatter([x], [fn_lo1(x)], alpha=0.5, s=50, color='tab:cyan')


# Bar chart of raises
order = sorted(range(len(cns_adjs)), key=lambda i: (cns_adjs[i] + mkt_adjs[i])/2, reverse=True)
cns_adjs = [cns_adjs[i] for i in order]
mkt_adjs = [mkt_adjs[i] for i in order]
width = 0.35  # the width of the bars
fig, ax = pyplot.subplots(figsize=(6, 3))
x = numpy.arange(len(cns_adjs))
rects1 = ax.bar(x - width/2, cns_adjs, width, label='Consistency-based adjustment', color='tab:pink')
rects2 = ax.bar(x + width/2, mkt_adjs, width, label='Market-based adjustment', color='tab:cyan')
ax.set_ylabel('Raise')
ax.set_xlabel('Employee (sorted by raise)')
ax.set_xticks(x + 1)
ax.set_yticks([])
ax.legend()
fig.tight_layout()
pyplot.savefig('figure-10.png', dpi=600)
