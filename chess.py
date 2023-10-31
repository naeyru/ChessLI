# Constants
files = "abcdefgh"
ranks = "12345678"


# Important utility stuff
def pos_to_index(pos):
    return [ord(pos[0])-96, int(pos[1])]


def index_to_pos(index):
    return f"{chr(index[0]+96)}{index[1]}"


def valid_pos(pos):
    if pos[0] not in files or pos[1] not in ranks:
        return False
    return True


# Chess Pieces
class ChessManTemplate:
    def __init__(self, name, notation, team):
        self.name = name  # Name of the piece
        self.notation = notation  # Notation used for output
        self.team = team  # Team specifier

    def __str__(self):
        return f"Name: {self.name}\nTeam: {self.team}"

    def visible_squares(self, pos, board):  # pos -> position of the piece
        pass  # Should return list of squares "visible" to the piece, not including itself

    def attacking_squares(self, pos, board):
        pass  # Fundamentally the same as visible squares, only return squares that can be captured


class ChessManKing(ChessManTemplate):
    def __init__(self, team):
        super().__init__("king", "k", team)

    def visible_squares(self, pos, board=None):
        n_pos = pos_to_index(pos)
        squares = []

        for f in [-1, 0, 1]:
            for r in [-1, 0, 1]:
                t_pos = index_to_pos([n_pos[0] - f, n_pos[1] - r])
                if t_pos != pos and valid_pos(t_pos):
                    squares.append(t_pos)
        return squares

    def attacking_squares(self, pos, board):
        return self.visible_squares(pos, board)


class ChessManQueen(ChessManTemplate):
    def __init__(self, team):
        super().__init__("queen", "q", team)

    def visible_squares(self, pos, board):
        return ChessManBishop("white").visible_squares(pos, board) + ChessManRook("white").visible_squares(pos, board)

    def attacking_squares(self, pos, board):
        squares = self.visible_squares(pos, board)
        attacking_squares = []

        for piece in squares:
            if board.board[piece].team != self.team:
                attacking_squares.append(board.board[piece])

        return attacking_squares


class ChessManRook(ChessManTemplate):
    def __init__(self, team):
        super().__init__("rook", "r", team)

    def visible_squares(self, pos, board):
        squares = []
        n_pos = pos_to_index(pos)

        # Get rank moves
        for dir_x in [-1, 1]:
            t_pos = n_pos.copy()  # IMPORTANT for not using reference
            t_pos[0] += dir_x
            while valid_pos(index_to_pos(t_pos)):
                squares.append(index_to_pos(t_pos))
                if board.board[index_to_pos(t_pos)].name != "":  # Populated by an actual piece
                    break
                t_pos[0] += dir_x

        # Get file moves
        for dir_y in [-1, 1]:
            t_pos = n_pos.copy()  # IMPORTANT for not using reference
            t_pos[1] += dir_y
            while valid_pos(index_to_pos(t_pos)):
                squares.append(index_to_pos(t_pos))
                if board.board[index_to_pos(t_pos)].name != "":  # Populated by an actual piece
                    break
                t_pos[1] += dir_y

        return squares

    def attacking_squares(self, pos, board):
        squares = self.visible_squares(pos, board)
        attacking_squares = []

        for piece in squares:
            if board.board[piece].team != self.team:
                attacking_squares.append(board.board[piece])

        return attacking_squares


class ChessManBishop(ChessManTemplate):
    def __init__(self, team):
        super().__init__("bishop", "b", team)

    def visible_squares(self, pos, board):
        squares = []

        # Get diagonals
        for dir_x in [-1, 1]:
            for dir_y in [-1, 1]:
                n_pos = pos_to_index(pos)
                n_pos[0] += dir_x
                n_pos[1] += dir_y
                while valid_pos(index_to_pos(n_pos)):
                    squares.append(index_to_pos(n_pos))
                    if board.board[index_to_pos(n_pos)].name != "":  # Populated by an actual piece
                        break
                    n_pos[0] += dir_x
                    n_pos[1] += dir_y

        return squares

    def attacking_squares(self, pos, board):
        squares = self.visible_squares(pos, board)
        attacking_squares = []

        for piece in squares:
            if board.board[piece].team != self.team:
                attacking_squares.append(board.board[piece])

        return attacking_squares


