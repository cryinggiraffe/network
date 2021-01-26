#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
from mygui import *
import network
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()

    ui = Ui_Dialog()  # 这里改成你自己的项目名称，如果你没特意改过，就默认就行

    ui.setupUi(widget)

    widget.show()

    sys.exit(app.exec_())
