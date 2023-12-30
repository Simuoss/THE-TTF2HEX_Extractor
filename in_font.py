from fontTools.ttLib import TTFont

def char_in_font(char: str, cfont: TTFont) -> bool:
            """判断字符是否在字体里

            Args:
                char (str): 单字符文本
                fontfile (str): 字体文件

            Returns:
                bool: 是否在字体里
            """
            code = char.encode("unicode-escape").decode()
            if "\\u" in code:
                code = "uni" + code[2:].upper()
            
            glyf = cfont["glyf"]
            if not glyf.has_key(code):
                return False
            return len(glyf[code].getCoordinates(0)[0]) > 0