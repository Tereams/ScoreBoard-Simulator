import time
import copy

from tkinter import Tk, Frame, Label, Menu, NSEW, W
from tkinter.messagebox import showerror,showinfo
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askopenfilename


# 对象定义
# 此部分的数据结构是为了便于编程
# 指令对象
class Instr:
    def __init__(self, type, toshow, source, target):
        self.type = type
        self.toshow = toshow
        self.source = source
        self.target = target


# 此部分的数据结构是为了便于窗体展示
# 指令状态表行的结构
class InstrTabelRow:
    def __init__(self, toshow):
        self.toshow = toshow
        self.IS = ''
        self.RO = ''
        self.EX = ''
        self.WB = ''


# 功能部件状态表
class FuncTableRow:
    def __init__(self):
        self.id = -1
        self.Busy = False
        self.Op = ''
        self.Fi = ''
        self.Fj = ''
        self.Fk = ''
        self.Qj = -1
        self.Qk = -1
        self.Rj = False
        self.Rk = False


# 记分牌状态对象
class Scoreboard:
    def __init__(self):
        self.instr_state_table = [InstrTabelRow(['', ''])] * 3
        self.func_state_table = []
        self.result_reg_state_table = {'F0': -1, 'F2': -1, 'F4': -1, 'F6': -1, 'F8': -1, 'F10': -1, 'F12': -1,
                                       'F14': -1}

        int_func = FuncTableRow()
        mult_func1 = FuncTableRow()
        mult_func2 = FuncTableRow()
        add_func = FuncTableRow()
        divd_func = FuncTableRow()

        self.func_state_table.append(int_func)
        self.func_state_table.append(mult_func1)
        self.func_state_table.append(mult_func2)
        self.func_state_table.append(add_func)
        self.func_state_table.append(divd_func)


# 功能块对象
class RuntimeBlock:
    def __init__(self, func_row: FuncTableRow, instr_row_id, mytime):
        self.stage = 'IS'
        self.func_id = func_row.id
        self.instr_id = instr_row_id
        self.reg_target = func_row.Fi
        self.left_time = mytime


# 指令队列
instr_queue = []
# 运行结果存储区
ans_store = []
# 指令状态表
InstrStateList = []
# 全局记分牌对象
mainBoard = Scoreboard()
# 指令执行时间表
ex_time = {'LD': 1, 'SD': 1, 'ADDD': 2, 'SUBD': 2, 'MULTD': 10, 'DIVD': 40}
map_id_func = {-1: '', 0: '整数', 1: '乘法1', 2: '乘法2', 3: '加法', 4: '减法'}
# 当前的周期数
clock_now = 0
# 路径变量
err_path = 'err_log.txt'
ans_path = 'ans.txt'


# 窗体的初始化函数
def init_Window():
    pass


# 每个函数对应按钮绑定事件的函数
def readMips(file_path='./test.txt'):
    try:
        f1 = open(file_path, 'r', encoding='utf-8')
        err_list = []
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
        showerror(title='程序加载错误', message='Error: 没有找到文件或读取文件失败')
    else:
        instrs = f1.readlines()
        for l, instr in enumerate(instrs):
            try:
                toshow = []
                instr.strip()

                # 获取指令类型
                type, *operate = instr.split()
                toshow.append(type)

                operate = ''.join(operate)
                # 去掉注释的部分
                operate = operate.split(';')[0]
                toshow.append(operate)

                operates = operate.split(',')
                target = operates[:1]
                source = operates[1:]

                if type == 'LD':
                    source = operates[1].split('(')
                    if len(source) > 1:
                        source = [source[1].strip(')')]
                elif type == 'SD':
                    source = operates[0].split('(')
                    if len(source) > 1:
                        source = [source[1].strip(')')]
            except:
                err = "Line {}: Syntax Error: 指令存在语法错误".format(l+1)
                err_list.append(err)
            else:
                if type not in ['LD', 'SD', 'ADDD', 'SUBD', 'MULTD', 'DIVD']:
                    err = "Line {}: Unknown Instruction Type: 未知指令字错误".format(l+1)
                    err_list.append(err)
                else:
                    if type in ['LD', 'SD']:
                        if len(source) != 1 or len(target) != 1:
                            err = "Line {}: Wrong Operand: 操作数格式错误".format(l+1)
                            err_list.append(err)
                        else:
                            if target[0] not in ['F0','F2','F4','F6','F8','F10','F12','F14']:
                                err = "Line {}: Wrong Target Reg: 目的寄存器错误错误".format(l+1)
                                err_list.append(err)
                            else:
                                ins = Instr(type, toshow, source, target)
                                instr_queue.append(ins)

                    else:
                        if len(source) != 2 or len(target) != 1:
                            err = "Line {}: Wrong Operand: 操作数格式错误".format(l+1)
                            err_list.append(err)
                        else:
                            if target[0] not in ['F0', 'F2', 'F4', 'F6', 'F8', 'F10', 'F12', 'F14']:
                                err = "Line {}: Wrong Target Reg: 目的寄存器错误错误".format(l+1)
                                err_list.append(err)
                            else:
                                ins = Instr(type, toshow, source, target)
                                instr_queue.append(ins)
    finally:
        if len(err_list) != 0:
            showerror(title='程序错误', message='Error: 程序存在语法错误，详细信息请看err_log.txt')
            with open(err_path, 'a', encoding='utf-8') as f:
                for line in err_list:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n')
                    f.write(line + '\n')
            instr_queue.clear()
            return -1
        else:
            # 如果成功读取并且没有出现错误，就开始运行
            if (len(instr_queue) != 0):
                runScoreboard()
            f1.close()
            return 0



