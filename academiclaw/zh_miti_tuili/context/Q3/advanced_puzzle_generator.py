"""
Ultimate Logic Puzzle Generator - Chinese Puzzles
Extremely complex reasoning puzzles with Chinese descriptions
"""

import random
import json
import itertools
from typing import Dict, List, Any, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
import re

class StatementType(Enum):
    ALIBI = "alibi"
    WITNESS = "witness" 
    ACCUSATION = "accusation"
    FACT = "fact"
    KNOWLEDGE = "knowledge"
    PSYCHOLOGICAL = "psychological"
    EVIDENCE = "evidence"
    LOGICAL = "logical"

class RoleType(Enum):
    MURDERER = "murderer"
    ACCOMPLICE = "accomplice"
    INNOCENT = "innocent"
    LIAR = "liar"
    TRUTH_TELLER = "truth_teller"

@dataclass
class PuzzleConfig:
    difficulty: str = "hell"  # easy, medium, hard, hell
    num_suspects: int = 10  # 增加人数
    statements_per_person: int = 5  # 每人更多陈述
    num_global_constraints: int = 12  # 更多约束
    special_roles: int = 4  # 更多特殊身份
    require_unique_solution: bool = True
    min_reasoning_steps: int = 25  # 强制更多推理步骤

class UltimateChinesePuzzleGenerator:
    """生成极致复杂中文谜题的生成器"""
    
    def __init__(self, config: PuzzleConfig = None):
        self.config = config or PuzzleConfig()
        self._adjust_by_difficulty()
        
        # Chinese suspect names
        self.suspects_pool = [
            "欧阳锋", "慕容复", "令狐冲", "任盈盈", "张无忌", "赵敏",
            "郭靖", "黄蓉", "杨过", "小龙女", "段誉", "王语嫣",
            "虚竹", "梦姑", "乔峰", "阿朱", "韦小宝", "双儿",
            "胡斐", "程灵素", "狄云", "水笙", "石破天", "阿绣"
        ][:self.config.num_suspects]
        
        # Crime elements (in Chinese)
        self.crime_elements = {
            'murderer': self.suspects_pool.copy(),
            'weapon': ['青铜匕首', '鹤顶红毒药', '冰魄银针', '玄铁重剑', '金蚕蛊毒', 
                      '暴雨梨花针', '生死符', '化骨绵掌', '软猬甲', '金轮'],
            'location': ['藏经阁', '冰火岛', '桃花岛', '光明顶', '绝情谷', 
                        '燕子坞', '黑木崖', '侠客岛', '重阳宫', '古墓'],
            'time': ['子时(23:00-01:00)', '丑时(01:00-03:00)', '寅时(03:00-05:00)',
                    '卯时(05:00-07:00)', '辰时(07:00-09:00)', '巳时(09:00-11:00)',
                    '午时(11:00-13:00)', '未时(13:00-15:00)', '申时(15:00-17:00)'],
            'motive': ['复仇', '夺宝', '灭口', '情杀', '政变', '栽赃', '实验', '仪式', '练功']
        }
        
        # Enhanced statement templates in Chinese
        self.statement_templates = {
            StatementType.ALIBI: [
                "案发时我正在{location}与{person}切磋武艺，{witness}可以作证。",
                "{time}整，我在{location}修炼{skill}内功，全程未离开。",
                "整个{time_period}，我都在{location}照顾受伤的{person}，{evidence}可以证明。",
                "{location}的签到记录显示{time}我确实在那里，守卫{guard}看到了我。",
                "我与{person1}、{person2}一起在{location}饮酒，直到{time}才散。",
            ],
            
            StatementType.WITNESS: [
                "我亲眼看到{person}在{time}从{location}匆忙离开，手中拿着{item}。",
                "{time}左右，我听到{location}传来{sound}，随后看到{person}神色慌张地出来。",
                "我看到{person}拿着{item}进入了{location}，大约{time}才出来，身上有{mark}。",
                "{person}在{time}曾向我询问{location}的密道位置，行为可疑。",
                "案发前后，{person}多次在{location}附近徘徊，似乎在观察什么。",
            ],
            
            StatementType.ACCUSATION: [
                "{person}一直觊觎被害人的{treasure}，这可能是杀人动机。",
                "只有{person}精通{skill}，能够使用{weapon}这种特殊凶器作案。",
                "{person}与被害人是{relationship}关系，最近因{reason}矛盾激化。",
                "我亲眼看到{person}在案发前三天购买了{weapon}所需的{ingredient}。",
                "{person}曾扬言要杀死被害人，这话{hearer}也听到了。",
            ],
            
            StatementType.FACT: [
                "凶手使用的是{weapon}，因为现场发现了{evidence}。",
                "案发地点是{location1}，不是{location2}，{reason}可以证明。",
                "死亡时间在{time}前后，误差不超过{interval}。",
                "现场发现了{evidence1}和{evidence2}，指向凶手具备{skill1}和{skill2}。",
                "根据{method}分析，凶手的身份应该满足{condition}条件。",
            ],
            
            StatementType.KNOWLEDGE: [
                "要使用{weapon}作案，必须同时精通{skill1}和{skill2}。",
                "{location}在{time}会有{number}名守卫巡逻，外人难以进入。",
                "了解{location}密道的人不超过{number}个，分别是{person1}、{person2}、{person3}。",
                "{weapon}的制作方法只有{sect}的{position}才知道。",
                "在{time}进入{location}而不被发现，需要具备{skill}。",
            ],
            
            StatementType.PSYCHOLOGICAL: [
                "如果是{person}作案，一定会选择{time}这个时辰，这是他的习惯。",
                "使用{weapon}的人通常具有{character}性格特征，而{person}正是如此。",
                "{person}的习惯是在{time}前往{location}，这为作案提供了机会。",
                "以{person}的{character}性格，如果作案会选择{method}方式。",
                "{person}最近{behavior}，这与他平时的{habit}不符。",
            ],
            
            StatementType.EVIDENCE: [
                "现场留下的{evidence}与{person}之前使用的物品{detail}吻合。",
                "{location}发现的{mark}需要同时掌握{skill1}和{skill2}才能制造。",
                "根据{evidence}的分布，凶手的身高应该在{height_range}之间。",
                "{weapon}上检测到了{substance}，这与{person}的{background}有关联。",
                "被害人手中的{clue}指向{sect}的人，而{person}正是该派弟子。",
            ],
            
            StatementType.LOGICAL: [
                "如果{person1}说的是真话，那么{person2}一定在说谎。",
                "关于{weapon}的陈述{statement1}和{statement2}不可能同时为真。",
                "要么{person}是无辜的，要么{weapon}不是真正的凶器。",
                "如果案发在{location}，那么{person}的不在场证明成立当且仅当{condition}。",
                "{person1}和{person2}的证词互相矛盾，至少有一人在说谎。",
            ]
        }
        
        # Ultimate constraint templates in Chinese
        self.constraint_templates = [
            # 基础计数约束
            "所有人中，恰好有{number1}个人说的全是真话，{number2}个人说的全是假话。",
            "关于{element}的陈述中，真话数量是假话数量的{number}倍。",
            
            # 身份约束
            "凶手说的所有陈述都是假的，但关于{misc}的陈述除外。",
            "帮凶的陈述中至少有一条关于{element1}和一条关于{element2}的陈述为真。",
            "无辜者不会做出虚假的指控，但可能在其他陈述上说谎。",
            
            # 逻辑关系约束
            "如果{person1}的第一条陈述为真，那么他的第三条陈述一定为假，反之亦然。",
            "{person1}和{person2}的陈述真假情况完全相反。",
            "关于{location}的陈述，如果{person1}说的是真话，那么{person2}说的就是假话，且{person3}说的是真话。",
            
            # 复合约束
            "要么{person1}全是真话，要么{person2}全是假话，但两人不可能同时满足自己的情况。",
            "如果{element1}是{value1}，那么关于{element2}的陈述中最多有{number}条为真。",
            
            # 多层嵌套约束
            "{person1}的陈述真假情况与{person2}的陈述真假情况相同，当且仅当{element}是{value}。",
            "关于凶器的真话数量等于关于地点的假话数量，且等于关于时间的真话数量加{number}。",
            "所有提到{person}的陈述中，真话的数量是奇数，且这些陈述涉及{element}。",
            
            # 地狱级约束
            "如果{person1}说真话，则{person2}说假话；如果{person1}说假话，则{person3}说真话。且{person4}的情况与{person2}相反。",
            "关于作案时间的陈述，真话数量与关于凶器的陈述真话数量之和为{number}，且与关于地点的假话数量之差为{difference}。",
            "每个人的第{number1}条陈述的真假情况形成一个{pattern}序列，第{number2}条陈述形成相反的序列。",
            "如果{condition1}，则{conclusion1}；否则如果{condition2}，则{conclusion2}；否则{conclusion3}。",
            
            # 循环依赖约束
            "{person1}的证词可信当且仅当{person2}的证词不可信，而{person2}的证词可信当且仅当{person3}的证词不可信，{person3}的证词可信当且仅当{person1}的证词不可信。",
            "关于{element1}的真话数量比关于{element2}的假话数量多{number1}，比关于{element3}的真话数量少{number2}。",
        ]
        
        # Helper vocabularies in Chinese
        self.sounds = ['打斗声', '惨叫声', '破碎声', '脚步声', '对话声', '兵器碰撞声']
        self.items = ['秘籍', '宝剑', '药瓶', '地图', '玉佩', '暗器囊', '毒经', '信函']
        self.evidences = ['黑色布条', '血迹', '特殊指纹', '独特鞋印', '金色发丝', '紫色毒粉', '玉佩碎片']
        self.characters = ['谨慎', '冲动', '狡猾', '直接', '多疑', '大胆', '细心', '鲁莽']
        self.sects = ['少林', '武当', '峨眉', '丐帮', '明教', '日月神教', '华山派', '昆仑派']
        self.relationships = ['师徒', '父子', '兄弟', '夫妻', '主仆', '盟友', '仇敌', '同门', '情敌']
        self.skills = ['用毒', '暗器', '剑法', '掌法', '轻功', '医术', '机关', '易容', '内功', '点穴']
        self.treasures = ['九阴真经', '屠龙刀', '倚天剑', '武穆遗书', '乾坤大挪移心法', '六脉神剑图谱']
        
    def _adjust_by_difficulty(self):
        """根据难度调整参数"""
        if self.config.difficulty == "hell":
            self.config.num_suspects = 12
            self.config.statements_per_person = 6
            self.config.num_global_constraints = 15
            self.config.special_roles = 5
            self.config.min_reasoning_steps = 30
        elif self.config.difficulty == "hard":
            self.config.num_suspects = 10
            self.config.statements_per_person = 5
            self.config.num_global_constraints = 12
            self.config.special_roles = 4
            self.config.min_reasoning_steps = 25
        elif self.config.difficulty == "medium":
            self.config.num_suspects = 8
            self.config.statements_per_person = 4
            self.config.num_global_constraints = 8
            self.config.special_roles = 3
            self.config.min_reasoning_steps = 15
        else:  # easy
            self.config.num_suspects = 6
            self.config.statements_per_person = 3
            self.config.num_global_constraints = 5
            self.config.special_roles = 2
            self.config.min_reasoning_steps = 8

    def generate_random_crime(self):
        """生成随机犯罪事实"""
        crime = {}
        for element_type, options in self.crime_elements.items():
            crime[element_type] = random.choice(options)
        return crime
    
    def get_random_element(self, element_type, exclude=None):
        """随机获取元素"""
        exclude = exclude or []
        pool = self.crime_elements.get(element_type, [])
        if not pool:
            pool = getattr(self, f"{element_type}s", [])
        
        available = [e for e in pool if e not in exclude]
        return random.choice(available) if available else random.choice(pool)
    
    def generate_statement(self, speaker, stmt_type, crime_facts, other_suspects):
        """生成单条中文陈述"""
        template = random.choice(self.statement_templates[stmt_type])
        
        # 准备替换词
        replacements = {}
        
        # 人物相关
        if '{person}' in template:
            replacements['{person}'] = random.choice(other_suspects)
        if '{person1}' in template and '{person2}' in template:
            p1, p2 = random.sample(other_suspects, 2)
            replacements['{person1}'] = p1
            replacements['{person2}'] = p2
        if '{person3}' in template:
            p3 = random.choice([p for p in other_suspects if p not in replacements.values()])
            replacements['{person3}'] = p3
            
        # 犯罪元素
        crime_mapping = {
            '{weapon}': ('weapon', crime_facts.get('weapon')),
            '{location}': ('location', crime_facts.get('location')),
            '{location1}': ('location', crime_facts.get('location')),
            '{location2}': ('location', self.get_random_element('location', [crime_facts.get('location')])),
            '{time}': ('time', crime_facts.get('time')),
            '{motive}': ('motive', crime_facts.get('motive')),
        }
        
        for placeholder, (elem_type, true_value) in crime_mapping.items():
            if placeholder in template:
                # 70%概率用正确答案，30%用错误答案增加干扰
                if random.random() < 0.7:
                    replacements[placeholder] = true_value
                else:
                    wrong = self.get_random_element(elem_type, [true_value])
                    replacements[placeholder] = wrong
        
        # 其他词汇
        other_placeholders = {
            '{witness}': random.choice(self.suspects_pool),
            '{guard}': random.choice(['张三', '李四', '王五', '赵六']),
            '{item}': random.choice(self.items),
            '{sound}': random.choice(self.sounds),
            '{mark}': random.choice(['血迹', '污泥', '香气', '药渍']),
            '{treasure}': random.choice(self.treasures),
            '{skill}': random.choice(self.skills),
            '{skill1}': random.choice(self.skills),
            '{skill2}': random.choice([s for s in self.skills if s != replacements.get('{skill1}')]),
            '{relationship}': random.choice(self.relationships),
            '{reason}': random.choice(['金钱', '权力', '感情', '秘籍']),
            '{ingredient}': random.choice(['毒草', '金属', '药材', '矿石']),
            '{hearer}': random.choice(self.suspects_pool),
            '{evidence}': random.choice(self.evidences),
            '{evidence1}': random.choice(self.evidences),
            '{evidence2}': random.choice([e for e in self.evidences if e != replacements.get('{evidence1}', '')]),
            '{interval}': random.choice(['一刻钟', '半个时辰', '一炷香时间']),
            '{method}': random.choice(['血迹分析', '伤口检验', '毒理检测', '痕迹鉴定']),
            '{condition}': random.choice(['精通轻功', '熟悉地形', '内有接应', '使用密道']),
            '{number}': random.choice(['二', '三', '四', '五']),
            '{sect}': random.choice(self.sects),
            '{position}': random.choice(['掌门', '长老', '护法', '堂主']),
            '{character}': random.choice(self.characters),
            '{behavior}': random.choice(['心神不宁', '行踪诡秘', '大肆挥霍', '闭门不出']),
            '{habit}': random.choice(['作风', '习惯', '性格', '品行']),
            '{detail}': random.choice(['完全一致', '十分相似', '出自同源', '工艺相同']),
            '{height_range}': random.choice(['五尺到五尺五寸', '五尺五寸到六尺', '六尺以上']),
            '{substance}': random.choice(['西域香料', '唐门毒药', '苗疆蛊虫', '特殊花粉']),
            '{background}': random.choice(['出身', '师承', '经历', '爱好']),
            '{clue}': random.choice(['布片', '头发', '玉佩', '纸张']),
            '{time_period}': random.choice(['子时到丑时', '寅时到卯时', '整个晚上']),
        }
        
        for ph, value in other_placeholders.items():
            if ph in template and ph not in replacements:
                replacements[ph] = value
        
        # 应用替换
        statement = template
        for placeholder, value in replacements.items():
            statement = statement.replace(placeholder, value)
            
        return statement
    
    def assign_roles_and_truth(self, suspects, crime_facts):
        """分配角色和真值 - 修复版本"""
        roles = {}
        truth_values = {}
        
        # 使用 crime_facts 中的真正凶手
        murderer = crime_facts['murderer']
        if murderer not in suspects:
            # 如果凶手不在嫌疑人列表中，选择一名嫌疑人作为凶手
            murderer = random.choice(suspects)
            crime_facts['murderer'] = murderer  # 更新 crime_facts
        
        roles[murderer] = RoleType.MURDERER
        
        # 选择帮凶（不能是凶手）
        accomplice_pool = [s for s in suspects if s != murderer]
        accomplice = random.choice(accomplice_pool) if accomplice_pool else murderer
        roles[accomplice] = RoleType.ACCOMPLICE
        
        # 选择说谎者（不能是凶手或帮凶）
        liar_pool = [s for s in suspects if s not in [murderer, accomplice]]
        liar = random.choice(liar_pool) if liar_pool else random.choice(suspects)
        roles[liar] = RoleType.LIAR
        
        # 选择说真话者（不能是凶手、帮凶或说谎者）
        truth_teller_pool = [s for s in suspects if s not in roles]
        truth_teller = random.choice(truth_teller_pool) if truth_teller_pool else random.choice(suspects)
        roles[truth_teller] = RoleType.TRUTH_TELLER
        
        # 其余为无辜者
        for suspect in suspects:
            if suspect not in roles:
                roles[suspect] = RoleType.INNOCENT
        
        # 根据角色分配真值
        for suspect in suspects:
            stmt_truths = []
            role = roles[suspect]
            
            for _ in range(self.config.statements_per_person):
                if role == RoleType.MURDERER:
                    # 凶手大部分说谎，但可能说少量真话以迷惑
                    stmt_truths.append(random.random() > 0.85)  # 85% 说谎
                elif role == RoleType.ACCOMPLICE:
                    # 帮凶混合说真话和假话
                    stmt_truths.append(random.random() > 0.5)  # 50% 说真话
                elif role == RoleType.LIAR:
                    # 说谎者大部分说谎
                    stmt_truths.append(random.random() > 0.15)  # 85% 说谎
                elif role == RoleType.TRUTH_TELLER:
                    # 说真话者大部分说真话
                    stmt_truths.append(random.random() > 0.85)  # 85% 说真话
                else:  # INNOCENT
                    # 无辜者大部分说真话，但可能因误解而说假话
                    stmt_truths.append(random.random() > 0.3)  # 70% 说真话
            
            truth_values[suspect] = stmt_truths
        
        return roles, truth_values, crime_facts  # 返回更新后的 crime_facts
    
    def generate_statements_for_all(self, suspects, crime_facts):
        """为所有人生成陈述"""
        statements = {}
        all_statement_objs = []  # 保存完整陈述对象
        
        for suspect in suspects:
            suspect_statements = []
            other_suspects = [s for s in suspects if s != suspect]
            
            # 确保陈述类型多样
            stmt_types = random.sample(list(StatementType), 
                                      min(self.config.statements_per_person, len(StatementType)))
            
            # 如果类型不够，补充随机类型
            while len(stmt_types) < self.config.statements_per_person:
                stmt_types.append(random.choice(list(StatementType)))
            
            for stmt_type in stmt_types:
                stmt_text = self.generate_statement(suspect, stmt_type, crime_facts, other_suspects)
                suspect_statements.append(stmt_text)
                
                # 保存陈述对象
                all_statement_objs.append({
                    'speaker': suspect,
                    'type': stmt_type.value,
                    'text': stmt_text,
                    'mentions': self.extract_mentions(stmt_text)
                })
            
            statements[suspect] = suspect_statements
        
        return statements, all_statement_objs
    
    def extract_mentions(self, text):
        """提取陈述中提及的元素"""
        mentions = {
            'suspects': [],
            'weapons': [],
            'locations': [],
            'times': [],
            'motives': []
        }
        
        # 检查提及的嫌疑人
        for suspect in self.suspects_pool:
            if suspect in text:
                mentions['suspects'].append(suspect)
        
        # 检查提及的犯罪元素
        for element_type, values in self.crime_elements.items():
            if element_type != 'murderer':
                for value in values:
                    if value in text:
                        mentions[f'{element_type}s'].append(value)
        
        return mentions
    
    def generate_constraints(self, suspects, statements, truth_values, crime_facts):
        """生成全局约束 - 修复版本"""
        constraints = []
        
        # 1. 真话人数约束
        truth_tellers = [s for s, truths in truth_values.items() if any(truths)]
        num_truth_tellers = len(truth_tellers)
        num_liars = len(suspects) - num_truth_tellers
        
        constraints.append(f"所有人中，恰好有{num_truth_tellers}个人至少说了一句真话，{num_liars}个人可能全在说谎。")
        
        # 2. 凶手说谎约束 - 直接使用 crime_facts 中的凶手
        murderer = crime_facts['murderer']
        constraints.append(f"凶手说的所有陈述都是假的，但关于作案动机的陈述可能是例外。")
        
        # ... 其余约束生成保持不变 ...
        
        # 3. 复杂逻辑约束
        if len(suspects) >= 4:
            p1, p2, p3, p4 = random.sample(suspects, 4)
            constraints.append(f"如果{p1}说的全是真话，那么{p2}一定在说谎；如果{p1}在说谎，那么{p3}说的全是真话。且{p4}的情况与{p2}相反。")
        
        # 4. 计数约束 - 修复这里
        element = random.choice(['凶器', '地点', '时间', '动机'])
        count = random.randint(1, 3)
        constraints.append(f"关于{element}的陈述中，真话数量是假话数量的{count}倍。")
        
        # 5. 身份关系约束
        p1, p2 = random.sample(suspects, 2)
        constraints.append(f"{p1}和{p2}的陈述真假情况完全相反。")
        
        # 6. 条件约束
        location = crime_facts['location']
        p1, p2 = random.sample(suspects, 2)
        constraints.append(f"关于{location}的陈述，如果{p1}说的是真话，那么{p2}说的就是假话。")
        
        # 7. 复合约束
        p1, p2 = random.sample(suspects, 2)
        constraints.append(f"要么{p1}说的全是真话，要么{p2}说的全是假话，但两人不可能同时满足自己的情况。")
        
        # 8. 元素关联约束
        constraints.append("关于凶器的真话数量等于关于地点的假话数量。")
        
        # 9. 模式约束
        constraints.append("每个人的第三条陈述的真假情况形成一个特定的模式。")
        
        # 10. 循环依赖约束（地狱级）
        if len(suspects) >= 3:
            p1, p2, p3 = random.sample(suspects, 3)
            constraints.append(f"{p1}的证词可信当且仅当{p2}的证词不可信，而{p2}的证词可信当且仅当{p3}的证词不可信。")
        
        # 11. 生成剩余的约束 - 需要完全替换占位符
        while len(constraints) < self.config.num_global_constraints:
            template = random.choice(self.constraint_templates)
            
            # 为模板准备替换值
            replacements = {}
            
            # 数字替换
            for num_ph in ['{number1}', '{number2}', '{number}', '{difference}']:
                if num_ph in template:
                    replacements[num_ph] = str(random.randint(1, 5))
            
            # 人物替换
            person_placeholders = ['{person1}', '{person2}', '{person3}', '{person4}', '{person}']
            used_persons = []
            for ph in person_placeholders:
                if ph in template:
                    available = [p for p in suspects if p not in used_persons]
                    if available:
                        chosen = random.choice(available)
                        replacements[ph] = chosen
                        used_persons.append(chosen)
                    else:
                        replacements[ph] = random.choice(suspects)
            
            # 元素替换
            element_options = ['凶器', '地点', '时间', '动机']
            element_placeholders = ['{element}', '{element1}', '{element2}', '{element3}', '{misc}']
            for ph in element_placeholders:
                if ph in template:
                    replacements[ph] = random.choice(element_options)
            
            # 条件替换 - 处理条件占位符
            if '{condition1}' in template or '{condition2}' in template:
                conditions = [
                    f"{random.choice(suspects)}的陈述为真",
                    f"凶器是{random.choice(self.crime_elements['weapon'])}",
                    f"案发地点是{random.choice(self.crime_elements['location'])}",
                    f"作案时间是{random.choice(self.crime_elements['time'])}",
                    f"至少{random.randint(2,4)}个人说真话"
                ]
                for ph in ['{condition1}', '{condition2}']:
                    if ph in template:
                        replacements[ph] = random.choice(conditions)
            
            # 结论替换
            if '{conclusion1}' in template or '{conclusion2}' in template or '{conclusion3}' in template:
                conclusions = [
                    f"{random.choice(suspects)}是凶手",
                    f"凶器是{random.choice(self.crime_elements['weapon'])}",
                    f"{random.choice(suspects)}和{random.choice(suspects)}中至少一人在说谎",
                    f"关于地点的陈述中最多有{random.randint(1,3)}条为真",
                    f"{random.choice(suspects)}的无辜的"
                ]
                for ph in ['{conclusion1}', '{conclusion2}', '{conclusion3}']:
                    if ph in template:
                        replacements[ph] = random.choice(conclusions)
            
            # 模式替换
            if '{pattern}' in template:
                patterns = ['真假交替', '前真后假', '前假后真', '全真', '全假']
                replacements['{pattern}'] = random.choice(patterns)
            
            # 值替换
            if '{value1}' in template:
                element_type = replacements.get('{element1}', random.choice(element_options))
                if element_type == '凶器':
                    replacements['{value1}'] = random.choice(self.crime_elements['weapon'])
                elif element_type == '地点':
                    replacements['{value1}'] = random.choice(self.crime_elements['location'])
                elif element_type == '时间':
                    replacements['{value1}'] = random.choice(self.crime_elements['time'])
                elif element_type == '动机':
                    replacements['{value1}'] = random.choice(self.crime_elements['motive'])
                else:
                    replacements['{value1}'] = random.choice(self.crime_elements['weapon'])
            
            # 应用所有替换
            constraint = template
            for placeholder, value in replacements.items():
                constraint = constraint.replace(placeholder, value)
            
            # 确保没有未替换的占位符
            if '{' not in constraint:
                constraints.append(constraint)
            else:
                # 如果还有未替换的占位符，使用一个简单的约束
                simple_constraints = [
                    f"关于{random.choice(element_options)}的陈述，真话数量比假话数量多{random.randint(1,3)}。",
                    f"{random.choice(suspects)}和{random.choice(suspects)}的陈述真假情况恰好相反。",
                    f"所有提到{random.choice(suspects)}的陈述中，真话的数量是{random.choice(['奇数', '偶数'])}。"
                ]
                constraints.append(random.choice(simple_constraints))
        
        return constraints[:self.config.num_global_constraints]
    
    def calculate_difficulty_score(self, puzzle):
        """计算谜题难度分数"""
        score = 0
        
        # 基于嫌疑人数量
        score += len(puzzle['suspects']) * 3
        
        # 基于陈述总数
        total_statements = sum(len(stmts) for stmts in puzzle['statements'].values())
        score += total_statements * 2
        
        # 基于约束数量
        score += len(puzzle['constraints']) * 5
        
        # 基于陈述类型多样性
        unique_types = set()
        for stmt_obj in puzzle.get('statement_objects', []):
            unique_types.add(stmt_obj['type'])
        score += len(unique_types) * 4
        
        # 基于约束复杂度
        complex_keywords = ['当且仅当', '互为矛盾', '循环', '模式', '序列', '奇数', '偶数', '倍数']
        for constraint in puzzle['constraints']:
            if any(keyword in constraint for keyword in complex_keywords):
                score += 3
        
        return score
    
    def generate_puzzle(self, puzzle_id=1):
        """生成单个谜题 - 修复版本"""
        max_attempts = 100
        for attempt in range(max_attempts):
            try:
                # 生成犯罪事实
                crime_facts = self.generate_random_crime()
                
                # 选择嫌疑人
                selected_suspects = random.sample(
                    self.suspects_pool, 
                    min(self.config.num_suspects, len(self.suspects_pool))
                )
                
                # 确保凶手在选中的人中 - 修复逻辑
                if crime_facts['murderer'] not in selected_suspects:
                    # 用凶手替换随机一个嫌疑人
                    replace_index = random.randint(0, len(selected_suspects)-1)
                    selected_suspects[replace_index] = crime_facts['murderer']
                
                # 分配角色和真值 - 接受返回的 crime_facts
                roles, truth_values, updated_crime_facts = self.assign_roles_and_truth(selected_suspects, crime_facts)
                crime_facts = updated_crime_facts  # 使用更新后的 crime_facts
                
                # 生成陈述
                statements, statement_objs = self.generate_statements_for_all(selected_suspects, crime_facts)
                
                # 生成约束 - 注意传入正确的 roles
                constraints = self.generate_constraints(selected_suspects, statements, truth_values, crime_facts)
                
                # 构建谜题
                puzzle = {
                    'id': puzzle_id,
                    'difficulty': self.config.difficulty,
                    'suspects': selected_suspects,
                    'crime_elements': {
                        'weapons': self.crime_elements['weapon'],
                        'locations': self.crime_elements['location'],
                        'times': self.crime_elements['time'],
                        'motives': self.crime_elements['motive']
                    },
                    'statements': statements,
                    'statement_objects': statement_objs,
                    'constraints': constraints,
                    'hidden_data': {
                        'crime_facts': crime_facts,  # 使用更新后的 crime_facts
                        'roles': {s: r.value for s, r in roles.items()},
                        'truth_values': truth_values
                    },
                    'difficulty_score': 0,
                    'expected_solution_steps': self.config.min_reasoning_steps + random.randint(5, 15)
                }
                
                # 验证一致性
                if not self.validate_puzzle_consistency(puzzle):
                    continue
                    
                # 计算难度分数
                puzzle['difficulty_score'] = self.calculate_difficulty_score(puzzle)
                
                # 验证基本合理性
                if self.validate_puzzle(puzzle):
                    print(f"成功生成谜题 #{puzzle_id} (尝试{attempt+1}次)")
                    return puzzle
                else:
                    continue
                    
            except Exception as e:
                print(f"尝试 {attempt+1} 失败: {e}")
                continue
        
        raise Exception(f"生成谜题失败，已达到最大尝试次数 {max_attempts}")
    
    def validate_puzzle_consistency(self, puzzle):
        """验证谜题内部一致性"""
        crime_facts = puzzle['hidden_data']['crime_facts']
        roles = puzzle['hidden_data']['roles']
        
        # 1. 检查凶手是否在嫌疑人中
        if crime_facts['murderer'] not in puzzle['suspects']:
            print(f"凶手 {crime_facts['murderer']} 不在嫌疑人列表中")
            return False
        
        # 2. 检查 roles 中的凶手与 crime_facts 一致
        for suspect, role in roles.items():
            if role == 'murderer' and suspect != crime_facts['murderer']:
                print(f"矛盾: {suspect} 被标记为凶手，但 crime_facts 中的凶手是 {crime_facts['murderer']}")
                return False
        
        # 3. 检查是否只有一个凶手
        murderer_count = sum(1 for role in roles.values() if role == 'murderer')
        if murderer_count != 1:
            print(f"凶手数量不正确: {murderer_count}")
            return False
        
        # 4. 检查所有嫌疑人都有角色
        if len(roles) != len(puzzle['suspects']):
            print(f"角色数量 {len(roles)} 与嫌疑人数量 {len(puzzle['suspects'])} 不一致")
            return False
        
        return True
    def validate_puzzle(self, puzzle):
        """验证谜题基本合理性"""
        # 检查陈述数量
        total_statements = sum(len(stmts) for stmts in puzzle['statements'].values())
        if total_statements < len(puzzle['suspects']) * 3:
            return False
        
        # 检查约束数量
        if len(puzzle['constraints']) < self.config.num_global_constraints * 0.8:
            return False
        
        # 检查是否所有嫌疑人都被提及
        all_mentioned = set()
        for stmt_obj in puzzle['statement_objects']:
            all_mentioned.update(stmt_obj['mentions']['suspects'])
        
        if not all(s in all_mentioned for s in puzzle['suspects']):
            return False
        
        return True
    
    def generate_puzzle_library(self, num_puzzles=10, output_file='ultimate_chinese_puzzles.json'):
        """生成谜题库"""
        library = []
        
        print(f"开始生成 {num_puzzles} 个极致复杂中文逻辑谜题...")
        print("=" * 60)
        
        for i in range(1, num_puzzles + 1):
            try:
                puzzle = self.generate_puzzle(puzzle_id=i)
                library.append(puzzle)
                
                print(f"✓ 谜题 #{i:03d}: {len(puzzle['suspects'])}人, {sum(len(s) for s in puzzle['statements'].values())}条陈述, "
                      f"{len(puzzle['constraints'])}条约束, 难度分数: {puzzle['difficulty_score']}")
                
                # 显示第一个谜题作为示例
                if i == 1:
                    self.print_puzzle_example(puzzle)
                    
            except Exception as e:
                print(f"✗ 谜题 #{i} 生成失败: {e}")
        
        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=2, ensure_ascii=False)
        
        print(f"\n生成完成！成功生成 {len(library)}/{num_puzzles} 个谜题")
        print(f"已保存至: {output_file}")
        
        # 显示统计信息
        self.print_statistics(library)
        
        return library
    
    def print_puzzle_example(self, puzzle):
        """打印谜题示例"""
        print("\n" + "="*60)
        print("极致复杂逻辑谜题示例")
        print("="*60)
        
        print(f"\n案件背景：")
        print(f"武林盟主在{puzzle['hidden_data']['crime_facts']['location']}被杀害，")
        print(f"涉及{len(puzzle['suspects'])}名嫌疑人，各有复杂背景和动机。")
        
        print(f"\n嫌疑人名单：")
        for i, suspect in enumerate(puzzle['suspects'], 1):
            print(f"  {i:2d}. {suspect}")
        
        print(f"\n犯罪元素选项：")
        print(f"  凶器可能：{', '.join(puzzle['crime_elements']['weapons'][:5])}...")
        print(f"  地点可能：{', '.join(puzzle['crime_elements']['locations'][:5])}...")
        print(f"  时间可能：{', '.join(puzzle['crime_elements']['times'][:3])}...")
        print(f"  动机可能：{', '.join(puzzle['crime_elements']['motives'])}")
        
        print(f"\n每个人的陈述（共{sum(len(s) for s in puzzle['statements'].values())}条）：")
        for suspect, statements in puzzle['statements'].items():
            print(f"\n{suspect}:")
            for i, stmt in enumerate(statements[:3], 1):  # 只显示前3条
                print(f"  {i}. {stmt}")
            if len(statements) > 3:
                print(f"  ... 还有{len(statements)-3}条陈述")
        
        print(f"\n全局约束条件（共{len(puzzle['constraints'])}条）：")
        for i, constraint in enumerate(puzzle['constraints'][:8], 1):  # 只显示前8条
            print(f"  {i}. {constraint}")
        if len(puzzle['constraints']) > 8:
            print(f"  ... 还有{len(puzzle['constraints'])-8}条约束")
        
        print(f"\n推理任务：")
        print("1. 判断每个人的每条陈述是真是假")
        print("2. 根据约束条件推导凶手的身份")
        print("3. 确定凶器、地点、时间和动机")
        print("4. 识别帮凶、说谎者等特殊角色")
        print("5. 确保所有约束条件同时满足")
        
        print(f"\n预期推理步骤：{puzzle['expected_solution_steps']}+ 步")
        print(f"难度分数：{puzzle['difficulty_score']}/150")
        print("="*60)
    
    def print_statistics(self, library):
        """打印统计信息"""
        if not library:
            return
        
        print("\n" + "="*60)
        print("谜题库统计信息")
        print("="*60)
        
        # 基本统计
        total_puzzles = len(library)
        avg_suspects = sum(len(p['suspects']) for p in library) / total_puzzles
        avg_statements = sum(sum(len(s) for s in p['statements'].values()) for p in library) / total_puzzles
        avg_constraints = sum(len(p['constraints']) for p in library) / total_puzzles
        avg_difficulty = sum(p['difficulty_score'] for p in library) / total_puzzles
        
        print(f"谜题总数：{total_puzzles}")
        print(f"平均嫌疑人：{avg_suspects:.1f} 人")
        print(f"平均陈述数：{avg_statements:.1f} 条")
        print(f"平均约束数：{avg_constraints:.1f} 条")
        print(f"平均难度分：{avg_difficulty:.1f}")
        
        # 难度分布
        diff_levels = {'简单': 0, '中等': 0, '困难': 0, '地狱': 0}
        for puzzle in library:
            score = puzzle['difficulty_score']
            if score < 50:
                diff_levels['简单'] += 1
            elif score < 80:
                diff_levels['中等'] += 1
            elif score < 110:
                diff_levels['困难'] += 1
            else:
                diff_levels['地狱'] += 1
        
        print(f"\n难度分布：")
        for level, count in diff_levels.items():
            if count > 0:
                percentage = (count / total_puzzles) * 100
                print(f"  {level}: {count}个 ({percentage:.1f}%)")
        
        print("="*60)

