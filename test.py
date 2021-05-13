import numpy as np
import matplotlib.pyplot as plt


t = np.linspace(0, 1)
y1 = 2 * np.sin(2*np.pi*t)
y2 = 4 * np.sin(2*np.pi*2*t)

fig, ax = plt.subplots()
ax.set_title('Click on legend line to toggle line on/off')
line1, = ax.plot(t, y1, lw=2, label='1 Hz')
line2, = ax.plot(t, y2, lw=2, label='2 Hz')
leg = ax.legend(fancybox=True, shadow=True)

lines = [line1, line2]
lined = {}  # Will map legend lines to original lines.
for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(True)  # Enable picking on the legend line.
    lined[legline] = origline


def on_pick(event):
    # On the pick event, find the original line corresponding to the legend
    # proxy line, and toggle its visibility.
    print(event)
    legline = event.artist
    origline = lined[legline]
    visible = not origline.get_visible()
    origline.set_visible(visible)
    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled.
    legline.set_alpha(1.0 if visible else 0.2)
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', on_pick)
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# X = np.random.rand(100, 1000)
# xs = np.mean(X, axis=1)
# ys = np.std(X, axis=1)

# fig, ax = plt.subplots()
# ax.set_title('click on point to plot time series')
# line, = ax.plot(xs, ys, 'o', picker=True, pickradius=5)  # 5 points tolerance


# def onpick(event):
#     print(event)
#     if event.artist != line:
#         return
#     n = len(event.ind)
#     if not n:
#         return
#     fig, axs = plt.subplots(n, squeeze=False)
#     for dataind, ax in zip(event.ind, axs.flat):
#         ax.plot(X[dataind])
#         ax.text(0.05, 0.9,
#                 f"$\\mu$={xs[dataind]:1.3f}\n$\\sigma$={ys[dataind]:1.3f}",
#                 transform=ax.transAxes, verticalalignment='top')
#         ax.set_ylim(-0.5, 1.5)
#     fig.show()
#     return True


# fig.canvas.mpl_connect('pick_event', onpick)
# plt.show()