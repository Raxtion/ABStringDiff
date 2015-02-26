import tkinter
from tkinter import ttk
import threading
import time
import ctypes
import pickle
import os


class LabEntFrame(ttk.Frame):
    def __init__(self, parent, labelname):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.labelname = labelname
        self.init_frame()

    def init_frame(self):
        TOP = ttk.Frame(self, relief=tkinter.GROOVE)
        self.label = ttk.Label(TOP, text=self.labelname)
        self.label.pack(pady=2)
        TOP.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.text = tkinter.Text(self, width=30, height=20)
        self.text.bind('<Control-Key-a>', self.SelectAll)
        #self.text.bind('<ButtonRelease-1>', self.ShowNum) 當滑鼠點進去放開時就觸發
        #self.text.bind('<Leave>', self.ShowNum) 當滑鼠移開版面的區域時就觸發
        #self.text.bind('<FocusIn>', self.ShowNum) 當滑鼠點進去時就觸發
        #self.text.bind('<Enter>', self.ShowNum) 當滑鼠移入時就觸發
        #self.text.bind('<Configure>', self.ShowNum) 當主畫面被改變大小時就觸發
        self.text.bind('<FocusOut>', self.ShowNum) #當滑鼠點出去時就觸發
        self.text.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)

    def SelectAll(self, event):
        self.text.tag_add(tkinter.SEL, '1.0', tkinter.END)
        self.text.mark_set(tkinter.INSERT, '1.0')
        self.text.see(tkinter.INSERT)
        return 'break'

    def ShowNum(self, event):
        datalist = self.text.get('1.0', tkinter.END)[:-1].split('\n')
        self.label['text'] = self.labelname+'('+str(len(datalist))+')'
        self.label.update()
        return 'break'


class ResultBtnFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_frame()

    def init_frame(self):
        self.text = tkinter.Text(self, width=60, height=10)
        self.text.insert(tkinter.END, '>>>')
        self.text.configure(state='disable')
        self.text.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.BtnFrame = self.BtnFrame(self)
        self.BtnFrame.pack(fill=tkinter.BOTH)

    class BtnFrame(ttk.Frame):
        def __init__(self, parent):
            ttk.Frame.__init__(self, parent, relief=tkinter.GROOVE)
            self.parent = parent
            self.init_frame()

        def init_frame(self):
            self.interbtn = ttk.Button(self, text='Intersect')
            self.interbtn.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, pady=2)
            self.diffbtn = ttk.Button(self, text='Difference')
            self.diffbtn.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, pady=2)
            self.repbtn = ttk.Button(self, text='Repeat')
            self.repbtn.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, pady=2)
            self.resetbtn = ttk.Button(self, text='Reset')
            self.resetbtn.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, pady=2)


def DataProcessing(root):
    A_diff_set, B_diff_set, Result = None, None, ""
    A_list = root.input_A.text.get(1.0, tkinter.END)[:-1].split('\n')
    B_list = root.input_B.text.get(1.0, tkinter.END)[:-1].split('\n')
    A_repeat_list = [x for x in A_list if A_list.count(x) > 1]
    B_repeat_list = [x for x in B_list if B_list.count(x) > 1]
    A_set = set(A_list)
    B_set = set(B_list)
    S_set = A_set & B_set

    if A_set == B_set and len(A_set) == set(B_set):
        Result = 'A == B'
    else:
        A_diff_set = set(A_set-S_set)
        B_diff_set = set(B_set-S_set)
        Result = '\n'.join(['A_repeat_list :',
                            str(len([x for x in A_list if x not in A_repeat_list]))+' + '+str(tuple(A_repeat_list)).replace(' ', '')+' '+'('+str(len(A_repeat_list))+')',
                            'B_repeat_list :',
                            str(len([x for x in B_list if x not in B_repeat_list]))+' + '+str(tuple(B_repeat_list)).replace(' ', '')+' '+'('+str(len(B_repeat_list))+')',
                            "",
                            'A_diff_list :',
                            str(len(S_set))+' + '+str(tuple(A_diff_set)).replace(' ', '')+' '+'('+str(len(A_diff_set))+')',
                            'B_diff_list :',
                            str(len(S_set))+' + '+str(tuple(B_diff_set)).replace(' ', '')+' '+'('+str(len(B_diff_set))+')'])

    Result += '\nend processing'
    return Result, S_set, A_diff_set, B_diff_set, A_repeat_list, B_repeat_list


def DataProcessingUsingCDLL(root):

    A_string = root.input_A.text.get(1.0, tkinter.END)[:-1]
    Af = open('A.data.txt', 'w')
    Af.write(A_string+'\n')
    Af.close()

    B_string = root.input_B.text.get(1.0, tkinter.END)[:-1]
    Bf = open('B.data.txt', 'w')
    Bf.write(B_string+'\n')
    Bf.close()

    cdll = ctypes.cdll.LoadLibrary(r'C:\X.DLL')
    cdll.ProcessingStart()
    f = open('temp.text','r')
    S = f.read()
    #do something S should be treat because S is one String not a tuple which ready to use

    '''
    #open with pickle
    f = open('temp.pickle', 'rb')
    S = pickle.load(f)
    f.close()
    '''

    try:
        os.remove(r'temp.pickle')
        os.remove(r'A.data.txt')
        os.remove(r'B.data.txt')
    except:
        pass

    return S


class Thread(threading.Thread):
    def __init__(self, interval, func, *args):
        threading.Thread.__init__(self)
        self.interval = interval
        self.func = func
        self.interval = interval
        self.args = args
        self.thread_Event = threading.Event()

    def run(self):
        if self.interval is None:
            if len(self.args) == 0:
                self.func()
            else:
                self.func(self.args)
        else:
            if len(self.args) == 0:
                while not self.thread_Event.is_set():
                    self.func()
                    time.sleep(self.interval)
            else:
                while not self.thread_Event.is_set():
                    self.func(self.args)
                    time.sleep(self.interval)


if __name__ == '__main__':
    class Application:
        def __init__(self, root):
            self.root = root
            self.root.title('TESTApp')
            self.init_widgets()

        def init_widgets(self):
            #--------------------------------------------------------------------------------
            #TEST LabEntFrame()
            self.A = LabEntFrame(self.root, 'Input_A')
            self.A.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
            self.B = LabEntFrame(self.root, 'Input_B')
            self.B.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
            self.B.text.insert(tkinter.END, '>>>')

            print(self.B.text.get(1.0, tkinter.END))

            '''
            #--------------------------------------------------------------------------------
            #TEST ResultBtnFrame()
            self.Text = ResultBtnFrame(self.root)
            self.Text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
            '''

    mainpanel = tkinter.Tk()
    Application(mainpanel)
    #mainpanel.resizable(width='False', height='True')
    mainpanel.mainloop()