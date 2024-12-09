import { BoardCell, ChessPiece, EMPTY_CELL, PieceColor, PieceFace, PieceType } from "@/types";
import { Result } from "postcss";

export const BOARD_COLUMNS = 9;

export const BOARD_ROWS = 10;

export function centerCoord(coord: number, radius: number) {
    return coord - (radius / 2);
}

export function rowToCoord(row: number, flipped: boolean = false) {
    if (flipped) {
        return ((BOARD_ROWS - 1) - row) * 79.7;
    }
    else {
        return row * 79.7;
    }
}

export function colToCoord(col: number, flipped: boolean = false) {
    if (flipped) {
        return ((BOARD_COLUMNS - 1) - col) * 79.7;
    } else {
        return col * 79.7;
    }
}

export function indexToXCoord(index: number, flipped: boolean = false) {
    const originX = Math.floor(index % BOARD_COLUMNS);

    return colToCoord(originX, flipped);
}

export function indexToYCoord(index: number, flipped: boolean = false) {
    const originY = Math.floor(index / BOARD_COLUMNS);

    return rowToCoord(originY, flipped);
}


function xValid(x: number) {
    return x < BOARD_COLUMNS && x >= 0
}

function yValid(y: number) {
    return y < BOARD_ROWS && y >= 0
}

function xKingValid(x: number) {
    return x <= 5 && x >= 3
}

function yKingValid(y: number) {
    return (y < BOARD_ROWS && y >= 7) || (y >= 0 && y <= 2)
}

function computeRookMoves(pieceColor, row: number, col: number, board) {
    const result = []
    const directions = [{ x: 0, y: 1 }, { x: 0, y: -1 }, { x: 1, y: 0 }, { x: -1, y: 0 }]

    for (const direction of directions) {
        let currX = col;
        let currY = row;

        while (xValid(currX + direction.x) && yValid(currY + direction.y)) {
            currX += direction.x;
            currY += direction.y;

            if (board[currY][currX].chessPiece) {
                if (board[currY][currX].chessPiece.color != pieceColor) {
                    result.push({ row: currY, col: currX });
                }
                break;
            } else {
                result.push({ row: currY, col: currX });
            }

        }
    }
    return result
}

function computeCanonMoves(pieceColor, row: number, col: number, board) {
    const result = [];

    const directions = [{ x: 0, y: 1 }, { x: 0, y: -1 }, { x: 1, y: 0 }, { x: -1, y: 0 }]

    for (const direction of directions) {
        let currX = col;
        let currY = row;

        while (xValid(currX + direction.x) && yValid(currY + direction.y)) {
            currX += direction.x;
            currY += direction.y;

            if (board[currY][currX].chessPiece) {
                while (xValid(currX + direction.x) && yValid(currY + direction.y)) {
                    currX += direction.x;
                    currY += direction.y;
                    if (board[currY][currX].chessPiece) {
                        if (board[currY][currX].chessPiece.color != pieceColor) {
                            result.push({ row: currY, col: currX });
                        }
                        break;
                    }
                }
                break;
            } else {
                result.push({ row: currY, col: currX });
            }
        }
    }


    return result;
}

function computeKnightMoves(pieceColor, row: number, col: number, board) {
    const result = [];

    const directions = [{ x: 0, y: 1 }, { x: 0, y: -1 }, { x: 1, y: 0 }, { x: -1, y: 0 }]

    for (const direction of directions) {
        let currX = col;
        let currY = row;

        if (xValid(currX + direction.x) && yValid(currY + direction.y)) {
            if (board[currY + direction.y][currX + direction.x].chessPiece) {
                continue
            } else {
                let targets = []
                if (direction.x != 0) {
                    targets = [{ x: currX + direction.x * 2, y: currY + 1 }, { x: currX + direction.x * 2, y: currY - 1 }];
                } else {
                    targets = [{ x: currX + 1, y: currY + direction.y * 2 }, { x: currX - 1, y: currY + direction.y * 2 }];
                }

                for (const target of targets) {
                    if (xValid(target.x) && yValid(target.y)) {
                        if (board[target.y][target.x].chessPiece) {
                            if (board[target.y][target.x].chessPiece.color != pieceColor) {
                                result.push({ row: target.y, col: target.x });
                            }
                        } else {
                            result.push({ row: target.y, col: target.x });
                        }
                    }
                }
            }
        }
    }

    return result;
}

function computeElephantMoves(pieceColor: PieceColor, row: number, col: number, board: any) {
    const result = [];

    const directions = [{ x: 1, y: 1 }, { x: 1, y: -1 }, { x: -1, y: 1 }, { x: -1, y: -1 }]

    for (const direction of directions) {
        if (xValid(col + direction.x) && yValid(row + direction.y)) {
            if (board[row + direction.y][col + direction.x].chessPiece) {
                continue
            } else {
                const target = { x: col + direction.x * 2, y: row + direction.y * 2 };
                if (xValid(target.x) && yValid(target.y)) {
                    if (board[target.y][target.x].chessPiece) {
                        if (board[target.y][target.x].chessPiece.color != pieceColor) {
                            result.push({ row: target.y, col: target.x });
                        }
                    } else {
                        result.push({ row: target.y, col: target.x });
                    }
                }
            }
        }
    }

    return result;
}

