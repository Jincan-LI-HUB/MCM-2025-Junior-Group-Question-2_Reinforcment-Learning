# core/game.py

class GameEnv:
    def __init__(self, first_player=0):
        """
        初始化游戏环境
        :param first_player: 0 表示 Alice 先手，1 表示 Bob 先手
        """
        self.chain = []
        self.scores = [0, 0]  # [Alice, Bob]
        self.player = first_player  # 关键：支持指定先手
        self.done = False
        self.legal_moves_cache = None

    def is_valid_move(self, x):
        if not self.chain: return True
        last = self.chain[-1]
        return x not in self.chain and (x % last == 0 or last % x == 0)

    def get_legal_moves(self):
        return [i for i in range(1, 101) if self.is_valid_move(i)]

    def is_terminal(self):
        return len(self.get_legal_moves()) == 0

    def make_move(self, x):
        if not self.is_valid_move(x):
            return None
        new_env = GameEnv()
        new_env.chain = self.chain + [x]
        new_env.scores = self.scores[:]
        new_env.scores[self.player] += x
        new_env.player = 1 - self.player
        new_env.done = new_env.is_terminal()
        return new_env

    def get_state_vec(self):
        used = [1 if i in self.chain else 0 for i in range(1, 101)]
        last = self.chain[-1] / 100.0 if self.chain else 0
        turn = self.player
        return used + [last, turn]

    def get_result(self):
        sa, sb = self.scores
        return sa, sb, "Alice" if sa > sb else "Bob" if sb > sa else "Tie"