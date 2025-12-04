import {
    cloneBoard,
    getNeighbors,
    Point,
    prepareBoard,
    serializePoint
} from "../utils/grid/twoDimensional";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    const {board, length, width}  = prepareBoard(input)

    let nextBoard = board;
    while (true) {
        const {board: bb, count } = step(nextBoard, length, width)
        if (count == 0 ) {
            break
        }
        nextBoard = bb
        total += count
    }


    return total;
};

const step = (
    input: Map<string, string>,
    length: number,
    width: number,
    options?: {
    debug?: boolean
}): {
    board: Map<string, string>, count: number
} => {
    const output = cloneBoard(input, length, width)
    let total = 0;

    for (let row = 0; row < length; row += 1) {
        for (let col = 0; col < width; col += 1) {
            const point: Point = {x: col, y: row}
            const neighbors = getNeighbors(point, {length, width})

            const self = input.get(`${point.x}:${point.y}`)
            if (self == "@") {
                let count = 0
                for (const neighbor of neighbors) {
                    const parts = neighbor.split(":")
                    const x = parseInt(parts[0])
                    const y = parseInt(parts[1])

                    if (x >= 0 && x < width && y >= 0 && y < length) {
                        const pp = `${x}:${y}`
                        const found = input.get(pp)
                        if (found == "@") {
                            count += 1
                        }
                    }
                }
                if (count < 4) {
                    total += 1
                    output.set(serializePoint(point), ".")
                }
            }
        }
    }

    return {board: output, count: total};
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    const {board, length, width}  = prepareBoard(input)

    // length == row == y
    // width == col == x
    for (let row = 0; row < length; row += 1) {
        for (let col = 0; col < width; col += 1) {
            const point: Point = {x: col, y: row}
            const neighbors = getNeighbors(point, {length, width})

            const self = board.get(`${point.x}:${point.y}`)
            if (self == "@") {

                let count = 0
                for (const neighbor of neighbors) {
                    const parts = neighbor.split(":")
                    const x = parseInt(parts[0])
                    const y = parseInt(parts[1])

                    if (x >= 0 && x < width && y >= 0 && y < length) {

                        const found = board.get(`${x}:${y}`)
                        if (found == "@") {
                            count += 1
                        }
                    }
                }
                if (count < 4) {
                    console.log(point)
                    total += 1
                }
            }
        }
    }

    return total;
};

