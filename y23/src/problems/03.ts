import { range } from "../utils";
import {
    getNeighbors as getNeighborsNaïve,
    parsePoint,
    Point,
    serializePoint
} from "../utils/grid/twoDimensional";


const GEAR_SYMBOL = "*";
const NUMBER_DICTIONARY = "1234567890";

const isNumber = (input: string): boolean => NUMBER_DICTIONARY.includes(input);

const prepareBoard = (input: string[], options?: {
    debug?: boolean
}): {
    symbolLocations: Map<string, string>,
    partNumberLocations: Map<string, number>,
    length: number,
    width: number,
} => {
    const symbolLocations = new Map<string, string>;

    // This only captures the FIRST location
    const partNumberLocations = new Map<string, number>;

    let width = -1;
    let currentY = 0;
    for (const line of input) {
        width = line.length;
        if (options?.debug) console.log(line);
        let currentNumberBuffer = "";
        let currentX = 0;
        for (const char of line.split("")) {
            if (isNumber(char)) {
                currentNumberBuffer = currentNumberBuffer.concat(char);
            } else {
                if (currentNumberBuffer) {
                    // save the currentNumber
                    const currentPoint = {
                        y: currentY,
                        x: currentX - currentNumberBuffer.length,
                    };
                    partNumberLocations.set(serializePoint(currentPoint), parseInt(currentNumberBuffer));
                }
                if (char !== ".") {
                    symbolLocations.set(serializePoint({
                        y: currentY,
                        x: currentX
                    }), char);
                }
                currentNumberBuffer = "";
            }
            // last
            currentX += 1;
        }
        if (currentNumberBuffer) {
            // save the currentNumber
            const currentPoint = {
                y: currentY,
                x: currentX - currentNumberBuffer.length,
            };
            partNumberLocations.set(serializePoint(currentPoint), parseInt(currentNumberBuffer));
        }
        currentY += 1;
    }

    return {
        symbolLocations,
        partNumberLocations,
        length: input.length,
        width
    };
};

const getGearsToPartNumbersMapping = (options: {
    symbolLocations: Map<string, string>,
    partNumberLocations: Map<string, number>,
    length: number,
    width: number
    debug?: boolean,
}): Map<string, Map<string, number>> => {
    const { symbolLocations, partNumberLocations, debug } = options;

    // mapping of points to list of numbers
    const gears = new Map<string, Map<string, number>>();
    for (const [pointString, number] of partNumberLocations.entries()) {
        const point = parsePoint(pointString);
        const neighbors = getNeighbors(point, number, options);
        for (const neighborString of neighbors) {
            const symbolString = symbolLocations.get(neighborString);
            if (symbolString === GEAR_SYMBOL) {
                const lastValue = gears.get(neighborString) || new Map<string, number>();
                lastValue.set(pointString, number);
                gears.set(neighborString, lastValue);
            }
        }
    }
    return gears;
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const {
        symbolLocations,
        partNumberLocations,
        length,
        width,
    } = prepareBoard(input, options);

    const gears = getGearsToPartNumbersMapping({
        symbolLocations,
        partNumberLocations,
        length,
        width,
        ...options,
    });

    let total = 0;
    for (const gear of gears) {
        const [_, mapping] = gear;
        if (mapping.size > 1) {
            let x = 1;
            for (const entry of mapping) {
                const [__, n] = entry;
                x *= n;
            }

            if (options?.debug) console.log({ x });
            total += x;
        }
    }

    return total;
};
export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const {
        symbolLocations,
        partNumberLocations,
        length,
        width,
    } = prepareBoard(input, options);

    if (options?.debug) console.log(symbolLocations);
    if (options?.debug) console.log(partNumberLocations);

    let total = 0;
    for (const [pointString, number] of partNumberLocations.entries()) {
        const point = parsePoint(pointString);
        const neighbors = getNeighbors(point, number, {
            length,
            width,
            ...options
        });
        for (const neighborString of neighbors) {
            if (symbolLocations.has(neighborString)) {
                total += number;
                break;
            }
        }
    }
    return total;
};

const getNeighbors = (
    point: Point,
    number: number,
    options: {
        debug?: boolean
        length: number,
        width: number,
    }
): Set<string> => {
    const { y, x } = point;
    const numberLength = `${number}`.length;

    const output: Set<string> = new Set();
    for (const l of range(numberLength)) {
        for (const n of getNeighborsNaïve({ x: x + l, y }, options)) {
            output.add(n);
        }
    }
    if (options?.debug) console.log({ point, number, output });
    return output;
};
