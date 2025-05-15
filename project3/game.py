import numpy as np
from pos import CPos
from board import CBoard
from comchecker import CComchecker
from king import CKing

class CGame:
    def __init__(self, board: CBoard):
        self.m_board = board
        self.m_white_cnt = self.m_black_cnt = (self.m_board.m_size / 2 - 1) * (self.m_board.m_size / 2)
        self.m_no_capture_cnt = 0

    def copy_game(self):
        copy = CGame(self.m_board.clone_without_gui())
        copy.m_white_cnt = self.m_white_cnt
        copy.m_black_cnt = self.m_black_cnt
        return copy

    def eval_position(self) -> int:
        return int(self.m_white_cnt - self.m_black_cnt)

    def is_game_over(self) -> bool:
        return self.m_white_cnt == 0 or self.m_black_cnt == 0 or len(self.all_valid_moves(True)) == 0 or len(self.all_valid_moves(False)) == 0 or self.m_no_capture_cnt >= 25

    def who_winner(self) -> str:
        if (len(self.all_valid_moves(True)) == 0 and len(self.all_valid_moves(False)) == 0) or self.m_no_capture_cnt >= 25:
            return "tie"
        elif (self.m_white_cnt and not self.m_black_cnt) or len(self.all_valid_moves(False)) == 0:
            return "white"
        return "black"

    def is_capture(self, pos_from: CPos, pos_to: CPos) -> bool:
        return abs(pos_from.m_r - pos_to.m_r) >= 2 and abs(pos_from.m_r - pos_to.m_r) == abs(pos_from.m_c - pos_to.m_c)

    def possible_simple_moves(self, pos: CPos) -> list[CPos] | None:
        moves = []

        if pos.m_blank or pos.m_checker is None:
            return moves
        if isinstance(pos.m_checker, CKing):
            for dr, dc in pos.m_checker.capture_directions():
                for i in range(1, self.m_board.m_size):
                    new_r = pos.m_r + i * dr
                    new_c = pos.m_c + i * dc
                    if not self.m_board.in_boundaries(new_r, new_c):
                        break
                    new_pos = self.m_board[new_r, new_c]
                    if new_pos.m_blank:
                        moves.append(new_pos)
                    else:
                        break
        else:
            for dr, dc in pos.m_checker.simpe_directions():
                new_r = pos.m_r + dr
                new_c = pos.m_c + dc
                if self.m_board.in_boundaries(new_r, new_c):
                    new_pos = self.m_board[new_r, new_c]
                    if new_pos.m_blank:
                        moves.append(new_pos)

        return moves

    def possible_captures(self, pos: CPos, path: list = None, captured: set = None, result: list = None, is_white: bool = None
    ) -> list[tuple[list[CPos], set[tuple[int, int]]]] | None:
        if path is None: path = []
        if captured is None: captured = set()
        if result is None: result = []
        if is_white is None:
            if pos.m_checker is None:
                return result
            is_white = pos.m_checker.m_white

        found = False

        if isinstance(pos.m_checker, CKing):
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                jumped = False
                enemy_r, enemy_c = pos.m_r + dr, pos.m_c + dc
                while self.m_board.in_boundaries(enemy_r, enemy_c):
                    enemy = self.m_board[enemy_r, enemy_c]
                    if enemy.m_blank:
                        if jumped:
                            landing = self.m_board[enemy_r, enemy_c]
                            cap_r, cap_c = enemy_r - dr, enemy_c - dc
                            if (cap_r, cap_c) not in captured:
                                new_path = path + [landing]
                                new_captured = captured | {(cap_r, cap_c)}
                                found = True
                                self.possible_captures(landing, new_path, new_captured, result, is_white)
                        enemy_r += dr
                        enemy_c += dc
                    elif enemy.m_checker and enemy.m_checker.m_white != is_white and not jumped:
                        jumped = True
                        enemy_r += dr
                        enemy_c += dc
                    else:
                        break
        else:
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                enemy_r = pos.m_r + dr
                enemy_c = pos.m_c + dc
                new_r = pos.m_r + 2 * dr
                new_c = pos.m_c + 2 * dc

                if not self.m_board.in_boundaries(new_r, new_c):
                    continue

                enemy = self.m_board[enemy_r, enemy_c]
                landing = self.m_board[new_r, new_c]

                if (enemy.m_blank or enemy.m_checker is None or
                        enemy.m_checker.m_white == is_white):
                    continue

                if landing.m_blank and (enemy_r, enemy_c) not in captured:
                    new_path = path + [landing]
                    new_captured = captured | {(enemy_r, enemy_c)}
                    found = True
                    self.possible_captures(landing, new_path, new_captured, result, is_white)

        if not found and len(path):
            result.append((path, captured))

        return result

    def valid_moves(self, pos: CPos) -> list[tuple[list[CPos], set[tuple[int, int]]]] | None:
        captures = self.possible_captures(pos)
        if captures: return captures
        return [([move], set()) for move in self.possible_simple_moves(pos)]

    def all_valid_moves(self, is_white: bool) -> list[tuple[list[tuple[int, int]], set[tuple[int, int]]]] | None:
        capture_moves = []
        simple_moves = []

        for r in range(self.m_board.m_size):
            for c in range(self.m_board.m_size):
                pos = self.m_board[r, c]
                if not pos.m_blank and pos.m_checker.m_white == is_white:
                    moves = self.valid_moves(pos)
                    for path, captured in moves:
                        full_path = [(r, c)] + [(p.m_r, p.m_c) for p in path]
                        if captured:
                            capture_moves.append((full_path, captured))
                        else:
                            simple_moves.append((full_path, captured))

        return capture_moves if capture_moves else simple_moves

    def simple_move(self, from_pos: CPos, to_pos: CPos):
        assert not from_pos.m_blank and from_pos.m_checker is not None

        to_pos.m_checker = from_pos.m_checker
        to_pos.m_blank = False
        from_pos.m_checker = None
        from_pos.m_blank = True

        if isinstance(to_pos.m_checker, CComchecker):
            if ((to_pos.m_checker.m_white and to_pos.m_r == self.m_board.m_size - 1) or
                    (not to_pos.m_checker.m_white and to_pos.m_r == 0)):
                to_pos.m_checker = CKing(to_pos.m_checker.m_white)

    def make_move(self, move_with_captures: tuple[list[tuple[int, int]], set[tuple[int, int]]]):
        move, captured_positions = move_with_captures
        assert move
        start_r, start_c = move[0]
        for r, c in move[1:]:
            self.simple_move(self.m_board[start_r, start_c], self.m_board[r, c])
            start_r, start_c = r, c

        if captured_positions:
            self.m_no_capture_cnt = 0
        else:
            self.m_no_capture_cnt += 1

        for cap_r, cap_c in captured_positions:
            captured_pos = self.m_board[cap_r, cap_c]
            if captured_pos.m_checker is not None:
                color = "white" if captured_pos.m_checker.m_white else "black"
                captured_pos.m_checker = None
                captured_pos.m_blank = True
                if color == "white":
                    self.m_white_cnt -= 1
                else:
                    self.m_black_cnt -= 1

    def minimax(self, depth: int, alpha: int, beta: int, is_white: bool) -> int:
        if depth == 0 or self.is_game_over():
            return self.eval_position()

        if is_white:
            max_eval = -np.inf
            for move in self.all_valid_moves(is_white):
                saved_game = self.copy_game()
                saved_game.make_move(move)
                eval = saved_game.minimax(depth - 1, alpha, beta, not is_white)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = np.inf
            for move in self.all_valid_moves(is_white):
                saved_game = self.copy_game()
                saved_game.make_move(move)
                eval = saved_game.minimax(depth - 1, alpha, beta, not is_white)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self, is_white: bool, depth: int) -> list[tuple[int, int]] | None:
        best_eval = -np.inf if is_white else np.inf
        best_action = None

        all_moves = self.all_valid_moves(is_white)

        for move in all_moves:
            saved_game = self.copy_game()

            saved_game.make_move(move)
            eval = saved_game.minimax(depth - 1, -np.inf, np.inf, not is_white)

            if (is_white and eval > best_eval) or (not is_white and eval < best_eval):
                best_eval = eval
                best_action = move

        return best_action