#!/usr/bin/env python
import sys

import cv as cv
import numpy as np
import win32gui
from PyQt5.Qt import QApplication


def get_text():
    global hwnd
    hwnd_title = {}

    def _enum_windows(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(_enum_windows, 0)
    for window_id, title in hwnd_title.items():
        if hwnd_title[window_id] == "原神":
            hwnd = window_id
            break
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("test.png")
    pass  # breakpoint


if __name__ == '__main__':
    get_text()
