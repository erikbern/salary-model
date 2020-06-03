import math, matplotlib
from matplotlib import pyplot

def f(t):
    if t > 1:  # post-ipo
        return 1 - 0.25 * math.exp(-2*(t-1))
    else:
        return 5 * math.exp(-5*t) + \
            2.5 * math.exp(6*(t-1))


ts = [i/1000 for i in range(0, 1750)]
ys = [f(t) for t in ts]

pyplot.figure(figsize=(6, 3))
pyplot.plot(ts, ys)
pyplot.ylim([0, 5])
pyplot.xlim([0, 1.5])
#pyplot.xticks([0, 0.25, 0.5, 0.75, 1.0, 1.25],
#              ['Seed', 'Series A', 'Series B', '...', 'IPO', '...'],
#              fontsize='small')
#pyplot.yticks([0, 1, 2, 3, 4, 5],
#              ['0%', '100%', '200%', '300%', '400%', '500%'],
#              fontsize='small')
pyplot.xticks([])
pyplot.yticks([])
for dir in ['top', 'left', 'bottom', 'right']:
    pyplot.gca().spines[dir].set_visible(False)
pyplot.axhline(1, color='tab:purple', alpha=0.5)
pyplot.annotate('100% of "nominal" value', (0, 1), ha='left', va='bottom', color='tab:purple')
for x, stage in [(0, 'Seed'), (0.25, 'Series A'), (0.5, 'Series B'), (1.0, 'IPO')]:
    pyplot.annotate(stage, (x, 3), ha='center', va='bottom')
pyplot.figtext(0.5, 0.01, 'Figure 8: Employee perception of equity compensation', ha='center', style='italic') #, fontsize='small')
pyplot.tight_layout()
pyplot.savefig('equity-value.png', dpi=300)
