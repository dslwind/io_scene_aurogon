from dataclasses import dataclass, field


@dataclass
class 烛龙材质:
    名称: str = ""
    贴图字典: dict = field(default_factory=dict)


@dataclass
class 烛龙骨骼:
    ID: int = -1
    名称: str = ""
    父骨骼ID: int = -1
    父骨骼名称: str = ""
    头位置: list = field(default_factory=list)  # mathutils.Vector([x,y,z])
    尾位置: list = field(default_factory=list)  # mathutils.Vector([x,y,z])

    头位置vec3: list = field(default_factory=list)
    中位置vec3: list = field(default_factory=list)
    尾位置vec3: list = field(default_factory=list)
    头四元数: list = field(default_factory=list)  # mathutils.Quaternion([w,x,y,z])
    中四元数: list = field(default_factory=list)  # mathutils.Quaternion([w,x,y,z])
    尾四元数: list = field(default_factory=list)  # mathutils.Quaternion([w,x,y,z])


@dataclass
class 烛龙骨架:
    名称: str = ""
    骨骼列表: list = field(default_factory=list)
# 约定，仅有骨架名称来源于文件名称与文件名称一致。在blender导入中，使用骨架名称，不使用文件名称。


@dataclass
class 烛龙骨骼ID和权重值:
    骨骼ID: int = -1
    权重值: float = 0.0


@dataclass
class 烛龙顶点权重:
    顶点ID: int = -1
    骨骼ID和权重值列表: list = field(default_factory=list)  # 每个顶点都有一系列骨骼ID和权重值列表


@dataclass
class 烛龙顶点ID和权重值:
    顶点ID: int = -1
    权重值: float = 0.0


@dataclass
class 烛龙顶点组:
    骨骼ID: int = -1
    骨骼名称: str = ""
    顶点ID和权重值列表: list = field(default_factory=list)


@dataclass
class 烛龙网格:
    # 无默认参数需放前面
    名称: str = ""
    顶点个数: int = 0
    Loop总数: int = 0
    三角面数: int = 0
    顶点位置列表: list = field(default_factory=list)  # mathutils.Vector([x,y,z])
    顶点UV列表: list = field(default_factory=list)  # [[u,v],...]
    Loop列表: list = field(default_factory=list)
    材质: 烛龙材质 = field(default_factory=烛龙材质)
    顶点权重列表: list = field(default_factory=list)
    # [烛龙顶点组1, 烛龙顶点组2, ...] # 已处理成适合导入blender的形式，与blender28导入函数对接的列表
    顶点组列表: list = field(default_factory=list)

    # 古剑2
    ID: int = -1
    总网格ID: int = -1
    skinvert总数: int = -1
    skinvert索引: list = field(default_factory=list)

    # 古剑1
    总网格名称: str = ""
    父对象名称: str = ""
    骨骼ID列表: list = field(default_factory=list)
    权重值索引列表: list = field(default_factory=list)
    权重值列表: list = field(default_factory=list)

# @dataclass
# class 烛龙对象:
#     名称: str = ""
#     网格: 烛龙网格 = field(default_factory=烛龙网格)
# # 约定，对象的名称来源于网格的名称。此约定来源于blender一般操作中，一个对象仅拥有一个表格。objects与meshs属于不同的字典，故他们名字可相同，所以做相同处理、网格名称来源，解析文件自行处理。


@dataclass
class 烛龙位置帧:
    frame: int = -1
    location: list = field(default_factory=list)  # (x,y,z)


@dataclass
class 烛龙旋转帧:
    frame: int = -1
    rotation_quaternion: list = field(default_factory=list)  # (w,x,y,z)


@dataclass
class 烛龙matrix帧:
    frame: int = -1
    # mathutils.Quaternion([w,x,y,z])
    matrix: list = field(default_factory=list)


@dataclass
class 烛龙骨骼动作:  # 烛龙的单的骨骼关键帧集
    骨骼名称: str = ""
    位置帧列表: list = field(default_factory=list)
    旋转帧列表: list = field(default_factory=list)
    und_位置帧列表: list = field(default_factory=list)
    und_旋转帧列表: list = field(default_factory=list)

    # 计算
    matrix帧列表: list = field(default_factory=list)


@dataclass
class 烛龙动作文件:  # 烛龙的单的骨骼关键帧集
    名称: str = ""
    适用body文件名称: str = ""
    适用face文件名称: str = ""
    骨骼动作列表: list = field(default_factory=list)
    骨骼动作字典: dict = field(default_factory=dict)

    # 位置帧总数: int = 0
    # 旋转帧总数: int = 0


@dataclass
class 烛龙文件:
    网格列表: list = field(default_factory=list)
    骨架: 烛龙骨架 = field(default_factory=烛龙骨架)
    动作文件: 烛龙动作文件 = field(default_factory=烛龙动作文件)
