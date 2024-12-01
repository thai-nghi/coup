"use client";

import GameBoard from "@/components/game_board";
import Header from "@/components/header";
import MatchProfile from "@/components/match_profile";
import { BoardCell, CellAddr, PieceColor, PieceFace, PieceType } from "@/types";

import { useInterval } from 'ahooks';
import { useRef, useState } from "react";

const BOARD_COLUMNS = 9;
const BOARD_ROWS = 10;


const BLANK_BOARD: BoardCell[][] = [];

for (let row = 0; row < BOARD_ROWS; row++) {
    BLANK_BOARD.push([]);
    for (let col = 0; col < BOARD_COLUMNS; col++) {
        BLANK_BOARD[row].push({ chessPiece: undefined });
    }
}

BLANK_BOARD[0][0] = {
    chessPiece: {
        color: PieceColor.BLACK,
        type: PieceType.CANON,
        face: PieceFace.UP,
        down_type: PieceType.CANON
    }

};

const EMPTY_CELL: BoardCell = {
    chessPiece: undefined
}
export default function GamePage() {

    const [roundTime, setRoundTime] = useState<number>(60);
    const ref = useRef(null);

    const [board, setBoard] = useState<BoardCell[][]>(BLANK_BOARD);

    const [selectedCell, setSelectedCell] = useState<CellAddr>();

    useInterval(() => {
        if (roundTime >= 0) {
            setRoundTime(roundTime - 1);
        }

    }, 1000);

    const updateSelectCell = (cell: CellAddr) => {
        setSelectedCell(cell);
    }

    const movePieceFunc = (target: CellAddr) => {
        if (selectedCell) {
            board[target.row][target.col] = board[selectedCell.row][selectedCell.col];
            board[selectedCell.row][selectedCell.col] = EMPTY_CELL;

            setBoard(board);
        }
    }

    return (
        <>
            <Header></Header>
            <div className="relative flex h-screen overflow-auto justify-center pb-8 pt-8 bg-primary-bg w-full">
                <div className="relative flex h-full w-4/5 bg-white px-16">
                    <div className="h-full w-4/5" ref={ref}>
                        <GameBoard board={board} containerRef={ref} setSelectedCellFunc={updateSelectCell} movePieceFunc={movePieceFunc}></GameBoard>
                    </div>
                    <div className="h-full w-1/5 bg-red flex flex-col justify-between">
                        <div className="w-full bg-primary-element">
                            <MatchProfile roundTime={roundTime} matchTime={128} displayName={"Ling"} avatar={""} elo={1500}></MatchProfile>
                        </div>
                        <div className="w-full bg-primary-element pb-4">
                            <MatchProfile roundTime={roundTime} matchTime={128} displayName={"Ling"} avatar={""} elo={1500}></MatchProfile>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}