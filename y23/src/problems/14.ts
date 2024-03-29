import {
    findAll,
    prepareBoard,
    rotateBoardRight,
    serializePoint,
    toString
} from "../utils/grid/twoDimensional";
import { range, rangeOf } from "../utils";

const SQUARE_CHAR = "#";
const ROUND_CHAR = "O";
const CYCLES_TOTAL = 1000000000;

const countRounds = (
    board: Map<string, string>,
    length: number,
    width: number,
): number => findAll(board, length, width, ROUND_CHAR).length;

const getSquaresForBoard = (
    board: Map<string, string>,
    length: number,
    width: number,
    options?: { debug?: boolean }
): Set<string> =>
    new Set(findAll(board, length, width, SQUARE_CHAR).map(p => serializePoint(p)));

const getSections = (
    squares: Set<string>,
    length: number,
    width: number,
    options?: { debug?: boolean }
): [number, number][][] => {

    const sectionsByColumn: [number, number][][] = [];
    for (const column of range(width)) {
        //               inclusive, exclusive
        const sections: [number, number][] = [];
        let currentStart = 0;
        for (const row of range(length)) {
            const p = { y: row, x: column };
            const pp = serializePoint(p);
            if (squares.has(pp)) {
                if (row - currentStart >= 1) {
                    sections.push([currentStart, row]);
                }
                currentStart = row + 1;
            }
        }
        if (length - currentStart >= 1) {
            sections.push([currentStart, length]);
        }
        sectionsByColumn.push(sections);
    }
    return sectionsByColumn;
};

const tilt = (
    board: Map<string, string>,
    sectionsByColumn: [number, number][][],
    length: number,
    width: number,
    options?: { debug?: boolean }
): Map<string, string> => {
    const newBoard = new Map<string, string>();
    const before = countRounds(board, length, width);
    const squares = getSquaresForBoard(board, length, width);
    for (const square of squares) {
        newBoard.set(square, SQUARE_CHAR);
    }

    for (const column of range(width)) {
        for (const section of sectionsByColumn[column]) {
            let rockCount = 0;
            for (const i of rangeOf(section[0], section[1])) {
                const point = {
                    x: column, y: i,
                };
                const pp = serializePoint(point);
                const found = board.get(pp);
                if (found) {
                    if (found === ROUND_CHAR) rockCount += 1;
                }
            }

            for (const j of range(rockCount)) {
                const p = { x: column, y: section[0] + j };
                const pp = serializePoint(p);
                newBoard.set(pp, ROUND_CHAR);
            }
        }
    }
    const after = countRounds(board, length, width);
    if (before !== after) throw new Error("number changed");
    return newBoard;
};

const calculateScore = (
    board: Map<string, string>,
    length: number,
    width: number,
    options?: { debug?: boolean }
): number => {
    let total = 0;
    for (const column of range(width)) {
        let columnPlus = 0;
        for (const row of range(length)) {
            const p = { x: column, y: row };
            const pp = serializePoint(p);
            const found = board.get(pp);
            if (found) {
                if (found === ROUND_CHAR) {
                    columnPlus += (length - row);
                }
            }
        }
        total += columnPlus;
    }
    return total;
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const {
        board: boardOriginal,
        length: lengthOriginal,
        width: widthOriginal,
    } = prepareBoard(input);
    const cache = new Map<string, number>();

    let board = boardOriginal;
    let length = lengthOriginal;
    let width = widthOriginal;
    let i = 0;
    let j = 0;
    while (i < CYCLES_TOTAL) {
        for (const j of range(4)) {
            const squares = getSquaresForBoard(
                board,
                length,
                width,
                options
            );

            const sections = getSections(
                squares,
                length,
                width,
                options,
            );

            board = tilt(
                board,
                sections,
                length,
                width,
                options,
            );

            const {
                board: newBoard,
                length: newLength,
                width: newWidth
            } = rotateBoardRight(board, length, width);

            board = newBoard;
            length = newLength;
            width = newWidth;
        }
        const key = toString(board, length, width);
        const found = cache.get(key);
        if (found) {
            j = found;
            break;
        }
        cache.set(key, i);
        i += 1;
    }
    const cycleLength = i - j;
    const times = Math.floor(CYCLES_TOTAL / cycleLength);

    const remainder = CYCLES_TOTAL - (i % cycleLength + times * cycleLength);

    if (options?.debug) console.log({ i, j, cycleLength, remainder, times });

    for (const y of range((remainder - 1) * 4)) {
        const squares = getSquaresForBoard(board, length, width);
        const s = getSections(squares, length, width);
        board = tilt(board, s, length, width);
        const {
            board: newBoard,
            length: newLength,
            width: newWidth
        } = rotateBoardRight(board, length, width);

        board = newBoard;
        length = newLength;
        width = newWidth;
    }

    return calculateScore(
        board,
        length,
        width,
        options,
    );
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const {
        board: boardOriginal,
        length,
        width,
    } = prepareBoard(input);
    const squares = getSquaresForBoard(boardOriginal, length, width);
    const sectionsByColumn = getSections(squares, length, width);
    const boardNew = tilt(boardOriginal, sectionsByColumn, length, width);
    return calculateScore(boardNew, length, width);
};


