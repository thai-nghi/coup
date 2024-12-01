import enum
from typing import Literal, Union

import pydantic
from src import schemas
from typing_extensions import Annotated
from websockets.server import WebSocketServerProtocol


class PieceColor(str, enum.Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"


class PieceType(str, enum.Enum):
    KING = "KING"
    CANON = "CANON"
    PAWN = "PAWN"
    SOLDIER = "SOLDIER"
    ROOK = "ROOK"
    ELEPHANT = "ELEPHANT"
    KNIGHT = "KNIGHT"


class PieceFace(str, enum.Enum):
    UP = "UP"
    DOWN = "DOWN"


class MessageId(str, enum.Enum):
    FIND_MATCH = "FIND_MATCH"
    CANCEL = ""
    MOVE = "MOVE"
    RESIGN = "RESIGN"


class ChessPiece(pydantic.BaseModel):
    color: PieceColor
    type: PieceType
    face: PieceFace
    down_type: PieceType


class BoardCell(pydantic.BaseModel):
    chessPiece: ChessPiece | None


class MatchmakingEntry(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
    )
    connection: WebSocketServerProtocol
    player_id: int


class Player(MatchmakingEntry):
    # player_profile: schemas.UserResponse
    win_piece: list[ChessPiece]
    side: PieceColor
    turn_time: int
    match_time: int


class Game(pydantic.BaseModel):
    id: str
    chess_board: list[list[BoardCell]]
    players: dict[int, Player]
    current_turn_id: int


class CellAddr(pydantic.BaseModel):
    row: int
    col: int


class FindMatchMessage(pydantic.BaseModel):
    message_id: Literal[MessageId.FIND_MATCH]
    player_id: int


class MoveMessage(pydantic.BaseModel):
    message_id: Literal[MessageId.MOVE]
    start_addr: CellAddr
    dest_addr: CellAddr


Message = Annotated[
    Union[FindMatchMessage, MoveMessage], pydantic.Field(discriminator="message_id")
]

message_type_adapter = pydantic.TypeAdapter(Message)


class GameResponse(pydantic.BaseModel):
    message_id: Literal["GAME"] = "GAME"
    game: Game
