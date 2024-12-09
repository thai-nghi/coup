import random

from src.game_server import objects as game_objects

EMPTY_CELL = game_objects.BoardCell(chessPiece=None)
ROWS = 10
COLUMNS = 9

WHITE_PIECES = [
    {
        "type": game_objects.PieceType.ROOK,
        "amount": 2,
        "start_locations": [(9, 0), (9, 8)],
    },
    {
        "type": game_objects.PieceType.KNIGHT,
        "amount": 2,
        "start_locations": [(9, 1), (9, 7)],
    },
    {
        "type": game_objects.PieceType.ELEPHANT,
        "amount": 2,
        "start_locations": [(9, 2), (9, 6)],
    },
    {
        "type": game_objects.PieceType.SOLDIER,
        "amount": 2,
        "start_locations": [(9, 3), (9, 5)],
    },
    {
        "type": game_objects.PieceType.CANON,
        "amount": 2,
        "start_locations": [(7, 1), (7, 7)],
    },
    {
        "type": game_objects.PieceType.PAWN,
        "amount": 5,
        "start_locations": [(6, 0), (6, 2), (6, 4), (6, 6), (6, 8)],
    },
    {
        "type": game_objects.PieceType.KING,
        "amount": 1,
        "start_locations": [(9, 4)],
    },
]

BLACK_PIECES = [
    {
        "type": game_objects.PieceType.ROOK,
        "amount": 2,
        "start_locations": [(0, 0), (0, 8)],
    },
    {
        "type": game_objects.PieceType.KNIGHT,
        "amount": 2,
        "start_locations": [(0, 1), (0, 7)],
    },
    {
        "type": game_objects.PieceType.ELEPHANT,
        "amount": 2,
        "start_locations": [(0, 2), (0, 6)],
    },
    {
        "type": game_objects.PieceType.SOLDIER,
        "amount": 2,
        "start_locations": [(0, 3), (0, 5)],
    },
    {
        "type": game_objects.PieceType.CANON,
        "amount": 2,
        "start_locations": [(2, 1), (2, 7)],
    },
    {
        "type": game_objects.PieceType.PAWN,
        "amount": 5,
        "start_locations": [(3, 0), (3, 2), (3, 4), (3, 6), (3, 8)],
    },
    {
        "type": game_objects.PieceType.KING,
        "amount": 1,
        "start_locations": [(0, 4)],
    },
]


def generate_front():
    fronts = []
    for piece in WHITE_PIECES:
        if piece["type"] == game_objects.PieceType.KING:
            continue
        fronts.extend([piece["type"]] * piece["amount"])
    random.shuffle(fronts)
    return fronts


def fill_board(
    source_piece,
    board: list[list[game_objects.BoardCell]],
    fronts,
    color: game_objects.PieceColor,
):
    count = 0
    for piece in source_piece:
        for location in piece["start_locations"]:
            if piece["type"] == game_objects.PieceType.KING:
                cell = game_objects.BoardCell(
                    chessPiece=game_objects.ChessPiece(
                        color=color,
                        type=piece["type"],
                        face=game_objects.PieceFace.UP,
                        down_type=piece["type"],
                    )
                )
            else:
                cell = game_objects.BoardCell(
                    chessPiece=game_objects.ChessPiece(
                        color=color,
                        type=fronts[count],
                        face=game_objects.PieceFace.DOWN,
                        down_type=piece["type"],
                    )
                )
                count += 1
            board[location[0]][location[1]] = cell


def init_game_board():
    board = [[EMPTY_CELL] * COLUMNS for _ in range(ROWS)]

    black_fronts = generate_front()
    white_fronts = generate_front()

    fill_board(WHITE_PIECES, board, white_fronts, game_objects.PieceColor.WHITE)
    fill_board(BLACK_PIECES, board, black_fronts, game_objects.PieceColor.BLACK)

    return board


def move_piece(
    start: game_objects.CellAddr,
    dest: game_objects.CellAddr,
    board: list[list[game_objects.BoardCell]],
):
    start_piece = board[start.row][start.col]

    if start_piece.chessPiece is None:
        return

    if start_piece.chessPiece.face == game_objects.PieceFace.DOWN:
        start_piece.chessPiece.face = game_objects.PieceFace.UP

    board[dest.row][dest.col] = start_piece
    board[start.row][start.col] = EMPTY_CELL


def x_valid(x):
    return x < COLUMNS and x >= 0


def y_valid(y):
    return y < ROWS and y >= 0


def x_king_valid(x):
    return x <= 5 and x >= 3


def y_king_valid(y):
    return (y < ROWS and y >= 7) or (y >= 0 and y <= 2)


