import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import messagebox as mbox
import os
import shutil


class Main(tk.Frame):

    def __init__(self, root):
        super(Main, self).__init__(root)
        self.start()

    def start(self):
        self.lbl = tk.Label(root,
                            text='Обновлённый файл - файл, '
                                 'на который надо заменить файлы в рабочей папке\n'
                                 'Рабочая папка - папка в которой заменяются файлы',
                            font=('IBM Plex', 10))
        self.lbl.place(x=50, y=50)
        self.work_dir = tk.Button(root, text='Рабочая папка', font=('IBM Plex', 14), command=self.work_dir_choose)
        self.work_dir.place(x=50, y=220)
        self.file = tk.Button(root, text='Обновлённый файл', font=('IBM Plex', 14), command=self.file_choose)
        self.file.place(x=50, y=120)
        self.start_button = tk.Button(root, text='Заменить', font=('IBM Plex', 14), command=self.progress)
        self.start_button.place(x=50, y=320)
        self.info_button = tk.Button(root, text='i', font=('IBM Plex', 14), command=self.info)
        self.info_button.place(x=575, y=410)

    def info(self):
        self.infowin = tk.Toplevel()
        self.infowin.overrideredirect(False)
        self.infowin.geometry('400x200')
        self.infowin.geometry(f'+{root.winfo_screenwidth() // 2 - 200}+{root.winfo_screenheight() // 2 - 100}')
        self.infowin.title('Информация')
        self.infolbl = tk.Label(self.infowin, text="Разработанно: Соколов А.С.\n"
                                                   "По всем вопросам обращайтесь ...\n"  # надо что-то написать, но я не знаю что
                                                   "There should be an instruction, but, well, sorry\n"
                                                   "This is a test branch, I'm testing rn",
                                font=('IBM Plex', 10))
        self.infolbl.place(x=50, y=50)

    def work_dir_choose(self):
        self.w_d = tk.filedialog.askdirectory()
        self.lbl_w_d = tk.Label(root, text=f'Вы выбрали {self.w_d}')
        self.lbl_w_d.place(x=50, y=200)

    def file_choose(self):
        self.f = tk.filedialog.askopenfilename()
        self.lbl_f = tk.Label(root, text=f'Вы выбрали {self.f}')
        self.lbl_f.place(x=50, y=100)

    def progress(self):
        self.count = 0
        file_name = ''
        self.s = -1
        while self.f[self.s] != '/':
            file_name += self.f[self.s]
            self.s -= 1
        self.file_name = file_name[::-1]

        full_dict_list = os.walk(self.w_d)

        self.quant = 0

        for i in full_dict_list:
            self.quant += 1

        self.s1 = 0
        self.s = tk.IntVar()
        self.s.set(self.s1)
        self.prog = tk.Toplevel()
        self.prog.overrideredirect(False)
        self.prog.geometry('400x100')
        self.prog.geometry(f'+{root.winfo_screenwidth() // 2 - 200}+{root.winfo_screenheight() // 2 - 100}')
        self.prog.title('Прогресс')
        progressbar = ttk.Progressbar(self.prog, orient="horizontal", length=388, maximum=self.quant, variable=self.s)
        progressbar.place(x=6, y=6)
        self.replace()

    def replace(self):
        full_dict_list = os.walk(self.w_d)

        for i in full_dict_list:
            self.s1 += 1
            self.s.set(self.s1)
            self.prog.update()
            path = os.path.join(i[0], self.file_name)
            if os.path.isfile(path):
                os.remove(path)
                copy_file = shutil.copy2(self.f, i[0])
                self.count += 1

        self.prog.destroy()

        mbox.showinfo('Информация', f'Процесс завершён, было замененно {self.count} файлов')

        destroy_obj = [self.lbl_w_d, self.lbl_f]

        for obj_name in destroy_obj:
            obj_name.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    w = root.winfo_screenwidth()  # ширина экрана
    h = root.winfo_screenheight()  # высота экрана
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 300  # смещение от середины
    h = h - 225
    root.geometry('600x450+{}+{}'.format(w, h))
    root.title("File Swapper")
    root.resizable(False, False)
    root["bg"] = "#fff"
    app = Main(root)
    app.pack()

    root.mainloop()