# 使用示例
if __name__ == "__main__":
    print("极致复杂中文逻辑谜题生成器")
    print("=" * 60)
    
    # 配置地狱级难度
    config = PuzzleConfig(
        difficulty="hell",
        num_suspects=12,
        statements_per_person=6,
        num_global_constraints=15,
        special_roles=5,
        require_unique_solution=True,
        min_reasoning_steps=25
    )
    
    # 创建生成器
    generator = UltimateChinesePuzzleGenerator(config)
    
    # 生成单个示例
    print("\n生成示例谜题...")
    example = generator.generate_puzzle(puzzle_id=0)
    
    # 显示示例
    generator.print_puzzle_example(example)
    
    # 生成完整谜题库
    print("\n" + "="*60)
    response = input("是否生成完整谜题库？(y/n): ")
    
    if response.lower() == 'y':
        num = input("生成数量 (默认10): ")
        try:
            num_puzzles = int(num) if num.strip() else 10
        except:
            num_puzzles = 10
        
        generator.generate_puzzle_library(num_puzzles)
    
    print("\n" + "="*60)
    print("系统特点：")
    print("1. 12+嫌疑人，每人6+条陈述，15+条复杂约束")
    print("2. 陈述类型多样：不在场证明、目击证词、指控、事实、知识、心理分析等")
    print("3. 多层嵌套约束，包含循环依赖、条件逻辑、计数关系")
    print("4. 需要同时判断陈述真假、角色身份、犯罪事实")
    print("5. 人类解决时间预计：1-3小时/题")
    print("="*60)