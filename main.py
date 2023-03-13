# Create an app that will display a window in which the user can select a folder of images, a logo image, and a destination folder.
# The app will then add the logo image to each image and save it in the destination folder.

import os

import tkinter as tk
from tkinter import filedialog
from PIL import Image
from tkinter import ttk


deepblue = '#124165'


root = tk.Tk(screenName='Log(O)', baseName='Log(O)', className='Log(O)', useTk=1)
root.minsize(500, 150)
root.iconbitmap('home_icon.ico')
root.configure(background=deepblue)


def getFolder():
    got = filedialog.askdirectory()
    if got != '': 
        utils['init_folder'] = got
        if len(frame.grid_slaves(row=0, column=2)) > 0 :
            frame.grid_slaves(row=0, column=2)[0].destroy()
        path = utils['init_folder'].split('/')
        ttk.Label(frame, text='~/' + path[-2] + '/' + path[-1], background=deepblue, foreground='white').grid(row=0, column=2, sticky='w')
    
    
def getLogo():
    #delete the previous label
    
    got = filedialog.askopenfilename()
    if got != '': 
        utils['logo'] = got
        if len(frame.grid_slaves(row=1, column=2)) > 0 :
            frame.grid_slaves(row=1, column=2)[0].destroy()
        path = utils['logo'].split('/')
        tk.Label(frame, text='~/' + path[-2] + '/' + path[-1], background=deepblue, foreground='white').grid(row=1, column=2, sticky='w')
        
        
        

def getDestFolder():
    got = filedialog.askdirectory()
    if got != '':
        utils['dest_folder'] = got
        if len(frame.grid_slaves(row=2, column=2)) > 0 :
            frame.grid_slaves(row=2, column=2)[0].destroy()
        path = utils['dest_folder'].split('/')
        ttk.Label(frame, text='~/' + path[-2] + '/' + path[-1], background=deepblue, foreground='white').grid(row=2, column=2, sticky='w')
    
    
def pasteLogo():
    label = ttk.Label(frame, background=deepblue, font='bold')
    label.grid(row=3, column=2, sticky='w', pady=5)
    
    if (utils['init_folder'] == '' or utils['logo'] == '' or utils['dest_folder'] == ''):
        label.config(text='Please select all the fields!', foreground='red')
        root.after(5000, label.destroy)
        return
    label.config(text='Processing...', foreground='white')
    label.update()
    
    if not os.path.exists(utils['dest_folder']):
        os.makedirs(utils['dest_folder'])
    
    logo = Image.open(utils['logo']).convert('RGBA')
    index = 0
    Progressbar = ttk.Progressbar(frame, orient='horizontal', variable=index, mode='determinate', length = 200)
    Progressbar.grid(row=3, column=2, columnspan=2, sticky='w', pady=5)
    label.grid(row=3, column=0, sticky='w', pady=5, columnspan=2)
    length = len(os.listdir(utils['init_folder']))
    for file in os.listdir(utils['init_folder']):
        if (file == 'desktop.ini'):
            continue
        file_name = (file[:10] + '..' + file[-10:]) if len(file) > 22 else file
        label.config(text='[{}/{}]'.format(index+1, length) + ' ' + file_name, foreground='white', font='')
        img = Image.open(os.path.join(utils['init_folder'], file)).convert('RGBA')
        
        if choice.get() == 'Bottom Right':
            img.paste(logo, (img.width - logo.width, img.height - logo.height), logo)
        elif choice.get() == 'Bottom Left':
            img.paste(logo, (0, img.height - logo.height), logo)
        elif choice.get() == 'Bottom Center':
            img.paste(logo, (img.width//2 - logo.width//2, img.height - logo.height), logo)
        elif choice.get() == 'Top Right':
            img.paste(logo, (img.width - logo.width, 0), logo)
        elif choice.get() == 'Top Left':
            img.paste(logo, (0, 0), logo)
        elif choice.get() == 'Top Center':
            img.paste(logo, (img.width//2 - logo.width//2, 0), logo)
        
        img.save(os.path.join(utils['dest_folder'], file), format='PNG')
        index+=1
        Progressbar['value'] = 100 * index/length
        Progressbar.update()
    
    Progressbar.destroy()
    label.grid(row=3, column=2, sticky='w', pady=5)
    label.config(text='Done!', foreground='green', font='bold')
    if (utils['open_folder'].get()):
        os.startfile(utils['dest_folder'])
        
        
    

frame = tk.Frame(root, background=deepblue)
frame.grid()
frame.rowconfigure(3, minsize=50)
frame.columnconfigure(2, minsize=200)

utils = {'init_folder': '', 'logo': '', 'dest_folder': '', 'open_folder': tk.BooleanVar(frame)}

choice = ttk.Combobox(frame, values=['Top Left', 'Top Right', 'Top Center', 'Bottom Left', 'Bottom Right', 'Bottom Center'], state='readonly', width=15)
choice.grid(row=4, column=3, sticky='w', pady=10, padx=10)
choice.current(4)

tk.Checkbutton(frame, text='Open destination folder', variable=utils['open_folder'], onvalue=True, offvalue=False, background=deepblue, foreground='white', selectcolor='black').grid(row=4, column=0, sticky='w', pady=10, padx=10)

ttk.Label(frame, text='Folder of images to edit:', background=deepblue, foreground='white').grid(row=0, column=0, sticky='w', pady=10);     tk.Button(frame, text='Select Folder', command = getFolder, background='white', foreground='black').grid(row=0, column=1, sticky='w')
ttk.Label(frame, text='Logo image to append:', background=deepblue, foreground='white').grid(row=1, column=0, sticky='w', pady=10);         tk.Button(frame, text='Select Image', command = getLogo, background='white', foreground='black').grid(row=1, column=1, sticky='w')
ttk.Label(frame, text='Destination folder:', background=deepblue, foreground='white').grid(row=2, column=0, sticky='w', pady=10);           tk.Button(frame, text='Select Folder', command = getDestFolder, background='white', foreground='black').grid(row=2, column=1, sticky='w')

tk.Button(frame, text='Start', command=pasteLogo, background='white', foreground='black', padx=10).grid(row=4, column=2, sticky='e', pady=10)


root.mainloop()