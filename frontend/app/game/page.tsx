"use client";

import GameBoard from "@/components/game_board";
import Header from "@/components/header";
import MatchProfile from "@/components/match_profile";
import { BoardCell, CellAddr, GameState, PieceColor, PieceFace, PieceType, ReadyState, UserData } from "@/types";

import { useInterval, useSessionStorageState, useUnmount, useWebSocket } from 'ahooks';
import { Button, ConfigProvider, Modal, Typography } from "antd";
import { useEffect, useRef, useState } from "react";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCrown, faCoins } from '@fortawesome/free-solid-svg-icons'

const { Title } = Typography;

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

export default function GamePage() {

    const [userData, setUserData] = useSessionStorageState<UserData>("userData");
    const [board, setBoard] = useState<BoardCell[][]>(BLANK_BOARD);
    const [userColor, setUserColor] = useState();
    const [opponentData, setOpponentData] = useState();
    const [isOwnTurn, setOwnTurn] = useState(false);
    const [gameState, setGameState] = useState(GameState.Init);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [gameResult, setGameResult] = useState();

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
        if (gameState == GameState.WaitReady) {
            sendMessage(JSON.stringify({
                message_id: 'READY',
            }));
            setGameState(GameState.InGame);
        }
        if (gameState == GameState.EndGame){
            connect();
            setGameResult({elo_change: data.elo_change, coin_change: data.coin_change, result: data.result});
            setGameState(GameState.Init);
        }
    };

    const handleCancel = () => {
        setIsModalOpen(false);
        if (gameState == GameState.WaitReady || gameState == GameState.EndGame) {
            disconnect();
            window.open("/", "_self");
        }

    };

    const ref = useRef(null);
    const handleWsMessage = (message: WebSocketEventMap['message']) => {
        console.log(message)
        const data = JSON.parse(message.data);

        if (data.message_id == "GAME") {
            setBoard(data.game.chess_board);

            for (const player of Object.values(data.game.players)) {
                if (player.player_id == userData.id) {
                    setUserColor(player.side);
                } else {
                    setOpponentData({ display_name: player.display_name, elo: player.elo });
                }
            }

            setOwnTurn(data.game.current_turn_id == userData.id);
        }

        if (data.message_id == "WAIT_READY") {
            setGameState(GameState.WaitReady);
        }

        if (data.message_id == "MATCH_CANCEL") {
            setGameState(GameState.EndGame);
            setIsModalOpen(true);
            disconnect();
        }

        if (data.message_id == "MATCH_RESULT"){
            setGameState(GameState.EndGame);
            setGameResult({elo_change: data.elo_change, coin_change: data.coin_change, result: data.result});
            userData.elo += data.elo_change;
            userData.coins += data.coin_change;

            setUserData(userData);
            disconnect();
            setIsModalOpen(true);
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
        if (readyState == ReadyState.Open && userData && (gameState == GameState.Init)) {
            sendMessage(JSON.stringify({
                message_id: 'FIND_MATCH',
                player_id: userData?.id,
                elo: userData?.elo,
                display_name: userData.display_name
            }))
            setGameState(GameState.Finding);
            showModal();
        }

    },
        [readyState, userData, gameState]);

    useEffect(() => { connect() }, []);

    useEffect(() => {
        if (!userData) {
            window.open("/login", "_self");
        }
    }, [userData]);

    const updateSelectCell = (cell: CellAddr) => {
        setSelectedCell(cell);
    }

    const movePieceFunc = (target: CellAddr) => {
        if (selectedCell) {
            sendMessage(JSON.stringify({
                message_id: 'MOVE',
                start_addr: selectedCell,
                dest_addr: target
            }));
        }
    }

    const modalDisplayString = () => {
        console.log("Current game state: " + gameState);
        if (gameState == GameState.Finding) {
            return "Finding Match";
        } else if (gameState == GameState.WaitReady) {
            return "MATCH FOUND !!!";
        } else if (gameState == GameState.EndGame) {
            if (gameResult){
                if (gameResult.result == 0){
                    return "MATCH LOST";
                } else {    
                    return "MATCH WON";
                }
            } else {
                return "MATCH CANCELLED";
            }
            
        }
    }

    const footerButtons = () => {
        if (gameState == GameState.EndGame) {
            return [
                <Button key="play" type="primary" onClick={handleOk}>
                    Play again
                </Button>,
                <Button key="back" onClick={handleCancel}>
                    Back to menu
                </Button>,
            ]

        } else {
            return [
                <Button key="play" type="primary" onClick={handleOk} disabled={gameState == GameState.Finding}>
                    OK
                </Button>,
                <Button key="back" onClick={handleCancel} disabled={gameState == GameState.Finding}>
                    Cancel
                </Button>,
            ]
        }
    }

    return (
        <>
            <ConfigProvider
                theme={{
                    components: {
                        Button: {
                            defaultActiveBg: '#99B898',
                            defaultActiveColor: '#99B898',
                            defaultBg: '#99B898'
                        }
                    },
                    token: {
                        colorBgElevated: '#99B898',
                        colorText: '#FFFFFF',
                        colorPrimaryActive: '#E84A5F',
                        colorPrimary: '#E84A5F'
                    },
                }}
            >
                <Header></Header>
                <div className="relative flex h-screen overflow-auto justify-center pb-8 pt-8 bg-primary-bg w-full">
                    <div className="relative flex h-full w-4/5 lg:px-16 flex-col lg:flex-row">
                        <div className="h-full w-4/5" ref={ref}>
                            <GameBoard board={board} containerRef={ref} setSelectedCellFunc={updateSelectCell} movePieceFunc={movePieceFunc} flipped={userColor == "BLACK"} isTurn={isOwnTurn}></GameBoard>
                        </div>
                        <div className="h-full w-full bg-red flex justify-between lg:w-1/5 lg:flex-col pb-5">
                            <div className="w-fit bg-primary-element">
                                <MatchProfile displayName={opponentData?.display_name} avatar={""} elo={opponentData?.elo}></MatchProfile>
                            </div>


                            <Title level={2} className="">{isOwnTurn ? "Your Turn" : "Opponent's Turn"}</Title>


                            <div className="w-fit bg-primary-element pb-4">
                                <MatchProfile displayName={userData?.display_name} avatar={""} elo={userData?.elo}></MatchProfile>
                            </div>
                        </div>
                    </div>
                </div>

                <Modal title="" open={isModalOpen} footer={footerButtons()}>
                    <>
                        <Title level={2} className="">{modalDisplayString()}</Title>
                        <>
                        { gameResult && (
                            <>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faCrown} size="2x" /></div>
                                <p className="text-2xl">{gameResult?.elo_change}</p>
                            </div>
                            <div className="flex items-center gap-5">
                                <div className="w-1/4"><FontAwesomeIcon icon={faCoins} size="2x" /></div>
                                <p className="text-2xl">{gameResult?.coin_change}</p>
                            </div>
                            </>
                        )

                        }
                        </>
                    </>
                </Modal>
            </ConfigProvider>
        </>
    )
}