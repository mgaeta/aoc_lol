import {
    Point,
    prepareBoard,
    serializePoint
} from "../utils/grid/twoDimensional";
import { range } from "../utils";

enum Direction {
    UP = "^",
    LEFT = "<",
    RIGHT = ">",
    DOWN = "V",
}

const directionToPoint = (d: Direction): Point => {
    if (d === Direction.DOWN) return { x: 0, y: 1 };
    if (d === Direction.UP) return { x: 0, y: -1 };
    if (d === Direction.LEFT) return { x: -1, y: 0 };
    if (d === Direction.RIGHT) return { x: 1, y: 0 };
    throw new Error("bad direction");
};

const execute = (
    board: Map<string, string>,
    length: number,
    width: number,
    startPoint: Point,
    startDirection: Direction,
    options?: { debug?: boolean },
): Map<string, Set<Direction>> => {
    const energizedCells = new Map<string, Set<Direction>>();
    let heads: [Point, Direction][] = [[startPoint, startDirection]];

    while (true) {
        const next = heads.pop();
        if (!next) break;
        const [point, direction] = next;
        const delta = directionToPoint(direction);

        const nextCell: Point = {
            x: point.x + delta.x,
            y: point.y + delta.y
        };

        if (nextCell.x >= width ||
            nextCell.x < 0 ||
            nextCell.y >= length ||
            nextCell.y < 0
        ) {
            if (options?.debug) console.log({ nextCell, length, width });
            continue;
        }

        const pp = serializePoint(nextCell);
        const found = board.get(pp);
        if (!found) throw new Error("not found");

        const energyStates = energizedCells.get(pp) || new Set();
        if (energyStates.has(direction)) {
            if (options?.debug) console.log("breaking because in energyStates");
            continue;
        }
        energyStates.add(direction);

        if (options?.debug) console.log({
            point,
            direction,
            delta,
            nextCell,
            energyStates,
            found,
        });

        if (found === ".") {
            energizedCells.set(pp, energyStates);
            heads.push([nextCell, direction]);
        } else if (found === "/") {
            let nextDirection;
            if (direction === Direction.LEFT) {
                nextDirection = Direction.DOWN;
            } else if (direction === Direction.RIGHT) {
                nextDirection = Direction.UP;
            } else if (direction === Direction.DOWN) {
                nextDirection = Direction.LEFT;
            } else {
                nextDirection = Direction.RIGHT;
            }

            energizedCells.set(pp, energyStates);
            heads.push([nextCell, nextDirection]);
        } else if (found === "\\") {
            let nextDirection;
            if (direction === Direction.LEFT) {
                nextDirection = Direction.UP;
            } else if (direction === Direction.RIGHT) {
                nextDirection = Direction.DOWN;
            } else if (direction === Direction.DOWN) {
                nextDirection = Direction.RIGHT;
            } else {
                nextDirection = Direction.LEFT;
            }
            energizedCells.set(pp, energyStates);
            heads.push([nextCell, nextDirection]);
        } else if (found === "-") {
            if ([Direction.LEFT, Direction.RIGHT].includes(direction)) {
                energizedCells.set(pp, energyStates);
                heads.push([nextCell, direction]);
            } else {
                energizedCells.set(pp, energyStates);
                heads.push([nextCell, Direction.LEFT]);
                heads.push([nextCell, Direction.RIGHT]);
            }
        } else if (found === "|") {
            if ([Direction.LEFT, Direction.RIGHT].includes(direction)) {
                energizedCells.set(pp, energyStates);
                heads.push([nextCell, Direction.UP]);
                heads.push([nextCell, Direction.DOWN]);
            } else {
                energizedCells.set(pp, energyStates);
                heads.push([nextCell, direction]);
            }
        } else {
            throw new Error("unknown symbol");
        }
    }
    return energizedCells;
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, length, width } = prepareBoard(input);

    let output = 0;
    for (const y of range(length)) {
        for (const i of range(2)) {
            const energizedCells = execute(
                board,
                length,
                width,
                { x: i ? -1 : length, y },
                i ? Direction.RIGHT : Direction.LEFT,
            );
            output = Math.max(output, energizedCells.size);
        }
    }
    for (const x of range(width)) {
        for (const i of range(2)) {
            const energizedCells = execute(
                board,
                length,
                width,
                { x, y: i ? -1 : width },
                i ? Direction.DOWN : Direction.UP,
            );
            output = Math.max(output, energizedCells.size);
        }
    }

    return output;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { board, length, width } = prepareBoard(input);
    const energizedCells = execute(
        board,
        length,
        width,
        { x: -1, y: 0 },
        Direction.RIGHT,
    );

    return energizedCells.size;
};

