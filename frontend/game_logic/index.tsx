
export const BOARD_COLUMNS = 9;

export const BOARD_ROWS = 10;

export function centerCoord(coord: number, radius: number) {
    return coord - (radius / 2);
}

export function indexToXCoord(index: number, flipped: boolean = false) {
    const originX = Math.floor(index % BOARD_COLUMNS);

    if (flipped){
        return ((BOARD_COLUMNS-1) - originX) * 79.7;
    }
    else {
        return originX * 79.7;
    }
}

export function indexToYCoord(index: number, flipped: boolean = false) {
    const originY = Math.floor(index / BOARD_COLUMNS);

    if (flipped){
        return ( (BOARD_ROWS-1) - originY) * 79.7;
    } else {
        return  originY * 79.7;
    }
}

