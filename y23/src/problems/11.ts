import { Point } from "../utils/grid/twoDimensional";
import { range } from "../utils";
import { difference } from "../utils/set";

const FACTOR_0 = 2;
const FACTOR_1 = 1000000;
const GALAXY_CHAR = "#";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, length, width } = prepareBoard(input, options);
    const {
        rowsWithoutGalaxies,
        columnsWithoutGalaxies,
    } = findEmptySpace(board, length, width);

    if (options?.debug) console.log({
        board,
        length,
        width,
        rowsWithoutGalaxies,
        columnsWithoutGalaxies
    });

    let total = 0;
    for (const [i, pi] of board) {
        for (const [j, pj] of board) {
            if (i >= j) continue;

            const maxX = Math.max(pi.x, pj.x);
            const maxY = Math.max(pi.y, pj.y);
            const minX = Math.min(pi.x, pj.x);
            const minY = Math.min(pi.y, pj.y);
            let distance = ((maxX - minX) + (maxY - minY));

            for (const row of rowsWithoutGalaxies) {
                if (maxY > row && minY < row) distance += FACTOR_1 - 1;
            }

            for (const column of columnsWithoutGalaxies) {
                if (maxX > column && minX < column) distance += FACTOR_1 - 1;
            }

            if (options?.debug) console.log({ i, j, distance });
            total += distance;
        }
    }
    return total;
};


const findEmptySpace = (board: Map<number, Point>, length: number, width: number): {
    rowsWithoutGalaxies: number[],
    columnsWithoutGalaxies: number[],
} => {
    const foundX = new Set(Array.from(board.values()).map(({ x }) => x));
    const foundY = new Set(Array.from(board.values()).map(({ y }) => y));

    return {
        rowsWithoutGalaxies: Array.from(difference(new Set(range(length)), foundY)),
        columnsWithoutGalaxies: Array.from(difference(new Set(range(width)), foundX)),
    };
};

const prepareBoard = (input: string[], options?: {
    debug?: boolean
}): {
    board: Map<number, Point>,
    length: number,
    width: number,
} => {
    const board = new Map<number, Point>;

    let index = 0;
    let column = 0;
    let row = 0;
    for (const line of input) {
        column = 0;
        for (const char of line.split("")) {
            if (char === GALAXY_CHAR) {
                const point: Point = { x: column, y: row };
                board.set(index, point);
                index += 1;
            }
            column += 1;
        }
        row += 1;
    }
    return { board, length: row, width: column };
};
