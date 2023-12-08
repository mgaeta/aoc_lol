import { leastCommonMultiple } from "../utils/arithmetic";

const START_NODE = "AAA";
const END_NODE = "ZZZ";

type DictionaryEntry = {
    left: string;
    right: string;
}

const getNextDirection = (directions: string, index: number): string =>
    directions.charAt(index % directions.length);

const prepareDictionary = (input: string[], options?: {
    debug?: boolean
}): Map<string, DictionaryEntry> => {
    const dictionary: Map<string, DictionaryEntry> = new Map<string, DictionaryEntry>();
    for (const line of input.slice(2)) {
        if (options?.debug) console.log({ line });
        const [name, values] = line.split(" = ");
        const [left, right] = values.slice(1, values.length - 1).split(", ");
        dictionary.set(name, { left, right });
    }
    return dictionary;
};

const getStartNodes = (dictionary: Map<string, DictionaryEntry>): string[] =>
    Array.from(dictionary.keys()).filter(i => i.charAt(2) === "A");

const isEndNode = (node: string): boolean => node.charAt(2) === "Z";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const directions = input[0];
    const dictionary = prepareDictionary(input);

    const totals: number[] = [];
    const allThreads: string[] = getStartNodes(dictionary);
    for (const thread of allThreads) {
        let i = 0;
        let next = thread;
        while (!isEndNode(next)) {
            if (options?.debug) console.log({ next, i });
            const direction = getNextDirection(directions, i);
            const found = dictionary.get(next);
            if (!found) throw new Error(`bad direction ${direction}`);
            next = direction === "L" ? found.left : found.right;
            i += 1;
        }
        totals.push(i);
    }

    return leastCommonMultiple(totals, options);
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const directions = input[0];
    const dictionary = prepareDictionary(input);

    let i = 0;
    let next = START_NODE;
    while (next != END_NODE) {
        if (options?.debug) console.log({ next, i });
        const direction = getNextDirection(directions, i);
        const found = dictionary.get(next);
        if (!found) throw new Error(`bad direction ${direction}`);
        next = direction === "L" ? found.left : found.right;
        i += 1;
    }
    return i;
};
