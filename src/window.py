import wx
import wx.adv
from RiShiQing import RiShiQing
from RiShiQingGUI import Tks


class MyTaskBarIcon(wx.adv.TaskBarIcon):
    _icon = 'logo.ico'  # 图标地址
    _about_id = wx.NewId()  # 菜单选项“关于”的ID
    _exit_id = wx.NewId()  # 菜单选项“退出”的ID
    _show_id = wx.NewId()  # 菜单选项“显示页面”的ID
    _title = '日事清PythonV1.0'
    _author = 'LazyMax'
    _last_change = '2019-01-10'

    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self._icon), self._title)  # 设置图标和标题
        print('%s , %s , %s' %(self._about_id, self._exit_id, self._show_id))
        self.Bind(wx.EVT_MENU, self.on_about, id=self._about_id)  # 绑定“关于”选项的点击事件
        self.Bind(wx.EVT_MENU, self.on_exit, id=self._exit_id)  # 绑定“退出”选项的点击事件
        self.Bind(wx.EVT_MENU, self.on_show_web, id=self._show_id)  # 绑定“显示页面”选项的点击事件

    def on_about(self, event):
        wx.MessageBox('作者: %s \n最后更新日期: %s' % (self._author, self._last_change), '关于')

    def on_exit(self, event):
        wx.Exit()

    # “显示页面”选项的事件处理器
    def on_show_web(self, event):
        Tks(RiShiQing())

    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for menuAttr in [('进入程序', self._show_id),
                ('关于', self._about_id),
                ('退出', self._exit_id)]:
            menu.Append(menuAttr[1], menuAttr[0])
        return menu


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True


if __name__ == "__main__":
    Tks(RiShiQing())
    app = MyApp()
    app.MainLoop()
