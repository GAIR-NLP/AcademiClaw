# Query 1: 立直麻将晋级条件计算器

## 【Query 描述】
### 背景
在多半庄规则下，由于顺位马点的出现，晋级条件随着不同的胡牌点数，
有很多变化，计算显得很困难。故需要设计一个计算器，对每个人的晋级条件进行总结，
方便选手进行决策。

### 需求：
你需要生成一个可执行文件，用于计算立直麻将的晋级条件。推荐使用java进行编程。
1. 输入信息： 四位选手的id，该半庄前总积分（pt），半庄当前状态（默认此时已到达了南场或者WRC规中已到达牌局最后一局，即如北家下庄即结束本场），选手目前点数，本场数，供托数。
2. 晋级条件：支持前1/2/3位晋级，计算条件。
3. 马点计算：至少需要支持M-League规则、A规、WRC规、最高位规的规则，后续可以增加更多规则。
相关规则请根据补充材料中的网页进行查询。（WRC规默认此时时间已到，本局为终局）
4. 结果生成：需要对每个选手自摸/从剩余三家荣胡/向剩余三家放铳所可以达成晋级的条件进行输出；
对每个选手由于横移动从而失去晋级条件的危险区间进行计算；
对流局的所有16种情况进行计算。
（注：不计算役满包牌、由于违反规则被罚点等过于特殊的情况）

## 【Context】
文件列表：
- 世界立直麻将大赛WRC规则 https://ooyamaneko.net/download/mahjong/riichi/WRC_Rules_2025_en.pdf 
- M-League规则 https://m-league.jp/about
- 日本职业麻将联盟竞技规则（简称A规） https://www.ma-jan.or.jp/guide/game_rule.html
- 最高位战日本立直麻将协会规则 https://saikouisen.com/about/rules/

测试用例详见 context 目录中的 `test_inputs.md`。


## 【交付要求】

1. 完整的Java源代码
2. 编译后的可执行jar文件
3. README.md，包含：
   - 编译和运行指南
   - 输入格式说明
   - 输出格式说明
   - 使用示例


## 样例

### 输入：

    当前亲家：北
    座次： 东 南 西 北
    名字： W1de Lemontruth 浅梦 kagayaki
    开始前总分 -46.5 63.1 9.8 -26.4
    当前分数 48200 13300 20000 18500
    晋级条件：2 
    规则：M-league
    供托：0 
    本场：0

### 输出：
    W1de晋级条件
    自摸	300・500以上
    =============================
    Lemontruth荣和	1000以上
    浅梦荣和	1000以上
    kagayaki荣和	1000以上
    =============================
    对Lemontruth放铳	16000以下
    对浅梦放铳	5800以下
    对kagayaki放铳	12000以下
    =============================
    被Lemontruth自摸	6000・12000以下
    被浅梦自摸	4000・8000以下
    被kagayaki亲家自摸	6000all以下

    W1de危险区间:
    Lemontruth点浅梦	24000以上会丢晋级资格
    Lemontruth点kagayaki	24000以上3倍役满以下会丢晋级资格
    浅梦点kagayaki	24000以上3倍役满以下会丢晋级资格
    kagayaki点Lemontruth	役满以上3倍役满以下会丢晋级资格
    kagayaki点浅梦	8000以上3倍役满以下会丢晋级资格

    Lemontruth晋级条件
    自摸	300・500以上
    =============================
    W1de荣和	1000以上
    浅梦荣和	1000以上
    kagayaki荣和	1000以上
    =============================
    对W1de放铳	6400以下
    对浅梦放铳	3200以下
    对浅梦放铳	役满
    对kagayaki放铳	18000以下
    =============================
    被W1de自摸	300・500以上
    被浅梦自摸	1300・2600以下
    被浅梦自摸	6000・12000以上
    被kagayaki亲家自摸	500all以上

    Lemontruth危险区间:

    浅梦晋级条件
    自摸	1500・2900以上
    =============================
    W1de荣和	6400以上
    Lemontruth荣和	3900以上
    kagayaki荣和	12000以上
    =============================
    =============================
    被Lemontruth自摸	役满以上

    浅梦危险区间:
    W1de点Lemontruth	12000以下会丢晋级资格
    W1de点kagayaki	3倍役满以下会丢晋级资格
    Lemontruth点W1de	6400以下会丢晋级资格
    Lemontruth点kagayaki	18000以下会丢晋级资格
    kagayaki点W1de	3倍役满以下会丢晋级资格
    kagayaki点Lemontruth	24000以下会丢晋级资格

    kagayaki晋级条件
    自摸	8000all以上
    =============================
    W1de荣和	18000以上
    Lemontruth荣和	24000以上
    浅梦荣和	36000以上
    =============================
    =============================

    kagayaki危险区间:
    W1de点Lemontruth	3倍役满以下会丢晋级资格
    W1de点浅梦	3倍役满以下会丢晋级资格
    Lemontruth点W1de	3倍役满以下会丢晋级资格
    Lemontruth点浅梦	3倍役满以下会丢晋级资格
    浅梦点W1de	3倍役满以下会丢晋级资格
    浅梦点Lemontruth	3倍役满以下会丢晋级资格

    【听牌分支一览】
    全员未听牌：[W1de, Lemontruth]晋级
    全员听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    W1de一人听牌：[W1de, Lemontruth]晋级
    Lemontruth一人听牌：[W1de, Lemontruth]晋级
    浅梦一人听牌：[W1de, Lemontruth]晋级
    kagayaki一人听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    W1de一人未听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    Lemontruth一人未听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    浅梦一人未听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    kagayaki一人未听牌：[W1de, Lemontruth]晋级
    W1de、Lemontruth听牌：[W1de, Lemontruth]晋级
    W1de、浅梦听牌：[W1de, Lemontruth]晋级
    W1de、kagayaki听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    Lemontruth、浅梦听牌：[W1de, Lemontruth]晋级
    Lemontruth、kagayaki听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续
    浅梦、kagayaki听牌：[W1de, Lemontruth]晋级，但kagayaki听牌而继续