def runScoreboard():
    runtime_list = []
    clock = 0

    while True:

        accrodBoard = copy.deepcopy(mainBoard)

        result_reg = mainBoard.result_reg_state_table
        func_table = mainBoard.func_state_table

        result_reg1 = accrodBoard.result_reg_state_table
        func_table1 = accrodBoard.func_state_table

        clock += 1

        # 算法的执行，所有已经发射后的指令，在满足条件的情况下，向后进行一个周期
        for task in runtime_list:
            f_id = task.func_id
            i_id = task.instr_id

            # 这里是一处设计上的漏洞，虽然状态设置的是'IS'，但是'IS'实际上已经执行完毕
            if task.stage == 'IS':
                if func_table1[f_id].Rk and func_table1[f_id].Rj:
                    task.stage = 'RO'
                    func_row = func_table[f_id]
                    func_row.Rk = False
                    func_row.Rj = False
                    func_row.Qj = -1
                    func_row.Qk = -1
                    InstrStateList[i_id].RO = str(clock)

            # ex阶段
            elif task.stage == 'RO':
                task.stage = 'EX'
                task.left_time -= 1
                if task.left_time > 0:
                    InstrStateList[i_id].EX = 'ex'
                else:
                    task.stage = 'WB'
                    InstrStateList[i_id].EX = str(clock)

            # ex阶段的执行，需要判断是否进入WB
            elif task.stage == 'EX':
                # EX再执行一个周期
                task.left_time -= 1
                if task.left_time == 0:
                    task.stage = 'WB'
                    InstrStateList[i_id].EX = str(clock)

            # 这里的含义就发生变化了，状态是'WB',就是要执行WB部分的代码
            elif task.stage == 'WB':
                for f in func_table1:
                    if (func_table1[f_id].Fi == f.Fj and f.Rj) or \
                            (func_table1[f_id].Fi == f.Fk and f.Rk):
                        break
                else:
                    func_table[f_id].Busy = False
                    for f in func_table:
                        if f.Qj == f_id:
                            f.Rj = True
                        if f.Qk == f_id:
                            f.Rk = True
                    result_reg[func_table[f_id].Fi] = -1
                    InstrStateList[i_id].WB = str(clock)
                    func_table[f_id].Fi = ''
                    func_table[f_id].Fj = ''
                    func_table[f_id].Fk = ''
                    func_table[f_id].Op = ''
                    task.stage = 'Finished'

        r = []
        for t in runtime_list:
            if t.stage != 'Finished':
                r.append(t)
        runtime_list = r

        # 检查指令队列头部的指令是否可以发射
        if len(instr_queue) > 0:
            instr = instr_queue[0]

            # 确定使用哪一个部件
            if instr.type in ['LD', 'SD']:
                func_row = func_table[0]
                func_row.id = 0
                func_row1 = func_table1[0]
            elif instr.type in ['ADDD', 'SUBD']:
                func_row = func_table[3]
                func_row.id = 3
                func_row1 = func_table1[3]
            elif instr.type == 'DIVD':
                func_row = func_table[4]
                func_row.id = 4
                func_row1 = func_table1[4]
            else:
                func_row = func_table[1]
                func_row.id = 1
                func_row1 = func_table1[1]
                if func_table[1].Busy:
                    func_row = func_table[2]
                    func_row.id = 2
                    func_row1 = func_table1[2]

            if not func_row1.Busy and result_reg1[instr.target[0]] == -1:

                del instr_queue[0]

                instr_row = InstrTabelRow(instr.toshow)
                instr_row.IS = str(clock)
                InstrStateList.append(instr_row)

                func_row.Busy = True
                func_row.Op = instr.type

                func_row.Fi = instr.target[0]
                if instr.target[0] not in result_reg:
                    result_reg[instr.target[0]] = -1
                func_row.Fj = instr.source[0]
                if instr.source[0] not in result_reg:
                    result_reg[instr.source[0]] = -1
                if instr.type not in ['LD', 'SD']:
                    func_row.Fk = instr.source[1]
                    if instr.source[1] not in result_reg:
                        result_reg[instr.source[1]] = -1

                # 填写Qj/Qk/Rj/Rk
                if result_reg[func_row.Fj] != -1:
                    func_row.Qj = result_reg[func_row.Fj]
                else:
                    func_row.Rj = True
                if instr.type not in ['LD', 'SD']:
                    if result_reg[func_row.Fk] != -1:
                        func_row.Qk = result_reg[func_row.Fk]
                    else:
                        func_row.Rk = True
                else:
                    func_row.Rk = True
                result_reg[func_row.Fi] = func_row.id
                mytime = ex_time[instr.type]
                rtb = RuntimeBlock(func_row, len(InstrStateList) - 1, mytime)
                runtime_list.append(rtb)

        # 一个节省空间的设计，如果记分牌没有变化，就存保存其上一个周期的id
        # 上一个周期也没有变化就再上一个周期，以此类推
        mainBoard.instr_state_table = InstrStateList[-3:]
        tosave = copy.deepcopy(mainBoard)
        ans_store.append(tosave)

        if len(runtime_list) == 0 and len(instr_queue) == 0:
            print("Finished!")
            break


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createMenu()
        self.createWidget()
        self.loadtoGUI(mainBoard)

    def loadtoGUI(self, scoreboard: Scoreboard):
        for i, instr in enumerate(scoreboard.instr_state_table):
            self.instr_table[i][0]['text'] = instr.toshow[0] + '  ' + instr.toshow[1]
            self.instr_table[i][1]['text'] = instr.IS
            self.instr_table[i][2]['text'] = instr.RO
            self.instr_table[i][3]['text'] = instr.EX
            self.instr_table[i][4]['text'] = instr.WB

        for i, func in enumerate(scoreboard.func_state_table):
            self.func_table[i][1]['text'] = 'yes' if func.Busy else 'no'
            self.func_table[i][2]['text'] = func.Op
            self.func_table[i][3]['text'] = func.Fi
            self.func_table[i][4]['text'] = func.Fj
            self.func_table[i][5]['text'] = func.Fk
            self.func_table[i][6]['text'] = map_id_func[func.Qj]
            self.func_table[i][7]['text'] = map_id_func[func.Qk]
            self.func_table[i][8]['text'] = 'yes' if func.Rj else 'no'
            self.func_table[i][9]['text'] = 'yes' if func.Rk else 'no'

        for i, t in enumerate(['F0', 'F2', 'F4', 'F6', 'F8', 'F10', 'F12', 'F14']):
            self.result_table[i]['text'] = map_id_func[scoreboard.result_reg_state_table[t]]

    def loadfile(self):
        file_path = askopenfilename(title='请选择要载入的程序')
        if file_path!='':
            tag=readMips(file_path)
            if tag!=-1:
                self.filepath['text'] = file_path
                self.fileNow1['text'] = '共{}个周期，目前执行至第:'.format(len(ans_store))
                self.menuFile.entryconfig(2, state="normal")
                self.menuFile.entryconfig(3, state="normal")
                self.menuRun.entryconfig(1, state="normal")
                self.menuRun.entryconfig(3, state="normal")
                self.menuRun.entryconfig(4, state="normal")


    def stepForward_one(self):
        global clock_now
        if clock_now <= len(ans_store):
            clock_now += 1
            self.now['text'] = ' {}   周期'.format(clock_now)
            self.loadtoGUI(ans_store[clock_now - 1])
        if clock_now > 1:
            self.menuRun.entryconfig(2, state="normal")
        if clock_now == len(ans_store):
            self.menuRun.entryconfig(1, state="disabled")

    def stepBackward_one(self):
        global clock_now
        if clock_now > 1:
            clock_now -= 1
            self.now['text'] = ' {}   周期'.format(clock_now)
            self.loadtoGUI(ans_store[clock_now - 1])
        if clock_now == 1:
            self.menuRun.entryconfig(2, state="disabled")
        if clock_now <= len(ans_store):
            self.menuRun.entryconfig(1, state="normal")

    def jumpToStep(self):
        global clock_now
        a = askinteger(title='执行至', prompt='请输入要跳转到的周期数' \
                       , initialvalue=clock_now, minvalue=1, maxvalue=len(ans_store))
        if a!=None:
            clock_now = a
            self.now['text'] = ' {}   周期'.format(clock_now)
            self.loadtoGUI(ans_store[clock_now - 1])
            if clock_now > 1:
                self.menuRun.entryconfig(2, state="normal")
            if clock_now == len(ans_store):
                self.menuRun.entryconfig(1, state="disabled")
            if clock_now == 1:
                self.menuRun.entryconfig(2, state="disabled")
            if clock_now <= len(ans_store):
                self.menuRun.entryconfig(1, state="normal")

    def excuteToEnd(self):
        global clock_now
        clock_now = len(ans_store)
        self.now['text'] = ' {}   周期'.format(clock_now)
        self.loadtoGUI(ans_store[clock_now - 1])
        if clock_now > 1:
            self.menuRun.entryconfig(2, state="normal")
        if clock_now == len(ans_store):
            self.menuRun.entryconfig(1, state="disabled")

    def print_ans(self):
        with open(ans_path, 'w', encoding='utf-8') as f2:
            for line in InstrStateList:
                ans = "{:15} IS:{:5} RO:{:5} EX:{:5} WB:{:5}\n". \
                    format(line.toshow[0] + " " + line.toshow[1], line.IS, line.RO, line.EX, line.WB)
                f2.write(ans)

    def reset(self):
        global clock_now
        ans_store.clear()
        instr_queue.clear()
        InstrStateList.clear()
        mainBoard = Scoreboard()
        clock_now = 0

        self.filepath['text'] = ''
        self.now['text'] = ''
        self.fileNow1['text'] = '共{}个周期，目前执行至第:'.format(len(ans_store))
        self.loadtoGUI(mainBoard)
        self.menuFile.entryconfig(2, state="disabled")
        self.menuFile.entryconfig(3, state="disabled")
        self.menuRun.entryconfig(1, state="disabled")
        self.menuRun.entryconfig(2, state="disabled")
        self.menuRun.entryconfig(3, state="disabled")
        self.menuRun.entryconfig(4, state="disabled")

    def setErrPath(self):
        global err_path
        file_path = askopenfilename(title='请选择保存错误日志的路径')
        if file_path!='':
            err_path=file_path

    def setAnsPath(self):
        global ans_path
        file_path = askopenfilename(title='请选择保存结果的路径')
        if file_path!='':
            ans_path=file_path

    def showKonwledge(self):
        showinfo(title='参考文献',message='计算机体系结构（第2版） 王志英等 P122-129')

    def aboutUs(self):
        showinfo(title='关于我们',message='本程序作者：计算机系20级，陈天悦。\n本程序的诞生，离不开史银雪老师一个学期的栽培，再次向史老师表示最衷心的感谢！')

    def createMenu(self):
        self.mainMenu = Menu(self.master)

        self.menuFile = Menu(self.mainMenu)
        self.menuRun = Menu(self.mainMenu)
        self.menuSet = Menu(self.mainMenu)
        self.menuHelp = Menu(self.mainMenu)

        self.mainMenu.add_cascade(label='文件', menu=self.menuFile)
        self.mainMenu.add_cascade(label='执行', menu=self.menuRun)
        self.mainMenu.add_cascade(label='设置', menu=self.menuSet)
        self.mainMenu.add_cascade(label='帮助', menu=self.menuHelp)

        self.menuFile.add_command(label='载入程序', accelerator='I', command=self.loadfile)
        self.menuFile.add_command(label='导出结果', accelerator='O', command=self.print_ans, state='disabled')
        self.menuFile.add_command(label='复位', accelerator='R', command=self.reset, state='disabled')

        self.menuRun.add_command(label='执行一个周期', accelerator='N', command=self.stepForward_one, state='disabled')
        self.menuRun.add_command(label='回退一个周期', accelerator='L', command=self.stepBackward_one, state='disabled')
        self.menuRun.add_command(label='执行至', accelerator='T', command=self.jumpToStep, state='disabled')
        self.menuRun.add_command(label='执行至结束', accelerator='E', command=self.excuteToEnd, state='disabled')

        self.menuSet.add_command(label='设置错误日志路径', accelerator='E',command=self.setErrPath)
        self.menuSet.add_command(label='设置结果导出路径', accelerator='A', command=self.setAnsPath)

        self.menuHelp.add_command(label='参考文献', accelerator='K',command=self.showKonwledge)
        self.menuHelp.add_command(label='关于我们', accelerator='A',command=self.aboutUs)

        self.master['menu'] = self.mainMenu

    def createWidget(self):

        self.frame0 = Frame(self)

        fileNow = Label(self.frame0, relief='flat', height=2, text='当前程序位置:')
        fileNow.grid(row=0, column=0, sticky=W)
        self.filepath = Label(self.frame0, relief='flat', height=2, width=80)
        self.filepath.grid(row=0, column=1)

        self.fileNow1 = Label(self.frame0, relief='flat', height=2, text='共{}个周期，目前执行至第:'.format(len(ans_store)))
        self.fileNow1.grid(row=0, column=2, sticky=W)
        self.now = Label(self.frame0, relief='flat', height=2, width=11)
        self.now.grid(row=0, column=3)

        self.frame0.pack()

        # 定义指令状态表
        self.frame1 = Frame(self)

        Label(self.frame1, relief='groove', text='指令', width=44, height=4).grid(row=0, column=0, rowspan=2,
                                                                                columnspan=2, sticky=NSEW)
        Label(self.frame1, relief='groove', text='指令状态表', width=22, height=2).grid(row=0, column=2, columnspan=4,
                                                                                   sticky=NSEW)
        for i, t in enumerate(['IS', 'RO', 'EX', 'WR']):
            Label(self.frame1, relief='groove', text=t, width=22, height=2).grid(row=1, column=2 + i, sticky=NSEW)

        self.instr_table = []
        for _ in range(3):
            l = []
            for __ in range(5):
                l.append(Label(self.frame1, relief='groove', width=22, height=2))
            self.instr_table.append(l)

        for i, l in enumerate(self.instr_table):
            for k, j in enumerate(l):
                if k == 0:
                    j.grid(row=2 + i, column=0, columnspan=2, sticky=NSEW)
                else:
                    j.grid(row=2 + i, column=1 + k, sticky=NSEW)

        self.frame1.pack(pady=5)

        # 定义功能部件表
        self.frame2 = Frame(self)

        Label(self.frame2, relief='groove', text='部件名称', width=24, height=4).grid(row=0, column=0, rowspan=2,
                                                                                  columnspan=2, sticky=NSEW)
        Label(self.frame2, relief='groove', text='功能部件状态表', width=12, height=2).grid(row=0, column=2, columnspan=9,
                                                                                     sticky=NSEW)
        for i, t in enumerate(['Busy', 'Op', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk']):
            Label(self.frame2, relief='groove', text=t, width=12, height=2).grid(row=1, column=2 + i, sticky=NSEW)

        self.func_table = []
        for t in ['整数', '乘法1', '乘法2', '加法', '除法']:
            l = []
            l.append(Label(self.frame2, relief='groove', text=t, width=12, height=2))
            for __ in range(9):
                l.append(Label(self.frame2, relief='groove', width=12, height=2))
            self.func_table.append(l)

        for i, l in enumerate(self.func_table):
            for k, j in enumerate(l):
                if k == 0:
                    j.grid(row=2 + i, column=0, columnspan=2, sticky=NSEW)
                else:
                    j.grid(row=2 + i, column=1 + k, sticky=NSEW)

        self.frame2.pack(pady=5)

        # 结果寄存器状态表
        self.frame3 = Frame(self)

        Label(self.frame3, relief='groove', width=26, height=4).grid(row=0, column=0, rowspan=2, columnspan=2,
                                                                     sticky=NSEW)
        Label(self.frame3, relief='groove', text='结果寄存器状态表', width=13, height=2).grid(row=0, column=2, columnspan=8,
                                                                                      sticky=NSEW)
        Label(self.frame3, relief='groove', text='部件名称', width=13, height=2).grid(row=2, column=0, columnspan=2,
                                                                                  sticky=NSEW)
        for i, t in enumerate(['F0', 'F2', 'F4', 'F6', 'F8', 'F10', 'F12', 'F14']):
            Label(self.frame3, relief='groove', text=t, width=13, height=2).grid(row=1, column=2 + i, sticky=NSEW)

        self.result_table = []

        for _ in range(8):
            self.result_table.append(Label(self.frame3, relief='groove', width=13, height=2))

        for k, l in enumerate(self.result_table):
            l.grid(row=2, column=2 + k, sticky=NSEW)

        self.frame3.pack(pady=5)


if __name__ == '__main__':
    # readMips('./test.txt')
    root = Tk()
    root.geometry("1000x700+50+50")
    root.title("ScoreBoard Simulator")
    app = Application(master=root)

    root.mainloop()
