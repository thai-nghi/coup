"use client";

import { ChessPiece, GameProps, PieceColor, PieceType, PieceFace } from "@/types";
import { Layer, Stage, Image, Circle } from "react-konva";
import useImage from "use-image";
import { useInterval, useSize } from 'ahooks';
import { useEffect, useRef, useState } from "react";
import { BOARD_COLUMNS, BOARD_ROWS, centerCoord, colToCoord, computePossibleMove, computeSafeMove, indexToXCoord, indexToYCoord, isKingUnderAttack, rowToCoord } from "@/game_logic";


export default function GameBoard({ board, containerRef, setSelectedCellFunc, movePieceFunc, flipped, isTurn }: GameProps) {
    const pieceImages = {
        [PieceColor.BLACK]: {},
        [PieceColor.WHITE]: {}
    };

    for (const color of Object.values(PieceColor)) {
        for (const piece of Object.values(PieceType)) {
            [pieceImages[color][piece]] = useImage(`/chess/${color.toLowerCase()}_${PieceType[piece].toLowerCase()}.svg`)
        }
    }

    [pieceImages["BLACK"]["back"]] = useImage("/chess/black_back.svg");
    [pieceImages["WHITE"]["back"]] = useImage("/chess/white_back.svg");

    const size = useSize(containerRef);
    const [boardBg] = useImage("/chess/board_bg.svg");
    const [boardFace] = useImage("/chess/board_face.svg");
    const [highlightCell, setHighLightCell] = useState([]);
    const [isUnderAttack, setUnderAttack] = useState(false);

    const backgroundRef = useRef(null)

    const realBoardX = size ? size.width * 0.07 : 0;
    const realBoardY = size ? size.height * 0.07 : 0;

    const highlightPossibleMove = (piece: ChessPiece, index: number) => {

        if (!isTurn){
            setHighLightCell([]);
            return
        }

        //flipped => user color is black
        if ((flipped && piece.color != PieceColor.BLACK) || (!flipped && piece.color != PieceColor.WHITE)){
            setHighLightCell([]);
            return
        }

        const col = Math.floor(index % BOARD_COLUMNS);
        const row = Math.floor(index / BOARD_COLUMNS);

        const cells = computeSafeMove(piece, index, board);

        console.log(cells);
        console.log(board);

        setHighLightCell(cells);

        setSelectedCellFunc({row: row, col: col});
    }

    const movePiece = (row: number, col: number) => {
        setHighLightCell([]);
        movePieceFunc({row: row, col: col})
    }

    useEffect(() => {
        setUnderAttack(isKingUnderAttack(flipped? PieceColor.BLACK : PieceColor.WHITE ,board));
    },
        [board]);

    return (
        <Stage width={size?.width} height={size?.height}>
            <Layer>
                <Image image={boardBg} ref={backgroundRef}></Image>
            </Layer>
            <Layer>
                <Image image={boardFace} x={realBoardX} y={realBoardY}></Image>
            </Layer>
            <Layer>
                <>
                    {board.flat().map((cell, cellIndex) => {
                        console.log()
                        return <>
                            {cell.chessPiece &&
                                <Image
                                    image={ cell.chessPiece.face == PieceFace.UP ? pieceImages[cell.chessPiece.color][cell.chessPiece.type] : pieceImages[cell.chessPiece.color]['back']}
                                    x={centerCoord(realBoardX + indexToXCoord(cellIndex, flipped), 65)}
                                    y={centerCoord(realBoardY + indexToYCoord(cellIndex, flipped), 65)}
                                    onClick={() => { highlightPossibleMove(cell.chessPiece, cellIndex) }}
                                    shadowColor="#fc9790"
                                >
                                </Image>
                            }
                        </>

                    })}
                </>
                {/* <Image image={chessPiece} x={centerCoord(realBoardX)} y={centerCoord(realBoardY)}></Image> */}
            </Layer>
            <Layer>
                <>
                    {highlightCell.map(({row, col}) => 
                        <Circle 
                        x={realBoardX + colToCoord(col, flipped)} 
                        y={realBoardY + rowToCoord(row, flipped)} 
                        radius={10} 
                        fill="#fc9790"
                        shadowBlur={10} 
                        shadowColor="#fc9790"   
                        onClick={() => movePiece(row, col)}    
                        key={row*BOARD_COLUMNS + col}
                        />
                    )

                    }
                </>
            </Layer>
        </Stage>

    )
}

// width - 0.8 widht 0.2 width / 2 = 0.1* 0.5 * width = 0.05