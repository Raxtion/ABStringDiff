import tkinter
from tkinter import ttk
import function_class


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('pyABDifference')
        self.init_widgets()

    def init_widgets(self):
        self.TOP = ttk.Frame(self.root)
        self.input_A = function_class.LabEntFrame(self.TOP, 'input_A')
        self.input_A.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.input_B = function_class.LabEntFrame(self.TOP, 'input_B')
        self.input_B.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.output = function_class.LabEntFrame(self.TOP, 'result')
        self.output.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.TOP.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)

        self.resultF = function_class.ResultBtnFrame(self.root)
        self.resultF.BtnFrame.interbtn.configure(command=self.Intersect)
        self.resultF.BtnFrame.diffbtn.configure(command=self.Difference)
        self.resultF.BtnFrame.repbtn.configure(command=self.Repeat)
        self.resultF.BtnFrame.resetbtn.configure(command=self.Reset)
        self.resultF.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES, pady=2)

        #self.progressBar = ttk.Progressbar(self.root, orient=tkinter.HORIZONTAL, mode='indeterminate', maximum='10')
        #self.progressBar.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH)

    def Intersect(self):
        #thread = function_class.Thread(0.1, self.UpdateProgressBar)
        try:
            #self.progressBar.start()
            #thread.start()

            Result = function_class.DataProcessing(self)
            self.resultF.text['state'] = 'normal'
            self.resultF.text.insert(tkinter.END, '\n'+Result[0]+'\n\n>>>')
            self.resultF.text.see(tkinter.END)
            self.resultF.text['state'] = 'disable'

            self.output.text.delete(1.0, tkinter.END)
            self.output.text.insert(tkinter.END, '\n'.join([x for x in Result[1] if x != '']))

            #thread.thread_Event.set()
            #self.progressBar.stop()

        except:
            self.resultF.text['state'] = 'normal'
            self.resultF.text.insert(tkinter.END, '\n'+'Intersect Error.'+'\n\n>>>')
            self.resultF.text.see(tkinter.END)
            self.resultF.text['state'] = 'disable'
            #thread.thread_Event.set()
            #self.progressBar.stop()

    def Difference(self):
        #thread = function_class.Thread(0.1, self.UpdateProgressBar)
        try:
            #self.progressBar.start()
            #thread.start()

            Result = function_class.DataProcessing(self)
            self.resultF.text['state'] = 'normal'
            self.resultF.text.insert(tkinter.END, '\n'+Result[0]+'\n\n>>>')
            self.resultF.text.see(tkinter.END)
            self.resultF.text['state'] = 'disable'

            self.output.text.delete(1.0, tkinter.END)
            self.output.text.insert(tkinter.END, 'diff_in_A: \n'+'\n'.join([x for x in Result[2] if x != ''])+'\n\n')
            self.output.text.insert(tkinter.END, 'diff_in_B: \n'+'\n'.join([x for x in Result[3] if x != ''])+'\n')

            #thread.thread_Event.set()
            #self.progressBar.stop()

        except:
            self.resultF.text['state'] = 'normal'
            self.resultF.text.insert(tkinter.END, '\n'+'Difference Error.'+'\n\n>>>')
            self.resultF.text.see(tkinter.END)
            self.resultF.text['state'] = 'disable'
            #thread.thread_Event.set()
            #self.progressBar.stop()

    def Repeat(self):
        try:
            Result = function_class.DataProcessing(self)
            self.resultF.text['state'] = 'normal'
            self.resultF.text.insert(tkinter.END, '\n'+Result[0]+'\n\n>>>')
            self.resultF.text.see(tkinter.END)
            self.resultF.text['state'] = 'disable'

            self.output.text.delete(1.0, tkinter.END)
            self.output.text.insert(tkinter.END, 'repeat_in_A: \n'+'\n'.join([x for x in set(Result[4]) if x != ''])+'\n\n')
            self.output.text.insert(tkinter.END, 'repeat_in_B: \n'+'\n'.join([x for x in set(Result[5]) if x != ''])+'\n')
        except:
            self.resultF.text['state'] = 'normal'
            self.resultF.text.insert(tkinter.END, '\n'+'Repeat Error.'+'\n\n>>>')
            self.resultF.text.see(tkinter.END)
            self.resultF.text['state'] = 'disable'

    def Reset(self):
        self.input_A.label.configure(text='input_A')
        self.input_B.label.configure(text='input_B')
        self.output.label.configure(text='result')
        self.input_A.text.delete(1.0, tkinter.END)
        self.input_B.text.delete(1.0, tkinter.END)
        self.output.text.delete(1.0, tkinter.END)

        self.resultF.text['state'] = 'normal'
        self.resultF.text.delete(1.0, tkinter.END)
        self.resultF.text.insert(tkinter.END, '>>>')
        self.resultF.text['state'] = 'disable'

    '''
    def UpdateProgressBar(self):
        i = str(int(function_class.time.time()))[-1:]
        self.progressBar['value'] = i
        self.progressBar.update()
    '''


if __name__ == '__main__':
    mainpanel = tkinter.Tk()
    Application(mainpanel)
    mainpanel.minsize(width=650, height=550)
    mainpanel.iconbitmap('CCC.ico')
    mainpanel.mainloop()