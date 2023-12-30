from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QFileDialog, QCheckBox, QLineEdit, QSpinBox, QComboBox, QProgressBar, QTextEdit
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont

from in_font import char_in_font
from woker import Worker


class FontExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("TTF2HEX 字体字库转换器    --- By 司沐_Simuoss @ https://github.com/Simuoss")
        
        # 主窗口包含一个水平布局
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        self.setupLeftWidgets(left_layout)
        self.setupRightWidgets(right_layout)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def setupLeftWidgets(self, layout):
        self.setupFileSelection(layout)
        self.setupCanvasFontInputs(layout)
        self.setupCharacterOffsetInputs(layout)
        self.setupFlipMirrorCheckboxes(layout)
        self.setupRotateInvertOptions(layout)
        self.setupExtractFontOptions(layout)
        
    def setupRightWidgets(self, layout):
        self.setupMintArea(layout)
        self.setupPreviewArea(layout)
        self.setupExtractArea(layout)
        
    # 下面是拆分出来的小功能块
    def setupFileSelection(self, layout):
        # 创建选择文件相关部件和布局
        # 创建一个水平布局以容纳文件选择按钮和文件路径文本框
        file_layout = QHBoxLayout()
        # 添加标题和选择文件标签
        title_label = QLabel("选择字体文件:")
        file_layout.addWidget(title_label)
        # 创建一个不可编辑的文本框用于显示文件路径
        self.file_path_textbox = QLineEdit()
        self.file_path_textbox.setReadOnly(True)
        file_layout.addWidget(self.file_path_textbox)
        # 创建一个按钮用于选择文件
        select_file_button = QPushButton("选择文件")
        select_file_button.clicked.connect(self.select_font_file)
        file_layout.addWidget(select_file_button)
        # 将文件选择部件添加到主布局中
        layout.addLayout(file_layout)
        
    
    def setupCanvasFontInputs(self, layout):
        # 创建画布大小、字体大小输入相关部件和布局
        # 添加画布大小、字体大小输入
        canvas_font_layout = QHBoxLayout()
        
        canvas_label = QLabel("画布大小(宽:高):")
        canvas_font_layout.addWidget(canvas_label)
        
        self.canvas_size_width_spinbox = QSpinBox()
        self.canvas_size_width_spinbox.setMinimum(1)
        self.canvas_size_width_spinbox.setValue(12)  # 默认值为8
        canvas_font_layout.addWidget(self.canvas_size_width_spinbox)

        self.canvas_size_height_spinbox = QSpinBox()
        self.canvas_size_height_spinbox.setMinimum(1)
        self.canvas_size_height_spinbox.setValue(12)
        canvas_font_layout.addWidget(self.canvas_size_height_spinbox)

        
        font_label = QLabel("字体大小:")
        canvas_font_layout.addWidget(font_label)
        
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setMinimum(1)
        self.font_size_spinbox.setValue(12)  # 默认值为8
        canvas_font_layout.addWidget(self.font_size_spinbox)
        
        layout.addLayout(canvas_font_layout)
    
    def setupCharacterOffsetInputs(self, layout):
        # 创建字符偏移量输入相关部件和布局
        # 添加字符偏移量输入框及方向提示标签
        offset_layout = QHBoxLayout()
        
        offset_label = QLabel("字符偏移量(可为负):")
        offset_layout.addWidget(offset_label)
        
        self.offset_x_spinbox = QSpinBox()
        self.offset_x_spinbox.setMinimum(-10)
        self.offset_x_spinbox.setMaximum(10)
        offset_layout.addWidget(self.offset_x_spinbox)
        
        self.offset_x_direction_label = QLabel("向右→    ")
        offset_layout.addWidget(self.offset_x_direction_label)
        
        self.offset_y_spinbox = QSpinBox()
        self.offset_y_spinbox.setMinimum(-10)
        self.offset_y_spinbox.setMaximum(10)
        offset_layout.addWidget(self.offset_y_spinbox)
        
        self.offset_y_direction_label = QLabel("↓向下")
        offset_layout.addWidget(self.offset_y_direction_label)
        
        layout.addLayout(offset_layout)

    
    def setupFlipMirrorCheckboxes(self, layout):
        # 创建上下翻转和左右翻转复选框相关部件和布局
        # 添加上下翻转和左右翻转复选框
        flip_mirror_layout = QHBoxLayout()
        
        flip_label = QLabel("上下翻转:")
        flip_mirror_layout.addWidget(flip_label)
        
        self.flip_checkbox = QCheckBox()
        flip_mirror_layout.addWidget(self.flip_checkbox)
        
        mirror_label = QLabel("左右翻转:")
        flip_mirror_layout.addWidget(mirror_label)
        
        self.mirror_checkbox = QCheckBox()
        flip_mirror_layout.addWidget(self.mirror_checkbox)
        
        layout.addLayout(flip_mirror_layout)

    
    def setupRotateInvertOptions(self, layout):
        # 创建旋转角度和反色选项相关部件和布局
        # 并排添加旋转角度和反色选项
        rotate_and_invert_layout = QHBoxLayout()
        # 添加旋转角度选项
        rotate_layout = QHBoxLayout()
        rotate_label = QLabel("顺时针旋转角度:")
        rotate_layout.addWidget(rotate_label)
        self.rotate_combobox = QComboBox()
        self.rotate_combobox.addItem("0°")
        self.rotate_combobox.addItem("90°")
        self.rotate_combobox.addItem("180°")
        self.rotate_combobox.addItem("270°")
        rotate_layout.addWidget(self.rotate_combobox)
        rotate_and_invert_layout.addLayout(rotate_layout)
        # 添加反色选项
        invert_label = QLabel("          反色:")
        rotate_and_invert_layout.addWidget(invert_label)
        self.invert_checkbox = QCheckBox()
        rotate_and_invert_layout.addWidget(self.invert_checkbox)
        layout.addLayout(rotate_and_invert_layout)

    
    def setupExtractFontOptions(self, layout):
        # 创建提取字体选项相关部件和布局
        # 添加提取字体选项
        # 创建布局
        extract_range_layout = QVBoxLayout()
        self.extract_font_label = QLabel("选择提取字体范围:")
        extract_range_layout.addWidget(self.extract_font_label)
        
        # 创建全选复选框
        self.select_all_checkbox = QCheckBox("所有字体(很大，慎用)")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        extract_range_layout.addWidget(self.select_all_checkbox)
        # 创建其他提取范围复选框
        self.ascii_checkbox = QCheckBox("ASCII可见字符集(0x0020, 0x007E)")
        self.chinese_checkbox = QCheckBox("所有汉字(0x4E00, 0x9FFF)")
        self.common_chinese_checkbox = QCheckBox("常用汉字(0x4E00, 0x9FA5)")
        self.chinese_punctuation_checkbox = QCheckBox("汉字标点符号(0x3000, 0x303F)")

        
        extract_range_layout.addWidget(self.ascii_checkbox)
        extract_range_layout.addWidget(self.chinese_checkbox)
        extract_range_layout.addWidget(self.common_chinese_checkbox)
        extract_range_layout.addWidget(self.chinese_punctuation_checkbox)

        # 创建自选区域复选框
        self.custom_range_checkbox = QCheckBox("自选区域")
        self.custom_range_checkbox.stateChanged.connect(self.toggle_custom_range)
        extract_range_layout.addWidget(self.custom_range_checkbox)

        # 创建水平布局用于放置自选区域输入框
        custom_range_layout = QHBoxLayout()

        # 创建自选区域输入框
        self.range_from_input = QLineEdit()
        self.range_from_input.setPlaceholderText("开始（0x0000）")
        self.range_to_input = QLineEdit()
        self.range_to_input.setPlaceholderText("结束（0xFFFF）")
        self.range_from_input.setEnabled(False)
        self.range_to_input.setEnabled(False)

        custom_range_layout.addWidget(self.range_from_input)
        custom_range_layout.addWidget(self.range_to_input)
        extract_range_layout.addLayout(custom_range_layout)

        # 创建从文本复选框，后面跟一个文本框
        self.extract_from_text_checkbox = QCheckBox("从文本提取(一般用这个)")
        self.extract_from_text_checkbox.stateChanged.connect(self.toggle_extract_from_text)
        extract_range_layout.addWidget(self.extract_from_text_checkbox)
        self.extract_from_text_input = QTextEdit()
        self.extract_from_text_input.setPlaceholderText("输入要提取的字符")
        self.extract_from_text_input.setEnabled(False)
        extract_range_layout.addWidget(self.extract_from_text_input)

        layout.addLayout(extract_range_layout)
        
        # 标志变量来控制复选框状态
        self.custom_range_enabled = False

    
    def setupMintArea(self, layout):
        # 预览区域标题
        preview_label = QLabel("预览区域:")
        layout.addWidget(preview_label)
        # 提示标签
        preview_tip_label1 = QLabel("有些字体标的是12px，但实际上调到15px才是正常的12px状态，需要多微调参数试试")
        layout.addWidget(preview_tip_label1)
        preview_tip_label2 = QLabel("有些屏幕显示点阵是旋转过的，比如1306的oled屏就需要上下翻转+旋转90°才是正的")
        layout.addWidget(preview_tip_label2)
    
    def setupPreviewArea(self, layout):
        # 创建预览图像展示框
        self.preview_image_label = QLabel()
        self.preview_image_label.setAlignment(Qt.AlignCenter)
        self.preview_image_label.setFixedSize(400, 400)
        self.preview_image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.preview_image_label)
        
        # 创建预览操作区域
        preview_options_layout = QHBoxLayout()
        # 创建预览字符输入框
        self.preview_input = QLineEdit()
        self.preview_input.setPlaceholderText("输入字符或 Unicode 编码")
        # 默认是A
        self.preview_input.setText("A")
        preview_options_layout.addWidget(self.preview_input)
        # 创建预览按钮
        preview_button = QPushButton("预览")
        preview_button.clicked.connect(self.preview_font)
        preview_options_layout.addWidget(preview_button)

        layout.addLayout(preview_options_layout)

    def setupExtractArea(self, layout):
        # 创建提取字体按钮
        extract_button = QPushButton("提取字体")
        extract_button.clicked.connect(self.extract_font)
        layout.addWidget(extract_button)
        
        # 创建主任务的进度条
        self.main_progress_bar = QProgressBar()
        self.main_progress_bar.setRange(0, 100)
        self.main_progress_bar.setValue(0)
        self.main_progress_bar.setFormat("等待开始")
        layout.addWidget(self.main_progress_bar)

    




        




        







    def update_main_progress(self, progress, text):
        self.main_progress_bar.setValue(progress)
        self.main_progress_bar.setFormat(text)

    
    def select_font_file(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择字体文件", "", "TrueType 字体文件 (*.ttf)", options=options)
        if file_path:
            self.file_path_textbox.setText(file_path)
            #print(f"已选择字体文件：{file_path}")

    def toggle_extract_from_text(self, state):
        # 如果选中了从文本提取，则禁用其他提取范围复选框
        if state:
            self.select_all_checkbox.setChecked(False)
            self.select_all_checkbox.setEnabled(False)

            self.ascii_checkbox.setChecked(False)
            self.ascii_checkbox.setEnabled(False)

            self.chinese_checkbox.setChecked(False)
            self.chinese_checkbox.setEnabled(False)

            self.common_chinese_checkbox.setChecked(False)
            self.common_chinese_checkbox.setEnabled(False)

            self.chinese_punctuation_checkbox.setChecked(False)
            self.chinese_punctuation_checkbox.setEnabled(False)

            self.custom_range_checkbox.setChecked(False)
            self.custom_range_checkbox.setEnabled(False)

            self.extract_from_text_input.setEnabled(True)
        else:
            self.select_all_checkbox.setEnabled(True)
            self.ascii_checkbox.setEnabled(True)
            self.chinese_checkbox.setEnabled(True)
            self.common_chinese_checkbox.setEnabled(True)
            self.chinese_punctuation_checkbox.setEnabled(True)
            self.custom_range_checkbox.setEnabled(True)
            self.extract_from_text_input.setEnabled(False)
            




    def toggle_select_all(self, state):
        self.ascii_checkbox.setChecked(state)
        self.ascii_checkbox.setEnabled(not state)
        
        self.chinese_checkbox.setChecked(state)
        self.chinese_checkbox.setEnabled(not state)
        
        self.common_chinese_checkbox.setChecked(state)
        self.common_chinese_checkbox.setEnabled(not state)
        
        self.chinese_punctuation_checkbox.setChecked(state)
        self.chinese_punctuation_checkbox.setEnabled(not state)
        
        self.custom_range_checkbox.setChecked(state)
        self.custom_range_checkbox.setEnabled(not state)

        self.extract_from_text_checkbox.setChecked(False)
        self.extract_from_text_checkbox.setEnabled(not state)


        self.toggle_custom_range(state)


    # 切换自选区域输入框的状态
    def toggle_custom_range(self, state):
        if not self.custom_range_enabled:
            self.range_from_input.setEnabled(True)
            self.range_to_input.setEnabled(True)
            self.custom_range_enabled = True
        else:
            self.range_from_input.setEnabled(False)
            self.range_to_input.setEnabled(False)
            self.custom_range_enabled = False


    def preview_font(self):
        font_path = self.file_path_textbox.text()
        font_size = self.font_size_spinbox.value()
        canvas_size_width = self.canvas_size_width_spinbox.value()
        canvas_size_height = self.canvas_size_height_spinbox.value()
        offset_x = self.offset_x_spinbox.value()
        offset_y = self.offset_y_spinbox.value()
        flip = self.flip_checkbox.isChecked()
        mirror = self.mirror_checkbox.isChecked()
        rotate = self.rotate_combobox.currentText()
        preview_text = self.preview_input.text()
        reverse_color = self.invert_checkbox.isChecked()
        if not font_path:
            self.update_main_progress(0, "还没选字体呢")
            return
        if not preview_text:
            self.update_main_progress(0, "还没输入预览字符呢")
            return
        if not preview_text.isprintable():
            self.update_main_progress(0, "这个字符显示不出呢")
            return
        # 如果整个preview_text存在字符不在字体里，则不显示
        if not all(char_in_font(c, TTFont(font_path)) for c in preview_text):
            self.update_main_progress(0, "字体里没有这个字呢")
            return
        

        # 创建一个空白画布来绘制字符
        canvas = Image.new("1", (canvas_size_width, canvas_size_height), reverse_color)

        # 使用PIL加载字体文件
        font = ImageFont.truetype(font_path, size=font_size)
        draw = ImageDraw.Draw(canvas)
        # 清空图像内容（不一定是8*8）
        draw.rectangle([0, 0, canvas_size_width, canvas_size_height], fill=reverse_color)#参数为左上角和右下角的坐标
        # 在图像上绘制字符
        draw.text((offset_x,offset_y), preview_text, font=font, fill= not reverse_color)

        # 上下翻转
        if flip:
            canvas = canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # 左右翻转
        if mirror:
            canvas = canvas.transpose(Image.FLIP_LEFT_RIGHT)
        # 顺时针旋转
        if rotate == "90°":
            canvas = canvas.transpose(Image.ROTATE_270)# 逆时针旋转270°，即顺时针旋转90°
        elif rotate == "180°":
            canvas = canvas.transpose(Image.ROTATE_180)
        elif rotate == "270°":
            canvas = canvas.transpose(Image.ROTATE_90)

        
        # 获取字符的点阵表示
        pixels = list(canvas.getdata())
        bitmap = [pixels[i:i+canvas_size_width] for i in range(0, len(pixels), canvas_size_width)]

        # 将点阵转换为硬缩放不大于400*400的图像
        zoom = 300 // canvas_size_width
        canvas = Image.new("1", (canvas_size_width*zoom, canvas_size_height*zoom))
        draw = ImageDraw.Draw(canvas)
        for y in range(canvas_size_height):
            for x in range(canvas_size_width):
                if bitmap[y][x]:
                    draw.rectangle([x*zoom, y*zoom, (x+1)*zoom, (y+1)*zoom], fill=0)
                else:
                    draw.rectangle([x*zoom, y*zoom, (x+1)*zoom, (y+1)*zoom], fill=1)
        



        # 在将 PIL.Image 转换为 QImage 对象时，需要将其模式转换为 RGB888 或 ARGB32
        canvas = canvas.convert("RGB")
        # 将 PIL.Image 转换为 QImage 对象
        qimage = QImage(canvas.tobytes(), canvas.width, canvas.height, QImage.Format_RGB888)

        # 然后再将 QImage 对象传递给 QPixmap.fromImage 方法
        self.preview_image_label.setPixmap(QPixmap.fromImage(qimage))
        
    def extract_font(self):
        font_path = self.file_path_textbox.text()
        font_size = self.font_size_spinbox.value()
        canvas_size_width = self.canvas_size_width_spinbox.value()
        canvas_size_height = self.canvas_size_height_spinbox.value()
        offset_x = self.offset_x_spinbox.value()
        offset_y = self.offset_y_spinbox.value()
        flip = self.flip_checkbox.isChecked()
        mirror = self.mirror_checkbox.isChecked()
        rotate = self.rotate_combobox.currentText()
        reverse_color = self.invert_checkbox.isChecked()
        input_text = self.extract_from_text_input.toPlainText()

        if not font_path:
            self.update_main_progress(0, "还没选字体呢")
            return
        # 如果没选中任何提取范围，则默认提取 ASCII 可见字符集
        if not self.ascii_checkbox.isChecked() and not self.chinese_checkbox.isChecked() \
            and not self.common_chinese_checkbox.isChecked() and not self.chinese_punctuation_checkbox.isChecked() \
            and not self.custom_range_checkbox.isChecked() and not self.extract_from_text_checkbox.isChecked():
            self.ascii_checkbox.setChecked(True)

        # 如果选择了自选区域，则检查输入是否合法
        if self.custom_range_checkbox.isChecked() and not self.select_all_checkbox.isChecked():
            range_from = self.range_from_input.text()
            range_to = self.range_to_input.text()
            if not range_from or not range_to:
                self.update_main_progress(0,"自选区域想选什么呢？")
                return
            if not range_from.startswith("0x") or not range_to.startswith("0x"):
                self.update_main_progress(0,"自选区域要0x开头哦")
                return
            range_from = int(range_from, 16)
            range_to = int(range_to, 16)
            if range_from > range_to:
                self.update_main_progress(0,"自选区域要从小到大哦")
                return
        
        # 确定提取范围
        extract_range = ""
        if self.extract_from_text_checkbox.isChecked():# 从文本提取
            extract_range = input_text
        elif self.select_all_checkbox.isChecked():# 全选
            extract_range = [chr(i) for i in range(0x0000, 0xFFFF + 1)]
        else:
            if self.ascii_checkbox.isChecked():# ASCII 可见字符集
                extract_range += "".join([chr(i) for i in range(0x0020, 0x007E + 1)])
            if self.chinese_checkbox.isChecked():# 所有汉字
                extract_range += "".join([chr(i) for i in range(0x4E00, 0x9FFF + 1)])
            if self.common_chinese_checkbox.isChecked():# 常用汉字
                extract_range += "".join([chr(i) for i in range(0x4E00, 0x9FA5 + 1)])
            if self.chinese_punctuation_checkbox.isChecked():# 汉字标点符号
                extract_range += "".join([chr(i) for i in range(0x3000, 0x303F + 1)])
            if self.custom_range_checkbox.isChecked():# 自选区域
                extract_range += "".join([chr(i) for i in range(range_from, range_to + 1)])
        
        #print(f"提取范围：{extract_range}")

        # 创建 Worker 对象
        self.worker = Worker(font_path, font_size, canvas_size_width, canvas_size_height, offset_x, offset_y, flip, mirror, rotate, reverse_color, extract_range)
        # 连接 Worker 信号与槽函数
        self.worker.update_main_progress.connect(self.update_main_progress)

        self.worker.start()