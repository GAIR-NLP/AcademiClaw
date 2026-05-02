import random
from collections import Counter

# =====================
# 牌生成
# =====================

def generate_tiles():
    tiles = []
    for suit in ["B", "T", "M"]:
        for i in range(1, 10):
            tiles += [f"{suit}{i}"] * 4
    for honor in ["E", "S", "W", "N", "P", "F", "D"]:
        tiles += [honor] * 4
    random.shuffle(tiles)
    return tiles


# =====================
# 牌型判断
# =====================

def can_form_sets(counter):
    if not counter:
        return True

    tile = next(iter(counter))

    if counter[tile] >= 3:
        counter[tile] -= 3
        if counter[tile] == 0:
            del counter[tile]
        if can_form_sets(counter):
            return True
        counter[tile] = counter.get(tile, 0) + 3

    if len(tile) == 2 and tile[0] in "BTM":
        suit, num = tile[0], int(tile[1])
        seq = [f"{suit}{num+i}" for i in range(3)]
        if all(counter.get(t, 0) >= 1 for t in seq):
            for t in seq:
                counter[t] -= 1
                if counter[t] == 0:
                    del counter[t]
            if can_form_sets(counter):
                return True
            for t in seq:
                counter[t] = counter.get(t, 0) + 1

    return False


def is_complete_hand(all_tiles):
    counter = Counter(all_tiles)
    for tile in list(counter):
        if counter[tile] >= 2:
            counter[tile] -= 2
            if counter[tile] == 0:
                del counter[tile]
            if can_form_sets(counter):
                return True
            counter[tile] = counter.get(tile, 0) + 2
    return False

ALL_TILE_TYPES = (
    [f"{s}{i}" for s in "BTM" for i in range(1, 10)] +
    ["E", "S", "W", "N", "P", "F", "D"]
)

def is_tenpai_tiles(tiles):
    """给定 13 张牌，判断是否听牌"""
    for t in ALL_TILE_TYPES:
        if is_complete_hand(tiles + [t]):
            return True
    return False


def can_riichi(player):
    full_tiles = player.hand + [x for m in player.melds for x in m]

    # 枚举每一张可打的牌
    for discard in set(player.hand):
        test_tiles = full_tiles.copy()
        test_tiles.remove(discard)

        # 如果打掉这张后进入听牌 → 可立直
        if is_tenpai_tiles(test_tiles):
            return True

    return False



# =====================
# 玩家类
# =====================

class Player:
    def __init__(self, pid, human=False):
        self.pid = pid
        self.human = human
        self.hand = []
        self.discards = []
        self.melds = []
        self.riichi = False
        self.last_draw = None

    def draw(self, tile):
        self.hand.append(tile)
        self.last_draw = tile

    def discard(self, tile):
        self.hand.remove(tile)
        self.discards.append(tile)
        return tile


# =====================
# 游戏类
# =====================

class MahjongGame:
    def __init__(self):
        self.tiles = generate_tiles()
        self.players = [Player(0, True)] + [Player(i) for i in range(1, 4)]
        self.dealer = random.randint(0, 3)
        self.turn = self.dealer
        self.first_discard = True
        self.game_over = False
        self.init_deal()

    def init_deal(self):
        for _ in range(13):
            for p in self.players:
                p.draw(self.tiles.pop())
        self.players[self.dealer].draw(self.tiles.pop())

    def print_state(self):
        me = self.players[0]
        print("\n" + "=" * 60)
        print(f"你的手牌（{len(me.hand)}）：", " ".join(sorted(me.hand)))
        print("你的弃牌：", me.discards)
        print("你的碰/杠：", me.melds)
        print("-" * 60)
        for p in self.players[1:]:
            print(f"玩家{p.pid} | 立直:{p.riichi} | 碰/杠:{p.melds} | 弃牌:{p.discards}")
        print("=" * 60)

    def check_win(self, player, tile):
        tiles = player.hand + [x for m in player.melds for x in m] + [tile]
        return is_complete_hand(tiles)

    def human_discard(self):
        me = self.players[0]
        self.print_state()

        if can_riichi(me) and not me.riichi:
            ans = input("⭐ 你现在可以立直，是否立直？(y/n)：")
            if ans.lower() == "y":
                me.riichi = True
                print(">>> 你已立直！")

        while True:
            tile = input("请输入你要打出的牌：").strip()
            if tile in me.hand:
                if me.riichi and tile != me.last_draw:
                    print("❌ 立直后只能打出自己摸到的牌")
                    continue
                break
            print("❌ 无效出牌")

        out = me.discard(tile)
        print(f"你打出了：{out}")
        return out

    def react_to_discard(self, from_pid, tile):
        me = self.players[0]

        # 🔥 立直后：别人打出的牌可直接胡
        if me.riichi and self.check_win(me, tile):
            print(f"\n🎉 玩家 {from_pid} 打出 {tile}")
            print("🎉 你胡牌了！对局结束")
            self.game_over = True
            return True

        return False

    def step(self):
        if self.game_over:
            return

        p = self.players[self.turn]

        # ---------- 庄家首回合 ----------
        if self.first_discard and self.turn == self.dealer:
            self.first_discard = False

            if p.human:
                tile = self.human_discard()
            else:
                tile = p.discard(random.choice(p.hand))
                print(f"玩家{p.pid} 打出 {tile}")

            self.react_to_discard(p.pid, tile)

        # ---------- 普通回合 ----------
        else:
            if not self.tiles:
                print("【流局】牌山已空")
                self.game_over = True
                return

            draw = self.tiles.pop()
            p.draw(draw)

            # 🔥 自摸胡
            if p.human and p.riichi and self.check_win(p, draw):
                print(f"\n🎉 你摸到了 {draw}")
                print("🎉 你自摸胡牌！对局结束")
                self.game_over = True
                return

            if p.human:
                print(f"\n【你的回合】你摸到了 {draw}")
                tile = self.human_discard()
            else:
                tile = p.discard(random.choice(p.hand))
                print(f"玩家{p.pid} 打出 {tile}")

            self.react_to_discard(p.pid, tile)

        self.turn = (self.turn + 1) % 4


# =====================
# 主程序
# =====================

def main():
    game = MahjongGame()
    print(f"庄家是玩家 {game.dealer}，你是玩家 0")

    step = 0
    while not game.game_over:
        print(f"\n--- 回合 {step} ---")
        game.step()
        step += 1


if __name__ == "__main__":
    main()
