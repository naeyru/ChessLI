"""
Thomas Safago
10/30/23
Algorithm/structure tests for chess. Third revision.
"""

import copy

files = "abcdefgh"
ranks = "12345678"


# Chess position things
def is_valid(pos):
    if pos[0] not in files or pos[1] not in ranks:
        return False
    return True


def pos_to_index(pos):
    return [ord(pos[0])-96, int(pos[1])]


def index_to_pos(index):
    return f"{chr(index[0]+96)}{index[1]}"


# ChessManTemplate / pieces
# Should contain name of chessman, notation, team, visible squares function, movable function
class ChessManTemplate:
    def __init__(self, name, notation, team):
        self.name = name
        self.notation = notation
        self.team = team

    def __str__(self):
        return f"Team: {self.team}\nType: {self.name}"

    def visible(self, pos, board=None):  # What the piece can see
        pass

    def movable(self, pos, board=None):  # All squares the piece can move to
        pass


class King(ChessManTemplate):
    def __init__(self, team=""):
        super().__init__("king", "k", team)

    def visible(self, pos, board=None):
        pass

    def movable(self, pos, board=None):
        pass


class Queen(ChessManTemplate):
    def __init__(self, team=""):
        super().__init__("queen", "q", team)

    def visible(self, pos, board=None):
        pass

    def movable(self, pos, board=None):
        pass


class Rook(ChessManTemplate):
    def __init__(self, team=""):
        super().__init__("rook", "r", team)

    def visible(self, pos, board=None):
        pass

    def movable(self, pos, board=None):
        pass


class Bishop(ChessManTemplate):
    def __init__(self, team=""):
        super().__init__("bishop", "b", team)

    def visible(self, pos, board=None):
        pass

    def movable(self, pos, board=None):
        pass


class Knight(ChessManTemplate):
    def __init__(self, team=""):
        super().__init__("knight", "n", team)

    def visible(self, pos, board=None):
        pass

    def movable(self, pos, board=None):
        pass


class Pawn(ChessManTemplate):
    def __init__(self, team=""):
        super().__init__("pawn", "p", team)

    def visible(self, pos, board=None):
        pass

    def movable(self, pos, board=None):
        pass


class Empty(ChessManTemplate):
    def __init__(self):
        super().__init__("", "", "")


# Chess Board stuff. Support FEN, board states
class GameState:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board = None
        self.active_color = "white"
        self.castling = "KQkq"
        self.en_passant = "-"
        self.board_setup(fen)

    def board_setup(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board = {}

        fen_parse = fen.split(' ')
        fen_pieces = fen_parse[0].split('/')

        r = 9

        for rank in fen_pieces:
            r -= 1
            # One rank at a time. example: "rnbqkbnr" or "8"
            f = 1

            for piece in rank:
                if piece.lower() not in "pnbrqk":  # Must be number of how many files to skip
                    for i in range(int(piece)):
                        self.board[index_to_pos((f, r))] = Empty()
                        f += 1
                else:
                    temp = piece.lower()

                    if temp == piece:
                        team = "black"
                    else:
                        team = "white"

                    if temp == "k":
                        self.board[index_to_pos((f, r))] = King(team)
                    elif temp == "q":
                        self.board[index_to_pos((f, r))] = Queen(team)
                    elif temp == "r":
                        self.board[index_to_pos((f, r))] = Rook(team)
                    elif temp == "b":
                        self.board[index_to_pos((f, r))] = Bishop(team)
                    elif temp == "n":
                        self.board[index_to_pos((f, r))] = Knight(team)
                    elif temp == "p":
                        self.board[index_to_pos((f, r))] = Pawn(team)
                    f += 1

        if fen_parse[1] == "w":
            self.active_color = "white"
        else:
            self.active_color = "black"

        self.castling = fen_parse[2]

        if fen_parse[3] == "-":
            self.en_passant = "-"
        else:
            self.en_passant = fen_parse[2]

    def move(self, old_pos, new_pos):  # TEMPORARY. DO NOT USE
        self.board[new_pos] = self.board[old_pos]
        self.board[old_pos] = Empty()
        return self

    def print_pieces(self):
        for pos in self.board.keys():
            if self.board[pos].name != "":
                print(f"{pos}:\n{self.board[pos]}\n")

    def pretty_print(self):
        black_square = 47
        white_square = 40
        blue_text = 34
        red_text = 31

        end_str = ""
        toggle = False

        for r in reversed(ranks):
            for f in files:
                if toggle:
                    bg = white_square
                else:
                    bg = black_square

                toggle = not toggle

                if self.board[f+r].team == "white":
                    fg = blue_text
                else:
                    fg = red_text

                piece = self.board[f+r].notation.upper()
                if piece == "":
                    piece = " "

                end_str += f"\x1b[1;{fg};{bg}m {piece} \x1b[0m"
            end_str += "\n"
            toggle = not toggle

        print(end_str)


# For feature testing. copy.deepcopy() is nice
def main():
    game = GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    game.pretty_print()
    game = GameState("8/2k5/2p5/3q4/5R2/4RK2/8/8 w - - 0 1")
    game.pretty_print()


if __name__ == "__main__":
    main()
