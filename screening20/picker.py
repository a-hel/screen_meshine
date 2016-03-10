import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on points')

x = range(20)
y = range(20)
line, = ax.plot(x,y, 'o', picker=5, label=(4,7,9))  # 5 points tolerance


def onpick(event):
    global txt
    global plt
    thisline = event.artist
    lbl = thisline.get_label()
    print lbl
    txt = plt.text(event.xdata, event.ydata,'bello')
    #fig.canvas.draw()
    #self.text.figure.canvas.draw()

class InfoLabel(object):
    def __init__(self, fig):
        self.txt = None
        self.fig = fig

    def onclick(self, event):
        if event.artist!=line:  #check that you clicked on the object you wanted
            return True
        if not len(event.ind):  #check the index is valid
            return True
        ind = event.ind[0]
        lbl = event.artist.get_label()
        self.txt = plt.text(x[ind],y[ind], lbl, fontsize=8) #event.xdata, event.ydata,
        fig.canvas.draw()

    def offclick(self, event):
        if self.txt:
            self.txt.remove()
            fig.canvas.draw()
            self.txt = None

il = InfoLabel(fig)
fig.canvas.mpl_connect('pick_event', il.onclick)
fig.canvas.mpl_connect('button_release_event', il.offclick)

plt.show()

#txt = None
#fig.canvas.mpl_connect('pick_event', onpick)

#plt.show()