class ChessManKnight(ChessManTemplate):
    def __init__(self, team):
        super().__init__("knight", "n", team)

    def visible_squares(self, pos, board):
        squares = []
        n_pos = pos_to_index(pos)

        for dir_x in [-2, 2]:
            for dir_y in [-1, 1]:
                t_pos = [n_pos[0] - dir_x, n_pos[1] - dir_y]
                if valid_pos(index_to_pos(t_pos)):
                    squares.append(index_to_pos(t_pos))

        for dir_x in [-1, 1]:
            for dir_y in [-2, 2]:
                t_pos = [n_pos[0] - dir_x, n_pos[1] - dir_y]
                if valid_pos(index_to_pos(t_pos)):
                    squares.append(index_to_pos(t_pos))

        return squares

    def attacking_squares(self, pos, board):
        squares = self.visible_squares(pos, board)
        attacking_squares = []

        for piece in squares:
            if board.board[piece].team != self.team:
                attacking_squares.append(board.board[piece])

        return attacking_squares


class ChessManPawn(ChessManTemplate):
    def __init__(self, team):
        super().__init__("pawn", "p", team)

    def visible_squares(self, pos, board):
        squares = []
        dir_y = 1  # if white

        if self.team == "black":
            dir_y = -1

        for dir_x in [-1, 1]:
            n_pos = pos_to_index(pos)
            n_pos[0] += dir_x
            n_pos[1] += dir_y
            if valid_pos(index_to_pos(n_pos)):
                squares.append(index_to_pos(n_pos))

        return squares


class ChessManEmpty(ChessManTemplate):
    def __init__(self):
        super().__init__("", "", "")


# Chess Board
class ChessBoard:
    def __init__(self):
        self.board = {}
        for f in files:
            for r in ranks:
                key = f"{f}{r}"
                team = ""

                if r in "1278":
                    if r == "2":  # White pawns
                        self.board[key] = ChessManPawn("white")
                    elif r == "7":  # Black pawns
                        self.board[key] = ChessManPawn("black")

                    if r in "18":  # Fill back ranks
                        if r == "1":
                            team = "white"
                        elif r == "8":
                            team = "black"

                        if f in "ah":  # Rooks
                            self.board[key] = ChessManRook(team)
                        elif f in "bg":  # Knights
                            self.board[key] = ChessManKnight(team)
                        elif f in "cf":  # Bishops
                            self.board[key] = ChessManBishop(team)
                        elif f == "d":  # Queens
                            self.board[key] = ChessManQueen(team)
                        elif f == "e":  # Kings
                            self.board[key] = ChessManKing(team)
                else:
                    self.board[key] = ChessManEmpty()

    def print_pieces(self):
        for r in ranks:
            for f in files:
                if self.board[f"{f}{r}"].team != "":
                    print(self.board[f"{f}{r}"], '\n')

    def get_visible_pieces(self, pos):  # Returns all pieces that "see" a specific square
        pieces = []

        # Find rooks/queens that can see square
        visible = ChessManRook("white").visible_squares(pos, self)
        for piece in visible:
            if self.board[piece].name == "rook" or self.board[piece].name == "queen":
                pieces.append((self.board[piece], piece))

        # Find bishops/queens that can see square
        visible = ChessManBishop("white").visible_squares(pos, self)
        for piece in visible:
            if self.board[piece].name == "bishop" or self.board[piece].name == "queen":
                pieces.append((self.board[piece], piece))

        # Find knights that can see squares
        visible = ChessManKnight("white").visible_squares(pos, self)
        for piece in visible:
            if self.board[piece].name == "knight":
                pieces.append((self.board[piece], piece))

        # Find pawns
        visible = ChessManPawn("white").visible_squares(pos, self) + ChessManPawn("black").visible_squares(pos, self)
        for piece in visible:
            if self.board[piece].name == "pawn":
                pieces.append((self.board[piece], piece))

        return pieces


def main():
    game_board = ChessBoard()
    game_board.board["e5"] = ChessManQueen("white")
    for piece in game_board.get_visible_pieces("c3"):
        print(f"{piece[1]}:\n{piece[0]}\n")


if __name__ == "__main__":
    main()
