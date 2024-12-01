export function centerCoord(coord: number, radius: number) {
    return coord - (radius / 2);
}

export function indexToXCoord(index: number) {
    return Math.floor(index % 10) * 79.7;
}

export function indexToYCoord(index: number) {
    return Math.floor(index / 10) * 79.7;
}


export const BOARD_COLUMNS = 9;

export const BOARD_ROWS = 10;