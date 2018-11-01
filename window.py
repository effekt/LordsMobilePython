import win32con
import win32gui


class Window:
    def __init__(self):
        self.hwnd = None
        self.getWindow()
        win32gui.MoveWindow(self.hwnd, 0, 0, 1015, 582, True)
        self.window = win32gui.GetWindowRect(self.hwnd)
        self.game = {
            'x1': self.window[0],
            'y1': self.window[1],
            'x2': self.window[2],
            'y2': self.window[3],
            'w': self.window[2] - self.window[0],
            'h': self.window[3] - self.window[1],
            'midx': int(self.window[2] / 2),
            'midy': int(self.window[3] / 2)
        }

    def isRealWindow(self, hWnd):
        if not win32gui.IsWindowVisible(hWnd):
            return False
        if win32gui.GetParent(hWnd) != 0:
            return False
        hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
        lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
        if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
          or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
            if win32gui.GetWindowText(hWnd):
                return True
        return False

    def getWindow(self):
        def callback(hwnd, extra):
            if win32gui.GetWindowText(hwnd) == 'MEmu':
                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0]
                y = rect[1]
                w = rect[2] - x
                h = rect[3] - y
                if w > 500 and h > 300:
                    self.hwnd = hwnd
        win32gui.EnumWindows(callback, None)
