from tkinter import *
from tkinter import ttk
from imageProcess import ImageProcess
import cv2
from tkinter import filedialog, messagebox
import os
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from batch import Batch
from mytreeview import MyTreeview
from mannually import Mannually
import cv2


class Main_RGB(Frame):
    def __init__(self, master):
        super().__init__(master)

        filelist = Frame(self)
        Button(filelist, text = 'import images', command = self._on_import).pack(pady = (5,5))
        #treeview
        self.treeview = MyTreeview(filelist)
        self.treeview.pack(fill = 'both',expand= True)

        #panel
        para_p = Frame(self)
        b_f = Frame(para_p) # 1
        b_f.grid(row = 0, column = 0, sticky = 'nw', padx = (5,0), pady = (5,5))

        self.imageList = ttk.Combobox(b_f, values = ['original', 'highlighted circle', 'rectangle', 'only wafer', 'RGB figures'])
        self.imageList.current(0)
        self.imageList.bind("<<ComboboxSelected>>", self.callbackFunc)

        self.imageList.grid(row = 0, column = 0, sticky = 'w', padx = (5,5))
        self.b_save = Button(b_f, text = 'save RGB to .csv', command = self._on_save)
        self.b_save.grid(row = 0, column = 1, sticky = 'w', padx = (5,5))
        Button(b_f, text = 'save current image', command = self._on_save_img).grid(row = 0, column = 2, sticky = 'w', padx = (5,5))
        self.saveInf = Label(b_f, fg = 'green')
        self.saveInf.grid(row = 0, column = 3, sticky = 'e')
        Button(b_f, bg = 'lightblue', width = 15, text = 'batch', command = self.on_batch).grid(row = 0, column = 4, sticky = 'e', padx = (80,0))




        self.columnconfigure(1, weight = 1)
        self.rowconfigure(1, weight = 1)

        self.treeview.treeview.column('#0', width = 160,  stretch = True)
        self.treeview.treeview.bind('<ButtonRelease-1>', self._onselect)
        self.treeview.treeview.bind("<Double-1>", self.OnDoubleClick)
        self.treeview.treeview.bind('<KeyRelease-Up>', self._onselect)
        self.treeview.treeview.bind('<KeyRelease-Down>', self._onselect)

        # for i in range(1,8):
        #     self.treeview.treeview.insert('','end',text = f'{i}.jpg', tags = {i})

        self.dirname = ''


    def _on_save_img(self):
        path = filedialog.asksaveasfilename()
        if path:
            try:
                self.fig.savefig(path+'.png', format = 'png', transparent=True, dpi = 800)

            except:
                messagebox.showinfo(message =f'save failed')
                return
            messagebox.showinfo(message =f'image saved!')

    def _on_save(self):
        path = filedialog.asksaveasfilename()
        item = self.treeview.treeview.focus()
        imageName = self.treeview.treeview.item(item, 'text')
        if path:
            try:
                self.myprocess.save_rgb_data(path)
            except: return
            messagebox.showinfo(message =f'{imageName} saved!')

    def callbackFunc(self, event):
        self._onselect(event)

    def _on_import(self):
        filenames =  filedialog.askopenfilenames(title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if filenames:
            self.dirname = os.path.dirname(filenames[0])
            # self.pathInf.config(text = self.dirname)
            self.treeview.treeview.delete(*self.treeview.treeview.get_children())
            self.treeview.treeview.heading('#0', text = f'image names ({len(filenames)})', anchor= 'w')
            for file in filenames:
                self.treeview.treeview.insert('', 'end', text = os.path.basename(file), tags = file)


    def _onselect(self, event):
        item = self.treeview.treeview.focus()

        self.imageName = self.treeview.treeview.item(item, 'text')
        self.myprocess = ImageProcess(os.path.join(self.dirname,self.imageName))

        if self.myprocess.isCircle():
            self.imageList.grid()
            self.b_save.grid()
            self.ax.clear()
            self.ax.axis('off')
            if self.imageList.get() == 'original':
                self.image = self.myprocess.get_ori()
            elif self.imageList.get() == 'highlighted circle':
                self.image = self.myprocess.get_circle()
            elif self.imageList.get() == 'rectangle':
                self.image = self.myprocess.get_crop()
            elif self.imageList.get() == 'only wafer':
                self.image = self.myprocess.get_wafer()
            elif self.imageList.get() == 'RGB figures':
                self.image = self.myprocess.get_RGBI()

                w,h = max(self.ax.get_xlim()), max(self.ax.get_ylim())
                pos = [[0,h/2,w/2*0.8,h/2*0.8],[w/2,h/2,w/2*0.8,h/2*0.8],[0,0,w/2*0.8,h/2*0.8],[w/2,0,w/2*0.8,h/2*0.8]]
                title = ['R', 'G', 'B', 'Intensity']
                cmap = ['Reds', 'Greens', 'Blues', 'gray']
                for i in range(4):
                    inset = self.ax.inset_axes(pos[i], transform = self.ax.transData)
                    inset.set_title(title[i])
                    inset.imshow(self.image[0], cmap = cmap[i])
                    inset.axis('off')
                    self.canvas.draw()
                return
        else:
            self.imageList.grid_remove()
            self.b_save.grid_remove()
            self.image = self.myprocess.get_ori() # just show original

        self.ax.imshow(self.image)
        self.canvas.draw()

class NavigationToolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    # toolitems = [t for t in NavigationToolbar2GTKAgg.toolitems if
    #              t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
    toolitems=[]




def main():
    root = Tk()
    root.title('Exact_rgb')
    app = Main_RGB(root)

    app.pack(fill = 'both', expand = True)

    root.mainloop()


if __name__=='__main__':
    main()






