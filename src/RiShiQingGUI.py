from tkinter import *
from tkinter import ttk
import time
import locale

# 设置底层接口编码
locale.setlocale(locale.LC_CTYPE, 'chinese')
now = time.strftime('%Y.%m.%d', time.localtime())


class Tks(object):
    _app = None
    _day = None
    _root = None
    _mRoot = None
    _fRoot = None
    _cRoot = None
    _pRoot =None
    _variable = []
    _startTime1 = None
    _startTime2 = None
    _endTime1 = None
    _endTime2 = None
    _task = None
    _title = None
    _result = None

    def __init__(self, app):
        self._app = app
        # GUI部分
        self._root = root = Tk()
        # 主页面
        root.title('日事清')
        root.geometry('480x520')
        self._title = today = StringVar()
        label = ttk.Label(root, textvariable=today)
        self._day = now
        today.set(self._day + ' 计划表')
        label.pack()
        # 加载操作栏
        self.create_m_root()
        # 加载添加计划栏
        self.create_c_root()
        # 加载列表栏
        self.create_f_root()
        mainloop()

    def create_m_root(self):
        self._mRoot = m_root = LabelFrame(self._root, text='操作栏', width=100)
        ttk.Button(m_root, text='前一天', width=6, style='TButton', command=self.last_day).grid(column=0, row=0)
        ttk.Label(m_root, text='  ', width=19).grid(column=2, row=0, columnspan=2)
        ttk.Label(m_root, text='  ', width=12).grid(column=3, row=0)
        ttk.Button(m_root, text='刷新', width=6, style='TButton', command=self.refresh).grid(column=4, row=0)
        ttk.Label(m_root, text='  ', width=19).grid(column=5, row=0, columnspan=3)
        ttk.Button(m_root, text='后一天', width=6, style='TButton', command=self.next_day).grid(column=8, row=0)
        m_root.pack()

    def create_c_root(self):
        self._cRoot = c_root = LabelFrame(self._root, text='添加计划')
        c_root.pack()
        self._startTime1 = StringVar()
        self._startTime2 = StringVar()
        self._endTime1 = StringVar()
        self._endTime2 = StringVar()
        self._task = StringVar()
        ttk.Label(c_root, text='开始时间', width=28).grid(column=0, row=0, columnspan=3)
        ttk.Label(c_root, text='结束时间', width=28).grid(column=3, row=0, columnspan=3)
        ttk.Entry(c_root, textvariable=self._startTime1, width=10).grid(column=0, row=1, stick='w')
        ttk.Label(c_root, text=':', width=2).grid(column=1, row=1, stick='w')
        ttk.Entry(c_root, textvariable=self._startTime2, width=10).grid(column=2, row=1, stick='w')
        ttk.Entry(c_root, textvariable=self._endTime1, width=10).grid(column=3, row=1, stick='w')
        ttk.Label(c_root, text=':', width=2).grid(column=4, row=1, stick='w')
        ttk.Entry(c_root, textvariable=self._endTime2, width=10).grid(column=5, row=1, stick='w')
        ttk.Label(c_root, text='计划做什么事情').grid(column=0, row=2, stick='w',columnspan=6)
        ttk.Entry(c_root, textvariable=self._task, width=53).grid(column=0, row=3, stick='w', columnspan=6)
        ttk.Button(c_root, text='+', width=3, style='TButton', command=self.add_task).grid(column=6, row=3)

    def create_f_root(self):
        if self._app is not None:
            app = self._app
            self._result = result = app.get_timer(self._day)
            self._variable = None
            self._fRoot = tabs = ttk.Notebook(self._root)
            tabs.pack()
            if len(result) > 0:
                length = len(result)
                if length % 10 == 0:
                    num = int(length / 10) - 1
                else:
                    num = int(length / 10)
                for n in range(0, num + 1):
                    self.create_f_root_page(n, tabs)

    def create_f_root_page(self, num, tabs):
        tab = ttk.Frame(tabs)
        tabs.add(tab, text='第%s页' % (num + 1))
        fRoot = LabelFrame(tab, text='计划详情')
        fRoot.pack()
        variable = []
        if self._variable is None:
            self._variable = variable
        else:
            variable = self._variable
        i = num
        for index, timer in enumerate(sorted(self._result, key=lambda times: times['boxContent'], reverse=True)):
            if index < num * 10 or index >= (num + 1) * 10:
                continue
            is_done = timer['isDone']
            if is_done:
                variable.append(IntVar().set(1))
            else:
                variable.append(IntVar())
            ttk.Checkbutton(fRoot, text=timer['boxContent'], width=54, variable=variable[i],
                            command=lambda box_id=timer['id'], done=timer['isDone']: self.checkbox_change(box_id,
                                                                                                          done)).grid(
                column=0, row=i, columnspan=2)
            ttk.Button(fRoot, text='-', width=3, style='TButton',
                       command=lambda box_id=timer['id']: self.del_list(box_id)).grid(column=2, row=i)
            i += 1

    def checkbox_change(self, box_id, is_done):
        self._app.isDone(box_id, is_done, self.refresh)

    def refresh(self):
        self._fRoot.destroy()
        self._cRoot.destroy()
        self.create_c_root()
        self.create_f_root()

    def del_list(self, box_id):
        self._fRoot.destroy()
        self._app.delete_msg(box_id, self.refresh)

    def add_task(self):
        start_time = self._startTime1.get() + ':' + self._startTime2.get()
        end_time = self._endTime1.get() + ':' + self._endTime2.get()
        self._app.set_timer(self._task.get(), start_time, end_time, self.refresh)

    def last_day(self):
        # 获取当前显示日期的时间戳
        now_long = time.mktime(time.strptime(self._day, '%Y.%m.%d'))
        now_long -= 3600*24
        self._day = time.strftime('%Y.%m.%d', time.localtime(now_long))
        self._title.set(self._day + ' 计划表')
        self.refresh()

    def next_day(self):
        # 获取当前显示日期的时间戳
        now_long = time.mktime(time.strptime(self._day, '%Y.%m.%d'))
        now_long += 3600 * 24
        self._day = time.strftime('%Y.%m.%d', time.localtime(now_long))
        self._title.set(self._day + ' 计划表')
        self.refresh()
