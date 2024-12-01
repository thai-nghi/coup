"use client";

import GameBoard from "@/components/game_board";
import Header from "@/components/header";
import MatchProfile from "@/components/match_profile";
import { BoardCell, CellAddr, PieceColor, PieceFace, PieceType, ReadyState, UserData } from "@/types";

import { useInterval, useSessionStorageState, useWebSocket } from 'ahooks';
import { useEffect, useRef, useState } from "react";

const BOARD_COLUMNS = 9;
const BOARD_ROWS = 10;


const BLANK_BOARD: BoardCell[][] = [];

for (let row = 0; row < BOARD_ROWS; row++) {
    BLANK_BOARD.push([]);
    for (let col = 0; col < BOARD_COLUMNS; col++) {
        BLANK_BOARD[row].push({ chessPiece: undefined });
    }
}

// BLANK_BOARD[0][0] = {
//     chessPiece: {
//         color: PieceColor.BLACK,
//         type: PieceType.CANON,
//         face: PieceFace.UP,
//         down_type: PieceType.CANON
//     }

// };

const EMPTY_CELL: BoardCell = {
    chessPiece: undefined
}
export default function GamePage() {

    const [userData, setUserData] = useSessionStorageState<UserData>("userData");
    const [board, setBoard] = useState<BoardCell[][]>(BLANK_BOARD);
    const [userColor, setUserColor] = useState();
    const [opponentData, setOpponentData] = useState();

    const ref = useRef(null);
    const handleWsMessage = (message: WebSocketEventMap['message']) => {
        console.log(message)
        const data = JSON.parse(message.data);

        if (data.message_id == "GAME"){
            setBoard(data.game.chess_board);

            for (const player of Object.values(data.game.players)){
                if (player.player_id == userData.id) {
                    setUserColor (player.side);
                } else {
                    setOpponentData({display_name: "a", elo: 0});
                }
            }

            
        }
    }
    const { readyState, sendMessage, disconnect, connect } = useWebSocket(
        'ws://192.168.31.115:4000/',
        {
            onMessage: handleWsMessage,
            manual: true
        }
    );

    

    const [selectedCell, setSelectedCell] = useState<CellAddr>();


    useEffect(() => {
        if (readyState == ReadyState.Open && userData) {
            sendMessage(JSON.stringify({
                message_id: 'FIND_MATCH',
                player_id: userData?.id
            }))
        }

    },
        [readyState, userData]);

    useEffect(() => { connect() }, [])

    useEffect(() => { if (!userData) {
        window.open("/login", "_self");
    } }, [userData])

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
                <div className="relative flex h-full w-4/5 lg:px-16 flex-col lg:flex-row">
                    <div className="h-full w-4/5" ref={ref}>
                        <GameBoard board={board} containerRef={ref} setSelectedCellFunc={updateSelectCell} movePieceFunc={movePieceFunc} flipped={userColor == "BLACK"}></GameBoard>
                    </div>
                    <div className="h-full w-full bg-red flex justify-between lg:w-1/5 lg:flex-col pb-5">
                        <div className="w-fit bg-primary-element">
                            <MatchProfile  displayName={opponentData?.display_name} avatar={""} elo={opponentData?.elo}></MatchProfile>
                        </div>
                        <div className="w-fit bg-primary-element pb-4">
                            <MatchProfile  displayName={userData?.display_name} avatar={""} elo={userData?.elo}></MatchProfile>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}