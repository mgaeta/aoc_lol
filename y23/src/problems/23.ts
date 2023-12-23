import {
    parsePoint,
    Point,
    prepareBoard,
    serializePoint
} from "../utils/grid/twoDimensional";
import { range } from "../utils";
import { MaxPriorityQueue } from "@datastructures-js/priority-queue";

enum Direction {
    UP = "^",
    LEFT = "<",
    RIGHT = ">",
    DOWN = "v",
}

const DIRECTIONS = [
    Direction.DOWN,
    Direction.LEFT,
    Direction.RIGHT,
    Direction.UP,
];

class History {
    data: string[];
    visitedStates: Set<string>;
    scores: number[];

    constructor() {
        this.data = [];
        this.visitedStates = new Set<string>();
        this.scores = [];
    }

    getScore(): number {
        const found = this.peek();
        if (!found) return 0;
        return (
            this.scores.reduce((total, next) => total + next, 0)
        );
    }

    add(point: string, score: number): void {
        this.data.push(point);
        this.visitedStates.add(point);
        this.scores.push(score);
    }

    peek(): ({ point: string } | undefined) {
        if (!this.size()) return undefined;
        const point = this.data[this.data.length - 1];
        return { point };
    }

    size(): number {
        return this.data.length;
    }

    isRevisiting(point: string): boolean {
        return this.visitedStates.has(point);
    }

    clone(): History {
        const output = new History();
        output.data = this.data.map(i => i);
        output.scores = this.scores.map(i => i);
        output.visitedStates = new Set<string>(this.visitedStates);
        return output;
    }
}

const directionToPoint = (d: Direction): Point => {
    if (d === Direction.DOWN) return { x: 0, y: 1 };
    if (d === Direction.UP) return { x: 0, y: -1 };
    if (d === Direction.LEFT) return { x: -1, y: 0 };
    if (d === Direction.RIGHT) return { x: 1, y: 0 };
    throw new Error("bad direction");
};

const identifyNodes = (
    board: Map<string, string>,
    length: number,
    width: number,
    options?: { debug?: boolean }
): string[] => {
    const output: string[] = [];
    for (const y of range(length)) {
        for (const x of range(width)) {
            const pp = serializePoint({ x, y });
            const found = board.get(pp);
            if (!found || found === "#") continue;

            let neighborCount = 0;
            for (const d of DIRECTIONS) {
                const delta = directionToPoint(d);
                const candidate = serializePoint({
                    x: x + delta.x,
                    y: y + delta.y,
                });
                const neighbor = board.get(candidate);
                if (neighbor && neighbor !== "#") {
                    neighborCount += 1;
                }
            }
            if (neighborCount > 2) {
                output.push(pp);
            }
        }
    }
    return output;
};

const getDistancesToEachNode = (nodes: string[], history: string[]): [string, number][] => {
    let output: [string, number][] = [];
    for (const i of range(history.length)) {
        const point = history[history.length - 1 - i];
        if (nodes.includes(point)) output.push([point, i]);
    }
    return output;
};

const serializeTuple = (points: string[]): string => points.map(p => p).join(">");

const isNode = (point: Point, nodes: string[]): boolean => nodes.includes(serializePoint(point));

export const getPathBetweenNodes = (
    board: Map<string, string>,
    nodes: string[],
    start: string,
    end: string,
    options?: {
        debug?: boolean
    }
): number => {
    const histories = [[start]];
    let i = 0;
    while (i < 10000000) {
        const history = histories.pop();
        if (!history) break;
        const headString = history[history.length - 1];
        const { x, y } = parsePoint(headString);
        for (const d of DIRECTIONS) {
            const delta = directionToPoint(d);
            const candidate = {
                x: x + delta.x,
                y: y + delta.y
            };
            const pp = serializePoint(candidate);
            if (pp === end) return history?.length;
            if (
                history.includes(pp) ||
                (board.get(pp) || "#") === "#" ||
                isNode(candidate, nodes)
            ) continue;

            const historyCopy = history.map(i => i);
            historyCopy.push(pp);
            histories.push(historyCopy);
        }
    }
    return -1;
};


