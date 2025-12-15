from requests import get
from io import BytesIO
color="#252626"
from tkinter import BOTTOM, RAISED, RIGHT, Button, Label, Entry, Frame, LEFT, Tk, X
from PIL import Image
from time import sleep, perf_counter
from random import randint
from threading import Thread
from random import randint
from pathlib import Path
import os.path
from os import remove
from imghdr import what
import hashlib

class image_downloader:
    def __init__(self, master):
        self.master = master
        master.configure(bg=color)
        master.geometry('270x90+800+500')
        master.resizable(False, False)
        # Custom title bar so that its dark theme cause yes'nt
        master.overrideredirect(True)
        fake_title_bar = Frame(master, bg=color, relief=RAISED, bd=0.5)
        fake_title_bar.pack(expand=1, fill=X)
        fake_title_label = Label(fake_title_bar, text="\t          Pic downloader", bg=color, fg="white")
        fake_title_label.pack(side=LEFT)
            #Binding the title bar
        def move_app(e):
            master.geometry(f'+{e.x_root-130}+{e.y_root-10}')
        def minimize():
            master.update_idletasks()
            master.overrideredirect(False)
            master.state('iconic')
        def return_to_normal_state(e="temp"):
            # master.update_idletasks()
            # master.overrideredirect(True)
            # master.deiconify()
            print(perf_counter())
        def bar_check_loop():
            while True:
                if master.state() == 'iconic':
                    master.bind("<Map>", return_to_normal_state)
        fake_title_bar.bind('<B1-Motion>', move_app)
        fake_title_label.bind('<B1-Motion>', move_app)
        
        
            #Adding a close button
        fake_title_close_button = Button(fake_title_bar, text="X", bg=color, fg="white", command=master.quit).pack(side=RIGHT)

        # fake_title_min_button = Button(fake_title_bar, text="━", bg=color, fg="white", command=minimize).pack(side=RIGHT)
        #=====================================================
        master.title("Pic downloader")
        self.label = Label(master, text="Downloader by ~docea", bg=color, fg="white")
        self.label.pack()
        frame1 = Frame(master,bg=color)
        frame1.pack()
        Label(frame1,text='Query:', bg=color, fg="white").pack(side=LEFT)
        self.querysearch = Entry(frame1,width=10, bg=color, fg="white")
        self.querysearch.pack(side=LEFT)
        Label(frame1,text=' Amount:', bg=color, fg="white").pack(side=LEFT)
        self.number_of_images = Entry(frame1,width=4, bg=color, fg="white")
        self.number_of_images.pack()
        frame2 = Frame(master,bg=color)
        frame2.pack(side=BOTTOM)
        self.close_button = Button(frame2, text="Download!", command=self.download, bg=color, fg="white").pack(side=LEFT)
        Label(frame2,text='   ', bg=color).pack(side=LEFT)
        self.post_cleanup_button = Button(frame2, text="Clean dupes!", command=self.post_cleanup, bg=color, fg="white").pack(side=RIGHT)
    
    def hash_file(filename):
        """"This function returns the SHA-1 hash
        of the file passed into it"""

        # make a hash object
        h = hashlib.sha1()

        # open file for reading in binary mode
        with open(filename,'rb') as file:

            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                h.update(chunk)

        # return the hex representation of digest
        return h.hexdigest()
        
    def download(self):
        try:
            number = int(self.number_of_images.get())
        except:
            self.number_of_images.delete(0, 'end')
            self.number_of_images.insert(10, "Enter valid number")
            return
        try:
            tags=self.querysearch.get().replace('/', '%20')
        except:
            tags="ass%20boobs"
        url = f"https://example.com/index.php?page=dapi&s=post&q=index&json=1&limit=1&tags={tags}"
        self.master.withdraw()
        sizes=[]
        def thread_func():
            while True:
                try:
                    response = get(url).json()
                    img_url = response['post'][0]['file_url']
                    sleep(0.1)
                    data = BytesIO(get(img_url).content)
                    sleep(0.1)
                    img = Image.open(data)
                    print(f"{Path(__file__).parent.resolve()}\Image{randint(0,1000)}.png")
                    try:
                        img.save(f"{Path(__file__).parent.resolve()}\Image{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}.png")
                        break
                    except:
                        print("Error saving")        
                except:
                    print("Error, trying again")
        def main():
            # create threads
            threads = []
            for i in range(number):
                threads.append(Thread(target=thread_func, args=()))

            # start the threads
            for thread in threads:
                thread.start()

            # wait for the threads to complete
            for thread in threads:
                thread.join()


        if __name__ == "__main__":
            start_time = perf_counter()

            main()

            end_time = perf_counter()
            print(f'It took {end_time- start_time :0.2f} second(s) to complete.')
        self.master.deiconify()
        self.master.deiconify()
    def post_cleanup(self):
        directory = Path(__file__).parent.resolve()
        file_sizes = []
        def convert_bytes(size):
            """ Convert bytes to KB, or MB or GB"""
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return "%3.1f %s" % (size, x)
                size /= 1024.0
        dupes_found = 0
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                if what(f) == "png":
                    print(f)
                    f_size = os.path.getsize(f)
                    x = convert_bytes(f_size)
                    print('file size is', x)
                    if x in file_sizes:
                        print(f'file \"{filename}\" is most likely a duplicate')
                        dupes_found+=1
                        remove(f)
                        continue
                    file_sizes.append(x)
        if dupes_found == 0:
            print('There are no duplicate files')
        elif dupes_found == 1:
            print("One duplicate file was deleted")
        else:
            print(f'{dupes_found} duplicate files were deleted')
root = Tk()
downloader = image_downloader(root)

root.mainloop()
