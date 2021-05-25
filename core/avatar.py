import os
import xml.etree.ElementTree as ET


class 解析():
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__数据准备()
        self.__数据读取()
        self.__数据处理()

    def __数据准备(self):
        self.文件名称 = os.path.basename(self.__file_path)
        self.__up_folder = os.path.dirname(os.path.dirname(self.__file_path))
        self.文件列表 = []

    def __数据读取(self):
        tree = ET.parse(self.__file_path)
        root = tree.getroot()
        for children in root.getchildren():
            # print(children.tag, children.attrib)
            # 'file': 'characters/actress1/models/actress1_md_body.model'
            file_name = children.attrib["file"]
            if file_name.endswith(".model"):
                # E:\Unpack_Files\Gujian3\asset\characters/actress1/models/actress1_md_body.model
                file_path = self.__up_folder + "\\" + file_name
                # E:\Unpack_Files\Gujian3\asset\characters\actress1\models\actress1_md_body.model
                file_path = file_path.replace("/", os.sep)

                self.文件列表.append(file_path)
                # print(file_path)

        # for childrens in root:
        #     for children in childrens:
        #         print(children.tag, children.attrib)

    def __数据处理(self):
        pass


if __name__ == "__main__":
    file_path = "E:\\Unpack_Files\\Gujian3\\asset\\avatar\\actress1_md_default.avatar"
    解析(file_path)
