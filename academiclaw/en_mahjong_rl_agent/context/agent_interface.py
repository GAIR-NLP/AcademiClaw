"""
麻将智能体接口定义

这个文件定义了 MahjongAgent 基类，供智能体实现时继承。
评估环境会使用这个接口与智能体交互。
"""

from typing import Dict


class MahjongAgent:
    """麻将智能体基类"""
    
    def act(self, obs: Dict) -> Dict:
        """
        根据观测(observation)选择动作
        
        Parameters:
        -----------
        obs: Dict
            观测信息，包含:
            {
                "hand": List[str],          # 当前手牌，格式如 ["B1", "B2", "T3", "M5", "E", "S"]
                "melds": List[List[str]],   # 已碰/杠的牌组
                "riichi": bool,             # 当前是否已立直
                "last_draw": str or None,   # 最后摸到的牌
                "can_riichi": bool,         # 当前是否可以立直
                "other_players": List[Dict] # 其他玩家信息
            }
        
        Returns:
        --------
        action: Dict
            动作字典，必须包含:
            {
                "type": str,  # "discard" 或 "riichi_discard"
                "tile": str   # 要打出的牌，必须在 obs["hand"] 中
            }
        """
        raise NotImplementedError("子类必须实现 act 方法")
