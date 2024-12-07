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
    CANCEL = "CANCEL"
    MOVE = "MOVE"
    RESIGN = "RESIGN"
    READY = "READY"


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
    elo: int
    display_name: str


class Player(MatchmakingEntry):
    # player_profile: schemas.UserResponse
    win_piece: list[ChessPiece]
    side: PieceColor
    turn_time: int
    match_time: int
    ready: bool = False
    elo: int


class Game(pydantic.BaseModel):
    id: str
    chess_board: list[list[BoardCell]]
    players: dict[int, Player]
    current_turn_id: int
    players_ready: int = 0
    opponent_id: dict[int, int]
    match_type: schemas.MatchType
    move_first_player: int
    game_end: bool = False


class CellAddr(pydantic.BaseModel):
    row: int
    col: int


class FindMatchMessage(pydantic.BaseModel):
    message_id: Literal[MessageId.FIND_MATCH]
    player_id: int
    elo: int
    display_name: str


class MoveMessage(pydantic.BaseModel):
    message_id: Literal[MessageId.MOVE]
    start_addr: CellAddr
    dest_addr: CellAddr


class ReadyMessage(pydantic.BaseModel):
    message_id: Literal[MessageId.READY]


class CancelMessage(pydantic.BaseModel):
    message_id: Literal[MessageId.CANCEL]


Message = Annotated[
    Union[FindMatchMessage, MoveMessage, ReadyMessage, CancelMessage],
    pydantic.Field(discriminator="message_id"),
]

message_type_adapter = pydantic.TypeAdapter(Message)


class BaseResposne(pydantic.BaseModel):
    message_id: Literal["MESSAGE"] = "MESSAGE"


class GameResponse(BaseResposne):
    message_id: Literal["GAME"] = "GAME"
    game: Game


class RequestReadyResponse(BaseResposne):
    message_id: Literal["WAIT_READY"] = "WAIT_READY"


class MatchCancelResponse(BaseResposne):
    message_id: Literal["MATCH_CANCEL"] = "MATCH_CANCEL"


class MatchResultResponse(BaseResposne):
    message_id: Literal["MATCH_RESULT"] = "MATCH_RESULT"
    result: schemas.MatchResult
    elo_change: int
    coin_change: int
