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
