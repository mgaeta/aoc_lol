import { Point, serializePoint } from "../utils/grid/twoDimensional";
import { range } from "../utils";

const directionToDelta = (direction: string): Point => {
    switch (direction) {
        case "N":
            return { x: 0, y: -1 };
        case "S":
            return { x: 0, y: 1 };
        case "E":
            return { x: 1, y: 0 };
        case "W":
            return { x: -1, y: 0 };
        default:
            throw new Error("invalid direction");
    }
};

const ALLOWED_TRANSITIONS = {
    ".": [serializePoint({ x: 0, y: 0 })],
    "|": [serializePoint({ x: 0, y: 1 }), serializePoint({ x: 0, y: -1 })],
    "-": [serializePoint({ x: 1, y: 0 }), serializePoint({ x: -1, y: 0 })],
    "7": [serializePoint({ x: 1, y: 1 }), serializePoint({ x: -1, y: -1 })],
    "J": [serializePoint({ x: -1, y: 1 }), serializePoint({ x: 1, y: -1 })],
    "F": [serializePoint({ x: -1, y: 1 }), serializePoint({ x: 1, y: -1 })],
};

const nextDirection = (previousDirection: string, transition: string): string => {
    switch (transition) {
        case ".":
            return "0";
        case "|":
        case "-":
            return previousDirection;
        case "7":
            if (previousDirection === "E") return "S";
            if (previousDirection === "N") return "W";
            throw new Error("bad d1");
        case "J":
            if (previousDirection === "E") return "N";
            if (previousDirection === "S") return "W";
            throw new Error("bad d2");
        case "L":
            if (previousDirection === "W") return "N";
            if (previousDirection === "S") return "E";
            throw new Error("bad d3");
        case "F":
            if (previousDirection === "W") return "S";
            if (previousDirection === "N") return "E";
            throw new Error("bad d4");
        default:
            throw new Error(`bad dd ${transition}`);
    }
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, start, length, width } = constructBoard(input, options);
    const distances = new Map<string, number>();
    distances.set(serializePoint(start), 0);
    let found = false;
    let paths: [string, Point][][] = getPaths(board, start, options);
    for (const path of paths) {
        distances.set(serializePoint(path[0][1]), 1);
    }
    while (!found) {
        for (const i of range(paths.length)) {
            const path = paths[i];
            const [previousDirection, currentPoint] = path[path.length - 1];
            const value = board.get(serializePoint(currentPoint));
            if (!value) throw new Error("lol");
            if (value === "S") {
                found = true;
                break;
            }
            const nd = nextDirection(previousDirection, value);
            const np = nextPoint(board, previousDirection, currentPoint);
            paths[i].push([nd, np]);
            const foundValue = distances.get(serializePoint(currentPoint)) || 0;
            const foundNewValue = distances.get(serializePoint(np)) || Infinity;
            distances.set(serializePoint(np), Math.min(foundValue + 1, foundNewValue));
        }
    }

    if (options?.debug) console.log({ board, distances, length, width });
    if (options?.debug) printCycle(board, distances, length, width);
    return final(board, distances, length, width, options);
};
const final = (
    board: Map<string, string>,
    distances: Map<string, number>,
    length,
    width,
    options?: {
        debug?: boolean
    }
): number => {
    let total = 0;
    for (const y of range(length)) {
        let isIn = false;
        for (const x of range(width)) {
            const pCheck = { x, y };
            const s = serializePoint(pCheck);
            const currentChar = board.get(s);
            if (!currentChar) throw new Error(`Adf ${currentChar} ${s} ${[pCheck.x, pCheck.y]}`);
            if (isIn && options?.debug) console.log({
                pCheck,
                s,
                has: distances.has(s)
            });
            if (distances.has(s)) {
                if (["S", "|", "F", "7"].includes(currentChar)) {
                    isIn = !isIn;
                }
            } else {
                if (isIn) total += 1;
            }
        }
    }
    return total;
};

const printCycle = (board, distances, length, width): void => {
    const MAP = {
        "|": "│",
        "-": "─",
        "L": "└",
        "7": "┐",
        "J": "┘",
        "F": "┌",
        "S": "S",
    };
    for (const y of range(length)) {
        let line: string[] = [];
        for (const x of range(width)) {
            const t = serializePoint({ x, y });
            if (distances.get(t)) {
                line.push(MAP[board.get(t)]);
            } else {
                line.push(" ");
            }
        }
        console.log(line.join(""));
    }
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, start } = constructBoard(input, options);
    const distances = new Map<string, number>();
    distances.set(serializePoint(start), 0);
    let found = false;

    let paths: [string, Point][][] = getPaths(board, start, options);
    while (!found) {
        for (const i of range(paths.length)) {
            const path = paths[i];
            const [previousDirection, currentPoint] = path[path.length - 1];
            const value = board.get(serializePoint(currentPoint));
            if (!value) throw new Error("lol");
            if (value === "S") {
                found = true;
                break;
            }
            const nd = nextDirection(previousDirection, value);
            const np = nextPoint(board, previousDirection, currentPoint);
            paths[i].push([nd, np]);
            const foundValue = distances.get(serializePoint(currentPoint)) || 0;
            const foundNewValue = distances.get(serializePoint(np)) || Infinity;
            distances.set(serializePoint(np), Math.min(foundValue + 1, foundNewValue));
        }
    }

    return (Math.max(...distances.values()) + 1) / 2;
};

const getPaths = (board, start: Point, options?: {
    debug?: boolean
}): [string, Point][][] => {
    let paths: [string, Point][][] = [];
    for (const direction of "NSEW".split("")) {
        const delta = directionToDelta(direction);
        const next = {
            x: start.x + delta.x,
            y: start.y + delta.y,
        };
        const pipe = board.get(serializePoint(next));
        if (!pipe || pipe === ".") continue;
        if (ALLOWED_TRANSITIONS[pipe].includes(serializePoint(delta))) {
            paths.push([[direction, next]]);
        }
    }
    return paths;
};

const nextPoint = (board, previousDirection: string, currentPoint: Point): Point => {
    const transition = board.get(serializePoint(currentPoint));
    const nd = nextDirection(previousDirection, transition);
    const delta = directionToDelta(nd);
    return {
        x: currentPoint.x + delta.x,
        y: currentPoint.y + delta.y,
    };
};

const constructBoard = (input: string[], options?: {
    debug?: boolean
}): {
    board: Map<string, string>,
    start: Point,
    length: number,
    width: number
} => {
    const board = new Map<string, string>;

    let length = input.length;
    let width = input[0].length;

    let start = { x: 0, y: 0 };
    let y = 0;
    for (const line of input) {
        if (options?.debug) console.log({ line });
        let x = 0;
        for (const c of line) {
            const p: Point = { x, y };
            board.set(serializePoint(p), c);
            if (c === "S") start = p;
            x += 1;
        }
        y += 1;
    }
    return { board, start, length, width };
};
