import { SEPARATOR } from "./constants";
import { getNeighbors as getNeighborsNDimensional } from "./nDimensional";
import { range } from "../array";

export type Point = {
    x: number;
    y: number;
}

export const parsePoint = (pointString: string): Point => {
    const parts = pointString.split(SEPARATOR);
    return {
        x: parseInt(parts[0]),
        y: parseInt(parts[1]),
    };
};

export const serializePoint = (point: Point): string =>
    [point.x, point.y].join(SEPARATOR);

export const getNeighbors = (
    point: Point,
    options: {
        debug?: boolean
        length: number,
        width: number,
    }
): Set<string> =>
    getNeighborsNDimensional(
        [point.x, point.y], {
            includeSelf: false,
            maxPoint: [options.length, options.width]
        }
    );

export const prepareBoard = (input: string[], options?: {
    debug?: boolean
}): {
    board: Map<string, string>,
    length: number,
    width: number
} => {
    const board = new Map<string, string>();
    let y = 0;
    let x = 0;
    for (const line of input) {
        x = 0;
        for (const char of line) {
            const p = { x, y };
            const pp = serializePoint(p);
            board.set(pp, char);
            x += 1;
        }
        y += 1;
    }
    return { board, length: y, width: x };
};

export const rotateBoardRight = (
    board: Map<string, string>,
    length: number,
    width: number,
    count: number = 1,
): {
    board: Map<string, string>,
    length: number,
    width: number,
} => {
    let newBoard = board;
    let newLength = length;
    let newWidth = width;
    for (const _ in range(count % 4)) {
        newBoard = rotateBoardOnce(newBoard, newLength, newWidth);
        const temp = newLength;
        newLength = newWidth;
        newWidth = temp;
    }
    return { board: newBoard, length: newLength, width: newWidth };
};

export const rotateBoardOnce = (
    board: Map<string, string>,
    length: number,
    width: number,
): Map<string, string> => {
    const newBoard = new Map<string, string>();
    for (const y of range(length)) {
        for (const x of range(width)) {
            const found = board.get(serializePoint({ x, y }));
            if (found) {
                newBoard.set(
                    serializePoint(
                        {
                            x: length - y - 1,
                            y: x,
                        }),
                    found
                );
            }
        }
    }
    return newBoard;
};

export const toString = (
    board: Map<string, string>,
    length: number,
    width: number,
): string => {
    let output: string[] = [];
    for (const y of range(length)) {
        output.push(
            range(width).map(x => board.get(serializePoint({
                x,
                y
            })) || ".").join("")
        );
    }
    return output.join("\n");
};

export const printBoard = (
    board: Map<string, string>,
    length: number,
    width: number,
): void => {
    console.log(toString(board, length, width));
};

export const findAll = <T>(
    board: Map<string, T>,
    length: number,
    width: number,
    target: T
): Point[] => {
    let output: Point[] = [];
    for (const y of range(length)) {
        for (const x of range(width)) {
            const p = { x, y };
            const found = board.get(serializePoint(p));
            if (found && found === target) {
                output.push(p);
            }
        }
    }
    return output;
};