function computeSoldierMoves(pieceColor: PieceColor, row: number, col: number, board: any, face: PieceFace) {
    const result = [];

    const directions = [{ x: 1, y: 1 }, { x: 1, y: -1 }, { x: -1, y: 1 }, { x: -1, y: -1 }]

    for (const direction of directions) {
        const target = { x: col + direction.x, y: row + direction.y };
        if (face == PieceFace.UP && xValid(target.x) && yValid(target.y) || (face == PieceFace.DOWN && xKingValid(target.x) && yKingValid(target.y) )) {
            if (board[target.y][target.x].chessPiece) {
                if (board[target.y][target.x].chessPiece.color != pieceColor) {
                    result.push({ row: target.y, col: target.x });
                }
            } else {
                result.push({ row: target.y, col: target.x });
            }
        }
    }

    return result;
}

function computeKingMoves(pieceColor: PieceColor, row: number, col: number, board: any) {
    const result = [];

    const directions = [{ x: 0, y: 1 }, { x: 0, y: -1 }, { x: 1, y: 0 }, { x: -1, y: 0 }]

    for (const direction of directions) {
        const target = { x: col + direction.x, y: row + direction.y };
        if (xKingValid(target.x) && yKingValid(target.y)) {
            if (board[target.y][target.x].chessPiece) {
                if (board[target.y][target.x].chessPiece.color != pieceColor) {
                    result.push({ row: target.y, col: target.x });
                }
            } else {
                result.push({ row: target.y, col: target.x });
            }
        }
    }

    return result;
}

function computePawnMoves(pieceColor: PieceColor, row: number, col: number, board: any) {
    const result = [];

    let directions = [];

    if (pieceColor == PieceColor.BLACK) {
        directions = [{ x: 0, y: 1 }]

        if (row > 4){
            directions = directions.concat([{ x: 1, y: 0 }, { x: -1, y: 0 }]);
        }
    } else {
        directions = [{ x: 0, y: -1 }]

        if (row < 5){
            directions = directions.concat([{ x: 1, y: 0 }, { x: -1, y: 0 }]);
        }
    }

    for (const direction of directions) {
        const target = { x: col + direction.x, y: row + direction.y };
        if (xValid(target.x) && yValid(target.y)) {
            if (board[target.y][target.x].chessPiece) {
                if (board[target.y][target.x].chessPiece.color != pieceColor) {
                    result.push({ row: target.y, col: target.x });
                }
            } else {
                result.push({ row: target.y, col: target.x });
            }
        }
    }

    return result;
}

function computePossibleMoveofType(pieceType: PieceType, row: number, col: number, board, pieceColor: PieceColor, face: PieceFace) {
    if (pieceType == PieceType.ROOK) {
        return computeRookMoves(pieceColor, row, col, board);
    }

    if (pieceType == PieceType.CANON) {
        return computeCanonMoves(pieceColor, row, col, board);
    }

    if (pieceType == PieceType.KNIGHT) {
        return computeKnightMoves(pieceColor, row, col, board);
    }

    if (pieceType == PieceType.ELEPHANT) {
        return computeElephantMoves(pieceColor, row, col, board);
    }

    if (pieceType == PieceType.SOLDIER) {
        return computeSoldierMoves(pieceColor, row, col, board, face);
    }

    if (pieceType == PieceType.KING) {
        return computeKingMoves(pieceColor, row, col, board);
    }

    if (pieceType == PieceType.PAWN){
        return computePawnMoves(pieceColor, row, col, board);
    }
    return [];

}

function computePossibleMoveFromCoord(piece: ChessPiece, row: number, col:number, board){
    if (piece.face == "DOWN") {
        return computePossibleMoveofType(piece.down_type, row, col, board, piece.color, piece.face);
    } else {
        return computePossibleMoveofType(piece.type, row, col, board, piece.color, piece.face);
    }
}

export function computePossibleMove(piece: ChessPiece, index: number, board) {
    const col = Math.floor(index % BOARD_COLUMNS);
    const row = Math.floor(index / BOARD_COLUMNS);

    return computePossibleMoveFromCoord(piece, row, col, board);
}


export function isKingUnderAttack(color: PieceColor, board: BoardCell[][]){
    let dangerousCells = []

    for (let row = 0; row < BOARD_ROWS; ++row){
        for (let col = 0; col < BOARD_COLUMNS; ++col){
            if (!board[row][col].chessPiece){
                continue;
            }

            if (board[row][col].chessPiece?.color == color){
                continue;
            }

            dangerousCells = dangerousCells.concat(computePossibleMoveFromCoord(board[row][col].chessPiece, row, col, board));
        }
    }

    for (let coord of dangerousCells){
        if (!board[coord.row][coord.col].chessPiece){
            continue;
        }

        if (board[coord.row][coord.col].chessPiece?.color != color){
            continue;
        }

        if (board[coord.row][coord.col].chessPiece?.type == PieceType.KING){
            return true;
        }
    }

    return false;
}

export function computeSafeMove(piece: ChessPiece, index: number, board){
    const possibleMoves = computePossibleMove(piece, index, board);
    const col = Math.floor(index % BOARD_COLUMNS);
    const row = Math.floor(index / BOARD_COLUMNS);

    const result = []

    for (let cell of possibleMoves){
        const temp = board[cell.row][cell.col];
        board[cell.row][cell.col] = board[row][col]
        board[row][col] = EMPTY_CELL

        if (!isKingUnderAttack(piece.color, board)){
            result.push(cell)
        }

        board[row][col] = board[cell.row][cell.col]
        board[cell.row][cell.col] = temp
    }

    return result;
}