def compute_rook_moves(piece_color, row, col, board):
    result = []
    directions = [
        {"x": 0, "y": 1},
        {"x": 0, "y": -1},
        {"x": 1, "y": 0},
        {"x": -1, "y": 0},
    ]

    for direction in directions:
        curr_x = col
        curr_y = row

        while x_valid(curr_x + direction["x"]) and y_valid(curr_y + direction["y"]):
            curr_x += direction["x"]
            curr_y += direction["y"]

            if board[curr_y][curr_x].chessPiece:
                if board[curr_y][curr_x].chessPiece.color != piece_color:
                    result.append({"row": curr_y, "col": curr_x})
                break
            else:
                result.append({"row": curr_y, "col": curr_x})

    return result


def compute_canon_moves(piece_color, row, col, board):
    result = []
    directions = [
        {"x": 0, "y": 1},
        {"x": 0, "y": -1},
        {"x": 1, "y": 0},
        {"x": -1, "y": 0},
    ]

    for direction in directions:
        curr_x = col
        curr_y = row

        while x_valid(curr_x + direction["x"]) and y_valid(curr_y + direction["y"]):
            curr_x += direction["x"]
            curr_y += direction["y"]

            if board[curr_y][curr_x].chessPiece:
                while x_valid(curr_x + direction["x"]) and y_valid(
                    curr_y + direction["y"]
                ):
                    curr_x += direction["x"]
                    curr_y += direction["y"]
                    if board[curr_y][curr_x].chessPiece:
                        if board[curr_y][curr_x].chessPiece.color != piece_color:
                            result.append({"row": curr_y, "col": curr_x})
                        break
                break
            else:
                result.append({"row": curr_y, "col": curr_x})

    return result


def compute_knight_moves(piece_color, row, col, board):
    result = []
    directions = [
        {"x": 0, "y": 1},
        {"x": 0, "y": -1},
        {"x": 1, "y": 0},
        {"x": -1, "y": 0},
    ]

    for direction in directions:
        curr_x = col
        curr_y = row

        if x_valid(curr_x + direction["x"]) and y_valid(curr_y + direction["y"]):
            if board[curr_y + direction["y"]][curr_x + direction["x"]].chessPiece:
                continue
            else:
                targets = []
                if direction["x"] != 0:
                    targets = [
                        {"x": curr_x + direction["x"] * 2, "y": curr_y + 1},
                        {"x": curr_x + direction["x"] * 2, "y": curr_y - 1},
                    ]
                else:
                    targets = [
                        {"x": curr_x + 1, "y": curr_y + direction["y"] * 2},
                        {"x": curr_x - 1, "y": curr_y + direction["y"] * 2},
                    ]

                for target in targets:
                    if x_valid(target["x"]) and y_valid(target["y"]):
                        if board[target["y"]][target["x"]].chessPiece:
                            if (
                                board[target["y"]][target["x"]].chessPiece.color
                                != piece_color
                            ):
                                result.append({"row": target["y"], "col": target["x"]})
                        else:
                            result.append({"row": target["y"], "col": target["x"]})

    return result


def compute_elephant_moves(piece_color, row, col, board):
    result = []
    directions = [
        {"x": 1, "y": 1},
        {"x": 1, "y": -1},
        {"x": -1, "y": 1},
        {"x": -1, "y": -1},
    ]

    for direction in directions:
        if x_valid(col + direction["x"]) and y_valid(row + direction["y"]):
            if board[row + direction["y"]][col + direction["x"]].chessPiece:
                continue
            else:
                target = {"x": col + direction["x"] * 2, "y": row + direction["y"] * 2}
                if x_valid(target["x"]) and y_valid(target["y"]):
                    if board[target["y"]][target["x"]].chessPiece:
                        if (
                            board[target["y"]][target["x"]].chessPiece.color
                            != piece_color
                        ):
                            result.append({"row": target["y"], "col": target["x"]})
                    else:
                        result.append({"row": target["y"], "col": target["x"]})

    return result


def compute_soldier_moves(piece_color, row, col, board, face):
    result = []
    directions = [
        {"x": 1, "y": 1},
        {"x": 1, "y": -1},
        {"x": -1, "y": 1},
        {"x": -1, "y": -1},
    ]

    for direction in directions:
        target = {"x": col + direction["x"], "y": row + direction["y"]}
        if (
            face == game_objects.PieceFace.UP
            and x_valid(target["x"])
            and y_valid(target["y"])
        ) or (
            face == game_objects.PieceFace.DOWN
            and x_king_valid(target["x"])
            and y_king_valid(target["y"])
        ):
            if board[target["y"]][target["x"]].chessPiece:
                if board[target["y"]][target["x"]].chessPiece.color != piece_color:
                    result.append({"row": target["y"], "col": target["x"]})
            else:
                result.append({"row": target["y"], "col": target["x"]})

    return result


