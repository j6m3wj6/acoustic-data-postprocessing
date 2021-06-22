# Import packages
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as sty
print(plt.style.available)
# Use our custom style
plt.style.use('./src/lib/style.mplstyle')
# Create figure
fig = plt.figure()
# Add subplot to figure
ax = fig.add_subplot(111)
# Show empty plot
# plt.show()

with open('./src/lib/style.mplstyle', 'r', encoding='UTF-8', errors='ignore') as file:
    print(file.readlines())
