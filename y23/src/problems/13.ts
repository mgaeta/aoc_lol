import { splitInputs } from "../utils/io";
import { prepareBoard, serializePoint } from "../utils/grid/twoDimensional";
import { range } from "../utils";

const permuteBoard = (
    board: Map<string, string>,
    length: number,
    width: number
): Map<string, string>[] => {
    const output: Map<string, string>[] = [];

    for (const x of range(width)) {
        for (const y of range(length)) {
            const boardCopy = new Map<string, string>(board);
            const key = serializePoint({ x, y });
            boardCopy.set(key, boardCopy.get(key) === "#" ? "." : "#");
            output.push(boardCopy);
        }
    }
    return output;
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let verticalTotals: number[] = [];
    let horizontalTotals: number[] = [];
    const blocks = splitInputs(input);
    for (const block of blocks) {
        const { board: boardOriginal, length, width } = prepareBoard(block);
        const h0 = findHorizontalSplit(boardOriginal, length, width, options);
        const v0 = findVerticalSplit(boardOriginal, length, width, options);

        const boards = permuteBoard(boardOriginal, length, width);
        if (options?.debug) console.log({ boards: boards.length });

        for (const board of boards) {
            const h1 = findHorizontalSplit(board, length, width, {
                ...options,
                exclude: h0 ? [h0] : []
            });
            const v1 = findVerticalSplit(board, length, width, {
                ...options,
                exclude: v0 ? [v0] : []
            });
            if (h1) horizontalTotals.push(h1);
            if (v1) verticalTotals.push(v1);
        }
    }
    if (options?.debug) console.log({ horizontalTotals, verticalTotals });

    return (
        100 * horizontalTotals.reduce((total, next) => total + next, 0)
        + verticalTotals.reduce((total, next) => total + next, 0)
    ) / 2; // Every smudge could be just a reflection.
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let verticalTotals: number[] = [];
    let horizontalTotals: number[] = [];
    const blocks = splitInputs(input);
    for (const block of blocks) {
        const { board, length, width } = prepareBoard(block);
        const h0 = findHorizontalSplit(board, length, width, options);
        const v0 = findVerticalSplit(board, length, width, options);
        if (h0) horizontalTotals.push(h0);
        if (v0) verticalTotals.push(v0);
    }

    return (
        100 * horizontalTotals.reduce((total, next) => total + next, 0)
        + verticalTotals.reduce((total, next) => total + next, 0)
    );
};


const findHorizontalSplit = (
    board: Map<string, string>,
    length: number,
    width: number,
    options?: {
        debug?: boolean,
        exclude?: number[],
    }
): number | undefined => {
    const lineStringsStack: string[] = [];
    let found: number | undefined = undefined;
    for (const y of range(length)) {
        const currentRow = range(width).map(x => board.get(serializePoint({
            x,
            y
        }))).join("");
        const previousRow = lineStringsStack.pop();

        if (found === undefined) {
            if (previousRow && currentRow === previousRow && !options?.exclude?.includes(y)) {
                found = y;
            } else {
                if (previousRow) lineStringsStack.push(previousRow);
                lineStringsStack.push(currentRow);
            }
        } else {
            if (previousRow && currentRow !== previousRow) {
                // try again, excluding found.
                const previousExclusions = options?.exclude || [];
                previousExclusions.push(found);
                return findHorizontalSplit(board, length, width, {
                    ...options,
                    exclude: previousExclusions
                });
            }
        }
    }
    return found;
};

const findVerticalSplit = (
    board: Map<string, string>,
    length: number,
    width: number,
    options?: {
        debug?: boolean,
        exclude?: number[],
    }
): number | undefined => {
    const lineStringsStack: string[] = [];
    let found: number | undefined = undefined;
    for (const x of range(width)) {
        const currentRow = range(length).map(y => board.get(serializePoint({
            x,
            y
        }))).join("");
        const previousRow = lineStringsStack.pop();

        if (found === undefined) {
            if (previousRow && currentRow === previousRow && !options?.exclude?.includes(x)) {
                found = x;
            } else {
                if (previousRow) lineStringsStack.push(previousRow);
                lineStringsStack.push(currentRow);
            }
        } else {
            if (previousRow && currentRow !== previousRow) {
                // try again, excluding found.
                const previousExclusions = options?.exclude || [];
                previousExclusions.push(found);
                return findVerticalSplit(board, length, width, {
                    ...options,
                    exclude: previousExclusions
                });
            }
        }
    }
    return found;
};
