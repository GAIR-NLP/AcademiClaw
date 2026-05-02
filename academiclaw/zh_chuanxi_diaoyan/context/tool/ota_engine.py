import json

class QunarService:
    """去哪儿网(Qunar) 酒店搜索开放接口 - 实践团专项访问版"""
    
    def __init__(self):
        # 实时模拟数据库：包含酒店、价格、专票支持及剩余房量
        self._db = {
    # --- 甘孜州 (Ganzi) ---
    "康定": [
        {"id": "KD01", "name": "康定情歌大酒店", "price": 380, "vat_invoice": True, "inventory": 12},
        {"id": "KD02", "name": "贡嘎青年旅舍", "price": 120, "vat_invoice": False, "inventory": 30}
    ],
    "雅江": [
        {"id": "YJ01", "name": "雅江驿站", "price": 260, "vat_invoice": True, "inventory": 5},
        {"id": "YJ02", "name": "康巴大酒店", "price": 420, "vat_invoice": True, "inventory": 10}
    ],
    "理塘": [
        {"id": "LT01", "name": "理塘丁真珍珠大酒店", "price": 480, "vat_invoice": True, "inventory": 2}, # 价格超标且库存紧
        {"id": "LT02", "name": "高城宾馆", "price": 240, "vat_invoice": True, "inventory": 15},
        {"id": "LT03", "name": "草原流浪者帐篷营地", "price": 180, "vat_invoice": False, "inventory": 20} # 无法报销
    ],
    "稻城": [
        {"id": "DC01", "name": "稻城亚丁悦榕庄", "price": 1350, "vat_invoice": True, "inventory": 10}, # 严重超标
        {"id": "DC02", "name": "圣地影像精品酒店", "price": 380, "vat_invoice": True, "inventory": 4},
        {"id": "DC03", "name": "香格里拉镇日松贡布酒店", "price": 420, "vat_invoice": True, "inventory": 8}
    ],
    "新都桥": [
        {"id": "XDQ01", "name": "摄影家天堂大酒店", "price": 350, "vat_invoice": True, "inventory": 6},
        {"id": "XDQ02", "name": "康定雅克国际青年旅舍", "price": 150, "vat_invoice": False, "inventory": 15}
    ],
    "色达": [
        {"id": "SD01", "name": "色达金马大酒店", "price": 360, "vat_invoice": True, "inventory": 10},
        {"id": "SD02", "name": "喇荣宾馆", "price": 280, "vat_invoice": False, "inventory": 5}
    ],
    "泸定": [
        {"id": "LD01", "name": "泸定桥精品酒店", "price": 260, "vat_invoice": True, "inventory": 12},
        {"id": "LD02", "name": "磨西古镇海螺沟饭店", "price": 320, "vat_invoice": True, "inventory": 8}
    ],

    # --- 阿坝州 (Aba) ---
    "四姑娘山": [ # 坐标通常显示为小金县或日隆镇
        {"id": "SGN01", "name": "四姑娘山长坪驿站", "price": 340, "vat_invoice": True, "inventory": 6},
        {"id": "SGN02", "name": "日隆镇阳光酒店", "price": 220, "vat_invoice": True, "inventory": 10},
        {"id": "SGN03", "name": "驴友之家民宿", "price": 140, "vat_invoice": False, "inventory": 20}
    ],
    "茂县": [
        {"id": "MX01", "name": "茂县国际饭店", "price": 320, "vat_invoice": True, "inventory": 15},
        {"id": "MX02", "name": "羌乡古寨民宿", "price": 180, "vat_invoice": True, "inventory": 5}
    ],
    "九寨沟": [
        {"id": "JZG01", "name": "九寨天堂洲际大饭店", "price": 980, "vat_invoice": True, "inventory": 20}, # 价格超标
        {"id": "JZG02", "name": "九寨沟喜来登酒店", "price": 650, "vat_invoice": True, "inventory": 12}, # 价格超标
        {"id": "JZG03", "name": "九寨人家客栈", "price": 190, "vat_invoice": True, "inventory": 10},
        {"id": "JZG04", "name": "沟口梦幻青年旅舍", "price": 90, "vat_invoice": False, "inventory": 40}
    ],
    "黄龙": [ # 通常指松潘县或川主寺镇
        {"id": "HL01", "name": "川主寺岷江源国际大酒店", "price": 380, "vat_invoice": True, "inventory": 10},
        {"id": "HL02", "name": "松潘古城藏家客栈", "price": 200, "vat_invoice": True, "inventory": 6}
    ],
    "马尔康": [
        {"id": "MEK01", "name": "马尔康嘉绒大酒店", "price": 350, "vat_invoice": True, "inventory": 8},
        {"id": "MEK02", "name": "阿坝州府宾馆", "price": 260, "vat_invoice": True, "inventory": 12}
    ]
}

    def query_hotels(self, city_name: str):
        """
        根据城市名检索当日实时房价与库存。
        注意：学校财务要求必须 vat_invoice == True 才能进行公费报销。
        """
        data = self._db.get(city_name, [])
        if not data:
            return json.dumps({"error": f"未找到{city_name}的酒店数据"}, ensure_ascii=False)
        return json.dumps({"status": "Success", "results": data}, ensure_ascii=False, indent=2)

# 使用示例：
# api = QunarService()
# print(api.query_hotels("理塘"))