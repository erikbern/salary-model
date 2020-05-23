import contextlib, math, matplotlib, numpy, random
from matplotlib import pyplot

data = [(300, 250), (325, 293), (437, 325), (469, 330), (855, 431), (880, 463), (1032, 463), (1091, 520), (1130, 631), (1332, 868), (1622, 1071), (1650, 1177), (1676, 1285), (1701, 1388), (1783, 1401), (1824, 1501), (1874, 1564), (2100, 1637), (2310, 1675), (2446, 1781)]
m = 2500

@contextlib.contextmanager
def plot(fignr, title):
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
    pyplot.figtext(0.5, 0.02, 'Figure %d: %s' % (fignr, title), ha='center', style='italic', fontsize='small')
    pyplot.tight_layout()
    pyplot.savefig('figure-%d.png' % fignr, dpi=600)

# Base scatter
with plot(1, 'Distribution of salaries at BananaLovers'):
    pyplot.scatter([x for x, y in data], [y for x, y in data], alpha=0.75, s=50, color='tab:blue')

# New hire
with plot(2, 'New potential candidate at BananaLovers'):
    pyplot.scatter([x for x, y in data], [y for x, y in data], alpha=0.75, s=50, color='tab:blue')
    x, y = 750, 600
    pyplot.scatter([x], [y], color='tab:green', alpha=0.75)
    pyplot.annotate('candidate', (x, y), ha='right', va='bottom', color='tab:green')
    pyplot.plot([x, x], [y, x], color='tab:olive')
    pyplot.annotate('value surplus', (x, x), ha='left', va='bottom', color='tab:olive')

# New hire inconsistencies
with plot(3, 'Inconsistency cost of hiring the new candidate'):
    pyplot.scatter([x for x, y in data], [y for x, y in data], alpha=0.75, s=50, color='tab:blue')
    pyplot.scatter([x], [y], color='tab:green', alpha=0.75)
    pyplot.plot([x, m], [y, y], color='black', linestyle=':')
    xs, ys = [], []
    for x2, y2 in data:
        if x2 > x and y2 < y:
            pyplot.annotate(None, (x2, y2), (x2, y), arrowprops=dict(arrowstyle='<|-', color='tab:red', shrinkA=0, shrinkB=0))
            xs.append(x2)
            ys.append(y2)
    pyplot.annotate('inconsistencies', (numpy.median(xs), numpy.min(ys)), ha='center', va='bottom', color='tab:red')

# New hire range
with plot(4, 'Consistency-based salary range for the new hire'):
    pyplot.scatter([x for x, y in data], [y for x, y in data], alpha=0.75, s=50, color='tab:blue')
    min_y = max(y2 for x2, y2 in data if x2 < x)
    max_y = min(y2 for x2, y2 in data if x2 > x)
    pyplot.scatter([x, x], [min_y, max_y], color='tab:green', alpha=0.75)
    pyplot.plot([x, x], [min_y, max_y], color='tab:green', alpha=0.75)
    pyplot.annotate('salary range', (x, (min_y+max_y)/2), ha='left', va='center', color='tab:green')

new_data = [(400, 300), (325, 293), (537, 425), (369, 430), (855, 431), (780, 563), (1032, 463), (1091, 640), (1230, 531), (1332, 668), (1422, 771), (1650, 677), (1676, 785), (1701, 788), (1803, 1101), (1924, 975), (2000, 1264), (2200, 1337), (2310, 1775), (2446, 1581)]

# Salary calibration
with plot(5, 'Idealized salary calibration to bring the distribution back to consistency'):
    pyplot.scatter([x for x, y in new_data], [y for x, y in new_data], alpha=0.75, s=50, color='tab:blue')
    adjusted_data = []
    for x, y in new_data:
        min_y = max([y2 for x2, y2 in new_data if x2 <= x])
        if min_y > y:
            pyplot.annotate(None, (x, y), (x, min_y), arrowprops=dict(arrowstyle='<|-', color='tab:red', shrinkA=0, shrinkB=0))
            adjusted_data.append((x, min_y))
    pyplot.scatter([x for x, y in adjusted_data], [y for x, y in adjusted_data], alpha=0.5, s=50, color='tab:cyan')
