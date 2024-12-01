"use client";

import { ChessPiece, GameProps, PieceColor, PieceType } from "@/types";
import { Layer, Stage, Image, Circle } from "react-konva";
import useImage from "use-image";
import { useSize } from 'ahooks';
import { useRef, useState } from "react";
import { BOARD_COLUMNS, BOARD_ROWS, centerCoord, indexToXCoord, indexToYCoord } from "@/game_logic";


export default function GameBoard({ board, containerRef, setSelectedCellFunc, movePieceFunc }: GameProps) {

    const pieceImages = {
        [PieceColor.BLACK]: {},
        [PieceColor.WHITE]: {}
    };

    for (const color of Object.values(PieceColor)) {
        for (const piece of Object.values(PieceType)) {
            [pieceImages[color][piece]] = useImage(`/chess/${color.toLocaleLowerCase()}_${PieceType[piece].toLocaleLowerCase()}.svg`)
        }
    }

    const size = useSize(containerRef);
    const [boardBg] = useImage("/chess/board_bg.svg");
    const [boardFace] = useImage("/chess/board_face.svg");
    const [highlightCell, setHighLightCell] = useState<number[]>([]);

    const backgroundRef = useRef(null)

    const realBoardX = size ? size.width * 0.07 : 0;
    const realBoardY = size ? size.height * 0.07 : 0;

    const highlightPossibleMove = (piece: ChessPiece, index: number) => {
        const currX = Math.floor(index % 10);
        const currY = Math.floor(index / 10);

        console.log(currX, currY);

        const cells = []

        for (let i = 1; (currX+i) < BOARD_COLUMNS; i++) {
            cells.push(currY * BOARD_ROWS + (currX + i));
        }

        setHighLightCell(cells);

        setSelectedCellFunc({row: currY, col: currX});
    }

    const movePiece = (index: number) => {
        setHighLightCell([]);
        movePieceFunc({row: Math.floor(index / 10), col: Math.floor(index % 10)})
    }

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
                        return <>
                            {cell.chessPiece &&
                                <Image
                                    image={pieceImages[cell.chessPiece.color][cell.chessPiece.type]}
                                    x={centerCoord(realBoardX + indexToXCoord(cellIndex), 65)}
                                    y={centerCoord(realBoardY + indexToYCoord(cellIndex), 65)}
                                    onClick={() => { highlightPossibleMove(cell.chessPiece, cellIndex) }}
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
                    {highlightCell.map((index) => 
                        <Circle 
                        x={realBoardX + indexToXCoord(index)} 
                        y={realBoardY + indexToYCoord(index)} 
                        radius={10} 
                        fill="#fc9790"
                        shadowBlur={10} 
                        shadowColor="#fc9790"   
                        onClick={() => movePiece(index)}    
                        key={index}
                        />
                    )

                    }
                </>
            </Layer>
        </Stage>

    )
}

// width - 0.8 widht 0.2 width / 2 = 0.1* 0.5 * width = 0.05