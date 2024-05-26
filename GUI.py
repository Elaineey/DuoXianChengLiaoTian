import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt  # 导入 Qt 以访问对齐标志
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QLineEdit, QVBoxLayout, QWidget, QComboBox, QTableWidget,
                             QTableWidgetItem, QApplication, QToolBar, QPushButton)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('多线程聊天分析')
        self.setGeometry(100, 100, 800, 600)

        # 创建工具栏模拟菜单栏
        tool_bar = QToolBar("Menu")
        self.addToolBar(tool_bar)

        # 创建 Actions
        task_init_action = QAction('任务初始化', self)
        concurrent_exec_action = QAction('并发执行', self)
        result_analysis_action = QAction('结果分析', self)

        # 连接动作与方法
        task_init_action.triggered.connect(self.display_task_init)
        concurrent_exec_action.triggered.connect(self.display_concurrent_exec)
        result_analysis_action.triggered.connect(self.display_result_analysis)

        # 将动作添加到工具栏
        tool_bar.addAction(task_init_action)
        tool_bar.addAction(concurrent_exec_action)
        tool_bar.addAction(result_analysis_action)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.display_task_init()  # 默认显示任务初始化界面

    def display_task_init(self):
        self.clear_layout(self.layout)

        # 顶部的输入布局
        top_layout = QtWidgets.QHBoxLayout()  # 水平布局用于顶部输入区域

        # 创建并添加 'From' 标签和输入框
        self.from_label = QLabel('From:', self)
        self.from_input = QLineEdit(self)
        top_layout.addWidget(self.from_label)
        top_layout.addWidget(self.from_input)

        # 创建并添加 'To' 标签和输入框
        self.to_label = QLabel('To:', self)
        self.to_input = QLineEdit(self)
        top_layout.addWidget(self.to_label)
        top_layout.addWidget(self.to_input)

        # 添加确认按钮
        self.confirm_button = QPushButton('确认', self)
        self.confirm_button.clicked.connect(self.update_table)
        top_layout.addWidget(self.confirm_button)

        # 添加顶部布局到主布局
        self.layout.addLayout(top_layout)

        # 创建表格并设置表格属性
        self.task_table = QTableWidget(0, 5, self)  # 初始化时没有行，5列
        self.task_table.setHorizontalHeaderLabels(['ID', '消息内容', '开始时间', '结束时间', '吞吐量'])
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.task_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # 将表格添加到主布局中
        self.layout.addWidget(self.task_table)

        # 确保表格和输入区域垂直排列
        self.layout.addStretch(1)

    def update_table(self):
        # 获取输入数据
        from_value = self.from_input.text()
        to_value = self.to_input.text()

        # 计算新行的索引（行号）
        row_position = self.task_table.rowCount()

        # 插入新行
        self.task_table.insertRow(row_position)

        # 添加数据到新行
        self.task_table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))  # ID
        self.task_table.setItem(row_position, 1, QTableWidgetItem(from_value))  # 消息内容
        self.task_table.setItem(row_position, 2, QTableWidgetItem(to_value))  # 开始时间
        self.task_table.setItem(row_position, 3, QTableWidgetItem("示例结束时间"))  # 结束时间
        self.task_table.setItem(row_position, 4, QTableWidgetItem("示例吞吐量"))  # 吞吐量

    def display_concurrent_exec(self):
        self.clear_layout(self.layout)
        self.parallelism_label = QLabel('Select Parallelism (1 to 10):', self)
        self.parallelism_combo = QComboBox(self)
        self.parallelism_combo.addItems([str(i) for i in range(1, 11)])

        # 初始化表格，并设置最大行数
        self.task_table = QTableWidget(10, 4, self)
        self.task_table.setHorizontalHeaderLabels(['ID', '开始时间', '结束时间', '所完成的任务'])
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.task_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # 连接下拉框的变化信号到更新行数的函数
        self.parallelism_combo.currentIndexChanged.connect(self.update_table_rows)

        # 设置布局，添加控件
        self.layout.addWidget(self.parallelism_label)
        self.layout.addWidget(self.parallelism_combo)
        self.layout.addWidget(self.task_table, 1)

        # 根据下拉框当前索引初始化表格行数
        self.update_table_rows(self.parallelism_combo.currentIndex())

    def update_table_rows(self, index):
        number_of_rows = index + 1
        self.task_table.setRowCount(number_of_rows)

        for row in range(number_of_rows):

            id_item = QtWidgets.QTableWidgetItem(str(row + 1))
            id_item.setTextAlignment(Qt.AlignCenter)  # 设置文本居中对齐

            self.task_table.setItem(row, 0, id_item)

            # 为其他列也设置示例数据和居中对齐
            for column in range(1, 4):  # 假设表格有4列
                item = QtWidgets.QTableWidgetItem(f"示例数据 {row + 1}, {column}")
                item.setTextAlignment(Qt.AlignCenter)  # 设置文本居中对齐
                self.task_table.setItem(row, column, item)

    def display_result_analysis(self):
        self.clear_layout(self.layout)
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [10, 1, 20, 3, 40], 'r-')
        ax.set_title('Analysis of results')
        ax.set_xlabel('Number of threads')
        ax.set_ylabel('Total implementation time')

        self.layout.addWidget(canvas)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainUI()
    gui.show()
    sys.exit(app.exec_())
