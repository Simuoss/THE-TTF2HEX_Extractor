import os
import re
from PySide6.QtCore import QThread, Signal
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont

from in_font import char_in_font

class Worker(QThread):
    update_main_progress = Signal(int, str)


    def __init__(self, font_path, font_size, canvas_size_width, canvas_size_height, offset_x, offset_y, flip, mirror, rotate, reverse_color, extract_range, parent=None):
        super().__init__(parent)
        self.font_path = font_path
        self.font_size = font_size
        self.canvas_size_width = canvas_size_width
        self.canvas_size_height = canvas_size_height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.flip = flip
        self.mirror = mirror
        self.rotate = rotate
        self.reverse_color = reverse_color
        self.extract_range = extract_range

        
    def run(self):
        # 字体文件路径
        font_path = self.font_path
        # 画布大小
        canvas_size_width = self.canvas_size_width
        canvas_size_height = self.canvas_size_height
        # 字体大小
        font_size = self.font_size
        # 反色
        reverse_color = self.reverse_color
        # 字符偏移量
        character_offset_x = self.offset_x
        character_offset_y = self.offset_y
        # 是否让字符上下翻转
        flip_character = self.flip
        # 是否让字符左右翻转
        mirror_character = self.mirror
        # 顺时针旋转多少度
        rotate_degree = self.rotate
        # 要提取的字符列表
        ori_characters = self.extract_range


        # 开启进度条
        total = len(ori_characters)
        step = 0
        not_in = 0
        self.update_main_progress.emit(0,"开始处理")

        # 使用PIL加载字体文件
        font = ImageFont.truetype(font_path, size=font_size)
        cfont = TTFont(font_path)
        # 创建一个空白画布来绘制字符
        image = Image.new("1", (canvas_size_width, canvas_size_height), reverse_color)
        draw = ImageDraw.Draw(image)

        # 生成类似C语言数组的输出
        base_font_name = os.path.basename(font_path)
        # 使用正则表达式替换非字母、数字和下划线的字符为下划线
        base_font_name = re.sub(r'[^a-zA-Z0-9_]', '_', base_font_name)

        # save
        with open(f"{base_font_name}.h", "w", encoding="utf-8") as f:
            f.writelines(f"#ifndef __{base_font_name.upper()}_FONT_H__\n#define __{base_font_name.upper()}_FONT_H__\n\n")
            f.writelines("const unsigned char code F_zh_cn_8x8[][8] = {\n")
            for char in ori_characters:
                if not char_in_font(char, cfont):
                    not_in += 1
                    continue


                # 清空图像内容
                draw.rectangle([0, 0, canvas_size_width, canvas_size_height], fill=reverse_color)#参数为左上角和右下角的坐标
                # 在图像上绘制字符
                draw.text((character_offset_x,character_offset_y), char, font=font, fill= not reverse_color)
                
                # 获取字符的点阵表示
                pixels = list(image.getdata())
                bitmap = [pixels[i:i+canvas_size_width] for i in range(0, len(pixels), canvas_size_width)]
                
                # 把每个char的每一行都翻转一下
                if flip_character:
                    bitmap.reverse()
                # 把每个char的每一列都翻转一下
                if mirror_character:
                    bitmap = [row[::-1] for row in bitmap]
                
                # 顺时针旋转
                if rotate_degree == '90°':
                    bitmap = list(zip(*bitmap[::-1]))
                elif rotate_degree == '180°':
                    bitmap = [row[::-1] for row in bitmap[::-1]]
                elif rotate_degree == '270°':
                    bitmap = list(zip(*bitmap))[::-1]

                # 以UTF-8写入文件
                try:
                    f.writelines(f"    // {char.encode('unicode-escape').decode()}: {char}\n")
                except:
                    f.writelines(f"    // 无法显示该字符\n")
                f.writelines("    {")
                for row in bitmap:
                    # 所以row是一个长度为8的数组，每个元素是一个bit。现在要把这个数组转换成一个byte，所以要把这8个bit拼接成一个byte。
                    row_hex = 0
                    for i in range(8):
                        row_hex |= row[i] << i
                    # 用十六进制表示byte
                    f.writelines(f"0x{row_hex:02X}, ")
                    
                f.writelines("},\n")

                step += 1
                self.update_main_progress.emit(step / total * 100, f"{step / total * 100:.1f}%  已处理{step}/{total}个字符")
            f.writelines("};\n\n#endif\n")
            f.writelines(f"// 提取完成，应提取{total}个字符，实际提取{total - not_in}个字符，有{not_in}个字符不在字体里。")

        # 关闭进度条
        self.update_main_progress.emit(100, f"完成！应提{total}字，实提{total - not_in}字，{not_in}字符不存在。已保存在同级目录。")