def compute_king_moves(piece_color, row, col, board):
    result = []
    directions = [
        {"x": 0, "y": 1},
        {"x": 0, "y": -1},
        {"x": 1, "y": 0},
        {"x": -1, "y": 0},
    ]

    for direction in directions:
        target = {"x": col + direction["x"], "y": row + direction["y"]}
        if x_king_valid(target["x"]) and y_king_valid(target["y"]):
            if board[target["y"]][target["x"]].chessPiece:
                if board[target["y"]][target["x"]].chessPiece.color != piece_color:
                    result.append({"row": target["y"], "col": target["x"]})
            else:
                result.append({"row": target["y"], "col": target["x"]})

    return result


def compute_pawn_moves(piece_color, row, col, board):
    result = []
    directions = []

    if piece_color == game_objects.PieceColor.BLACK:
        directions = [{"x": 0, "y": 1}]

        if row > 4:
            directions += [{"x": 1, "y": 0}, {"x": -1, "y": 0}]
    else:
        directions = [{"x": 0, "y": -1}]

        if row < 5:
            directions += [{"x": 1, "y": 0}, {"x": -1, "y": 0}]

    for direction in directions:
        target = {"x": col + direction["x"], "y": row + direction["y"]}
        if x_valid(target["x"]) and y_valid(target["y"]):
            if board[target["y"]][target["x"]].chessPiece:
                if board[target["y"]][target["x"]].chessPiece.color != piece_color:
                    result.append({"row": target["y"], "col": target["x"]})
            else:
                result.append({"row": target["y"], "col": target["x"]})

    return result


def compute_possible_move_of_type(piece_type, row, col, board, piece_color, face):
    if piece_type == game_objects.PieceType.ROOK:
        return compute_rook_moves(piece_color, row, col, board)

    if piece_type == game_objects.PieceType.CANON:
        return compute_canon_moves(piece_color, row, col, board)

    if piece_type == game_objects.PieceType.KNIGHT:
        return compute_knight_moves(piece_color, row, col, board)

    if piece_type == game_objects.PieceType.ELEPHANT:
        return compute_elephant_moves(piece_color, row, col, board)

    if piece_type == game_objects.PieceType.SOLDIER:
        return compute_soldier_moves(piece_color, row, col, board, face)

    if piece_type == game_objects.PieceType.KING:
        return compute_king_moves(piece_color, row, col, board)

    if piece_type == game_objects.PieceType.PAWN:
        return compute_pawn_moves(piece_color, row, col, board)

    return []


def compute_possible_move_from_coord(piece, row, col, board):
    if piece.face == "DOWN":
        return compute_possible_move_of_type(
            piece.down_type, row, col, board, piece.color, piece.face
        )
    else:
        return compute_possible_move_of_type(
            piece.type, row, col, board, piece.color, piece.face
        )


def is_king_under_attack(color, board: list[list[game_objects.BoardCell]]):
    dangerous_cells = []

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col].chessPiece is None:
                continue

            if board[row][col].chessPiece.color == color:
                continue

            dangerous_cells += compute_possible_move_from_coord(
                board[row][col].chessPiece, row, col, board
            )

    for coord in dangerous_cells:
        if not board[coord["row"]][coord["col"]].chessPiece:
            continue

        if board[coord["row"]][coord["col"]].chessPiece.color != color:
            continue

        if (
            board[coord["row"]][coord["col"]].chessPiece.type
            == game_objects.PieceType.KING
        ):
            return True

    return False


def compute_safe_move(piece: game_objects.ChessPiece, row: int, col: int, board):
    possible_moves = compute_possible_move_from_coord(piece, row, col, board)
    result = []

    for cell in possible_moves:
        temp = board[cell["row"]][cell["col"]]
        board[cell["row"]][cell["col"]] = board[row][col]
        board[row][col] = EMPTY_CELL

        if not is_king_under_attack(piece.color, board):
            result.append(cell)

        board[row][col] = board[cell["row"]][cell["col"]]
        board[cell["row"]][cell["col"]] = temp

    return result


def is_check_mate(
    defender_color: game_objects.PieceColor, board: list[list[game_objects.BoardCell]]
):
    safe_moves = []

    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                board[row][col].chessPiece is not None
                and board[row][col].chessPiece.color == defender_color
            ):
                safe_moves = compute_safe_move(
                    board[row][col].chessPiece, row, col, board
                )
                if safe_moves:
                    return False
    return True


def validate_move(
    start: game_objects.CellAddr,
    dest: game_objects.CellAddr,
    board: list[list[game_objects.BoardCell]],
    player_side: game_objects.PieceColor,
) -> bool:
    pass

    if board[start.row][start.col].chessPiece is None:
        return False

    if board[start.row][start.col].chessPiece.color != player_side:
        return False

    possible_moves = compute_safe_move(
        board[start.row][start.col].chessPiece, start.row, start.col, board
    )

    for move in possible_moves:
        if dest.row == move["row"] and dest.col == move["col"]:
            return True

    return True
