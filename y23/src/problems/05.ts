import { range } from "../utils";
import { splitInputs } from "../utils/io";

type Mapping = Map<string, number>;
type Range = {
    start: number,
    end: number,
    delta?: number;
}

const SEPARATOR = ":";

const serializeRange = (r: Range): string => `${r.start}${SEPARATOR}${r.end}`;

const deserializeRange = (s: string): Range => {
    const [start, end] = s.split(SEPARATOR).map(i => parseInt(i));
    return { start, end };
};

const inputToRange = (line: string): Range => {
    const [
        destinationRangeStart,
        sourceRangeStart,
        rangeLength
    ] = line.split(" ").map(i => parseInt(i));

    return ({
        start: sourceRangeStart,
        end: sourceRangeStart + rangeLength - 1,
        delta: destinationRangeStart - sourceRangeStart
    });
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const blocks = splitInputs(input);
    const blockMaps: Mapping[] = blocks.slice(1).map(block => processBlock(block, options));

    const baseSeeds = processSeeds2(blocks, options);
    let currentSeeds: Mapping =
        new Map<string, number>(baseSeeds.map(b => [serializeRange(b), 0]));
    for (const block of blockMaps) {
        if (options?.debug) console.log({ currentSeeds });
        let nextSeeds: Mapping = new Map<string, number>();
        let seedQueue = Array.from(currentSeeds.entries());
        if (options?.debug) console.log({ seedQueue, block });

        while (true) {
            const exists = seedQueue.pop();
            if (!exists) break;
            const [seedKey, seedValue] = exists;
            const seedRange = deserializeRange(seedKey);

            let wasEverFound = false;
            for (const [key, delta] of block.entries()) {
                const range = deserializeRange(key);
                const found = overlapRanges(seedRange, range);

                if (!found) continue;
                wasEverFound = true;
                if (options?.debug) console.log({ found });
                const adjusted = {
                    start: found.start + delta,
                    end: found.end + delta,
                };
                nextSeeds.set(serializeRange(adjusted), delta);

                if (seedRange.start < found.start) {
                    const r = {
                        start: seedRange.start,
                        end: found.start - 1,
                    };
                    seedQueue.push([serializeRange(r), seedValue]);
                }
                if (seedRange.end > found.end) {
                    const r = {
                        start: found.end + 1,
                        end: seedRange.end,
                    };
                    seedQueue.push([serializeRange(r), seedValue]);
                }
            }
            if (!wasEverFound) {
                if (options?.debug) console.log({ seedRange, wasEverFound });
                nextSeeds.set(serializeRange(seedRange), 0);
            }
        }
        currentSeeds = nextSeeds;
    }
    if (options?.debug) console.log({ currentSeeds });

    let output = Number.MAX_SAFE_INTEGER;
    for (const [key, value] of currentSeeds.entries()) {
        const { start, end } = deserializeRange(key);
        const x = start - value;
        if (x < output) output = x;
    }
    return output;
};


const overlapRanges = (range0: Range, range1: Range): Range | undefined => {
    if (range0.end < range1.start || range1.end < range0.start) {
        return undefined;
    }

    const start = Math.max(range0.start, range1.start);
    const end = Math.min(range0.end, range1.end);
    return { start, end: end };
};


const processSeeds2 = (blocks: string[][], options?: {
    debug?: boolean
}): Range[] => {
    const [_seedHeader, seedsString] = blocks[0][0].split(":");
    const seeds = seedsString.trim().split(" ").map(i => parseInt(i));

    const output: Range[] = [];
    for (const i of range(seeds.length / 2)) {
        const start = seeds[i * 2];
        const length = seeds[i * 2 + 1];
        output.push({ start, end: start + length - 1 });
    }
    return output;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const blocks = splitInputs(input);
    const seeds = processSeeds(blocks);

    const blockMaps: Mapping[] = [];
    for (const block of blocks.slice(1)) {
        if (options?.debug) console.log({ block });
        blockMaps.push(processBlock(block, options));
    }

    const locations: number[] = seeds.map(seed => calculateSeed(blockMaps, seed));
    return Math.min(...locations);
};

const calculateSeed = (blockMaps: Mapping[], seed: number): number => {
    let current = seed;
    for (const block of blockMaps) {
        current = getValueFromMap(block, current);
    }
    return current;
};

const processSeeds = (blocks: string[][], options?: {
    debug?: boolean
}): number[] => {
    const [_seedHeader, seedsString] = blocks[0][0].split(":");
    const seeds = seedsString.trim().split(" ").map(i => parseInt(i));
    if (options?.debug) console.log({ seeds });
    return seeds;
};

const processBlock = (block: string[], options?: {
    debug?: boolean
}): Mapping => {
    const output: Map<string, number> = new Map<string, number>();
    for (const line of block.slice(1)) {
        const range = inputToRange(line);
        output.set(serializeRange(range), range.delta || 0);
    }
    return output;
};

const getValueFromMap = (mapping: Mapping, key: number): number => {
    for (const [range, delta] of mapping.entries()) {
        const { start, end } = deserializeRange(range);
        if (key >= start && key < end) return key + delta;
    }
    return key;
};
