import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np

class draggable_lines:
	def __init__(self, ax, kind, XorY):
		self.ax = ax
		self.c = ax.get_figure().canvas
		self.o = kind
		self.XorY = XorY

		if kind == "h":
			x = [-1, 1]
			y = [XorY, XorY]

		elif kind == "v":
			x = [XorY, XorY]
			y = [-1, 1]
		
		self.line = lines.Line2D(x, y, picker=5)
		self.ax.add_line(self.line)
		self.c.draw_idle()
		self.sid = self.c.mpl_connect('pick_event', self.clickonline)

	def clickonline(self, event):
		print(event, event.artist)
		if event.artist == self.line:
			print("line selected ", event.artist)
			self.follower = self.c.mpl_connect("motion_notify_event", self.followmouse)
			self.releaser = self.c.mpl_connect("button_press_event", self.releaseonclick)

	def followmouse(self, event):
		if self.o == "h":
			self.line.set_ydata([event.ydata, event.ydata])
		else:
			self.line.set_xdata([event.xdata, event.xdata])
		self.c.draw_idle()

	def releaseonclick(self, event):
		# if self.o == "h":
		#     self.XorY = self.line.get_ydata()[0]
		# else:
		#     self.XorY = self.line.get_xdata()[0]

		# print (self.XorY)

		self.c.mpl_disconnect(self.releaser)
		self.c.mpl_disconnect(self.follower)

# fig = plt.figure() 
fig = plt.figure(constrained_layout = True)
ax = fig.add_subplot(111)
# Vline = draggable_lines(ax, "h", 0.5)
# Tline = draggable_lines(ax, "v", 0.5)
# Tline2 = draggable_lines(ax, "v", 0.1)


ax2 = ax.twinx()
ax2.set_visible(True)

def handle_pick(event):
	print('pick')
	# print(event, event.artist, event.ind, event.mouseevent)
	# print(event.artist.contains(event.mouseevent))
	for line in ax.lines:
		bo, ind = line.contains(event.mouseevent)
		print(bo, ind)
		if (bo): print('ax', line)
	for line in ax2.lines:
		bo, ind = line.contains(event.mouseevent)
		print(bo, ind)
		if (bo): print('ax2', line)

	# print(event, event.mouse_event, event.ind)

def handle_click(event):
	print('click')
	# print(event, event.button, event.xdata, event.ydata)
	# ax.pick(event)
	# button_press_event: xy=(534, 549) xydata=(5.058870967741935, -1.0607142857142886) 
	#   button=1 dblclick=False inaxes=AxesSubplot(0.125,0.11;0.775x0.77) 
	#   MouseButton.LEFT 5.058870967741935 -1.0607142857142886
	for line in ax.lines:
		bo, ind = line.contains(event)
		print(bo, ind)
		if (bo): print('ax', line)
	for line in ax2.lines:
		bo, ind = line.contains(event)
		print(bo, ind)
		if (bo): print('ax2', line)

x = np.arange(10)
lines = []
for i in range(1, 3):
#     line, = ax.plot(x, i * x, label=r'$y={}x$'.format(i))
	ax.plot(x, i * x, picker=True, label=r'$y={}ss$'.format(i))
ax2.plot(x, (-1) * x, picker=True, label='y=-x')
	# lines.append(line)

# fig.canvas.mpl_connect("pick_event", handle_pick)
# fig.canvas.mpl_connect("button_press_event", handle_click)
box = ax.get_position()
print(box.x0, box.y0, box.width * 0.8, box.height)


# fig.subplots_adjust(right=0.8)
# fig.tight_layout()
leg = ax.legend(bbox_to_anchor=(1.1, 1 ), loc='upper left', borderaxespad=0)
box = leg.get_bbox_to_anchor()
print(box.size, type(box), box.get_points())

leg.set_in_layout(True)

print(fig.get_size_inches(), fig.get_figheight())

plt.show()