const getEndpoints = (
    board: Map<string, string>,
    length: number,
    width: number,
): [string, string] => {
    const startX = range(width).find(x => board.get(serializePoint({
        x,
        y: 0
    })) === ".");
    const endX = range(width).find(x => board.get(serializePoint({
        x,
        y: length - 1
    })) === ".");
    if (startX === undefined) throw new Error("no end");
    if (endX === undefined) throw new Error("no end");

    const start = serializePoint({ x: startX, y: 0 });
    const end = serializePoint({ x: endX, y: length - 1 });
    return [start, end];
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, length, width } = prepareBoard(input, options);

    let nodes = identifyNodes(board, length, width, options);
    const [start, end] = getEndpoints(board, length, width);

    nodes.push(start);
    nodes.push(end);

    const distances = new Map<string, number>();
    for (const i in range(nodes.length)) {
        for (const j in range(nodes.length)) {
            if (i < j) {
                const p0 = nodes[i];
                const p1 = nodes[j];
                const x = getPathBetweenNodes(board, nodes, p0, p1, options);
                if (x > 0) {
                    distances.set(serializeTuple([p0, p1]), x);
                }
            }
        }
    }

    let output = -1;
    const heads = new MaxPriorityQueue<History>((h) => h.getScore());
    const root = new History();
    root.add(start, 0);
    heads.enqueue(root);
    while (true) {
        const history = heads.dequeue();
        if (!history) break;

        const current = history.peek();
        if (!current) {
            throw new Error("probably not actually an error");
        }
        const { point } = current;

        const score = history.getScore();

        if (point === end) {
            if (options?.debug) console.log({ history, distances });
            output = Math.max(output, score);
            console.log({ output });
            continue;
        }

        for (const [candidate, score] of findCandidates(point, distances)) {
            if (history.isRevisiting(candidate)) continue;
            const next = history.clone();
            next.add(candidate, score);
            heads.enqueue(next);
        }
    }
    return output;
};

const findCandidates = (point: string, distances: Map<string, number>): [string, number][] => {
    const output: [string, number][] = [];
    for (const [key, value] of distances) {
        const [p0, p1] = key.split(">");
        if (point === p0) output.push([p1, value]);
        if (point === p1) output.push([p0, value]);
    }
    return output;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, length, width } = prepareBoard(input, options);

    const startX = range(width).find(x => board.get(serializePoint({
        x,
        y: 0
    })) === ".");
    if (startX === undefined) throw new Error("no start");

    const start = serializePoint({ x: startX, y: 0 });
    const histories = [[start]];

    let output = -1;
    while (true) {
        const found = histories.pop();
        if (!found) break;
        const headString = found[found.length - 1];
        const { x, y } = parsePoint(headString);
        if (y === length - 1) {
            if (options?.debug) console.log({
                output,
                found: found.length,
            });
            if (options?.debug) console.log(toString(
                    board,
                    length,
                    width,
                    found,
                )
            );

            output = Math.max(output, found.length);
            continue;
        }
        for (const d of DIRECTIONS) {
            const delta = directionToPoint(d);
            const candidate = {
                x: x + delta.x,
                y: y + delta.y
            };
            const pp = serializePoint(candidate);
            if (found.includes(pp)) continue;
            const boardState = board.get(pp);
            if (!boardState || boardState === "#") continue;
            if (d === Direction.UP && boardState === Direction.DOWN) continue;
            if (d === Direction.DOWN && boardState === Direction.UP) continue;
            if (d === Direction.RIGHT && boardState === Direction.LEFT) continue;
            if (d === Direction.LEFT && boardState === Direction.RIGHT) continue;

            let pps = [pp];
            if (boardState !== ".") {
                const delta2 = directionToPoint(boardState as Direction);

                const candidate2 = {
                    x: candidate.x + delta2.x,
                    y: candidate.y + delta2.y
                };
                const pp2 = serializePoint(candidate2);
                if (found.includes(pp2)) continue;
                pps.push(pp2);
            }

            const historyCopy = found.map(i => i);
            for (const pp of pps) {
                historyCopy.push(pp);
            }
            histories.push(historyCopy);
        }
    }
    return output - 1;
};


const toString = (
    board: Map<string, string>,
    length: number,
    width: number,
    history: string[],
    options?: { debug?: boolean },
): string => {
    let output = "";
    for (const y of range(length)) {
        for (const x of range(width)) {
            const pp = serializePoint({ x, y });
            if (history.includes(pp)) {
                output += "0";
            } else {
                output += board.get(pp);
            }
        }
        output += "\n";
    }
    output += "\n";
    return output;
};
