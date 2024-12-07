import { MutableRefObject } from "react";

export interface ShopItem {
    id: number;
    name: string;
    description: string;
    price: number;
    banner_pic: string;
}

export interface ShopSectionProps {
    name: string;
    items: ShopItem[];
    clickBuyFn: Function;
}
    
export interface ShopSectionType {
    name: string;
    items: ShopItem[];
}

export interface UserData {
    email: string;
    display_name: string;
    id: number;
    elo: number;
    coins: number;
}

export enum PieceColor {
    WHITE = "WHITE",
    BLACK = "BLACK",
}

export enum PieceType {
    KING = "KING",
    CANON = "CANON",
    PAWN = "PAWN",
    SOLDIER = "SOLDIER",
    ROOK = "ROOK",
    ELEPHANT = "ELEPHANT",
    KNIGHT = "KNIGHT"
}

export enum PieceFace {
    UP = "UP",
    DOWN = "DOWN"
}


export interface ChessPiece {
    color:  PieceColor,
    type: PieceType,
    face: PieceFace,
    down_type: PieceType
}

export interface BoardCell {
    chessPiece: ChessPiece | undefined
}


export interface CellAddr {
    row: number,
    col: number
}

export type SetSelectCellFunc = (cell: CellAddr) => void

export type MovePieceFunc = (target: CellAddr) => void

export interface GameProps {
    board: BoardCell[][],
    containerRef: MutableRefObject<null>,
    setSelectedCellFunc: SetSelectCellFunc,
    movePieceFunc: MovePieceFunc,
    flipped: boolean,
    isTurn: boolean,
}

export enum ReadyState {
    Connecting = 0,
    Open = 1,
    Closing = 2,
    Closed = 3,
  }

  export enum GameState {
    Init = 0,
    Finding = 1,
    WaitReady = 2,
    InGame = 3,
    EndGame = 4
  }

 export const EMPTY_CELL: BoardCell = {
    chessPiece: undefined
}


export interface GameResult {
    elo_change: number,
    coin_change: number,
    result: number
}