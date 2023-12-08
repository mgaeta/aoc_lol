import { range } from "../utils";

const START_NODE = "AAA";
const END_NODE = "ZZZ";

type DictionaryEntry = {
    left: string;
    right: string;
}

const getNextDirection = (line0: string, index: number): string =>
    line0.charAt(index % line0.length);

const factor = (n: number): number[] => {
    const output: number[] = [];
    for (const i of range(n - 1)) {
        if (n % (i + 1) === 0) {
            output.push(i + 1);
        }
    }
    return output;
};

const leastCommonMultiple = (nn: number[]): number => {
    const allFactors = new Set<number>();
    for (const n of nn) {
        const factors = factor(n);
        for (const f of factors) {
            allFactors.add(f);
        }
    }
    return Array.from(allFactors).reduce((product, next) => product * next, 1);
};

const prepareDictionary = (input: string[], options?: {
    debug?: boolean
}): Map<string, DictionaryEntry> => {
    const dictionary: Map<string, DictionaryEntry> = new Map<string, DictionaryEntry>();
    for (const line of input.slice(2)) {
        if (options?.debug) console.log({ line });
        const [name, values] = line.split(" = ");
        const [left, right] = values.slice(1, values.length - 1).split(", ");

        const entry = { left, right };
        dictionary.set(name, entry);
    }
    return dictionary;
};

const getStartNodes = (dictionary: Map<string, DictionaryEntry>): string[] =>
    Array.from(dictionary.keys()).filter(i => i.charAt(2) === "A");

const isEndNode = (node: string): boolean => node.charAt(2) === "Z";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const line0 = input[0];
    const dictionary = prepareDictionary(input);

    const totals: number[] = [];
    const allThreads: string[] = getStartNodes(dictionary);
    for (const thread of allThreads) {
        let i = 0;
        let next = thread;
        while (!isEndNode(next)) {
            if (options?.debug) console.log({ next, i });
            const l = getNextDirection(line0, i);
            const found = dictionary.get(next);
            if (!found) throw new Error(`bad direction ${l}`);
            next = l === "L" ? found.left : found.right;
            i += 1;
        }
        totals.push(i);
    }

    console.log({ totals });
    return leastCommonMultiple(totals);
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const line0 = input[0];
    const dictionary = prepareDictionary(input);

    let i = 0;
    let next = START_NODE;
    while (next != END_NODE) {
        if (options?.debug) console.log({ next, i });
        const l = getNextDirection(line0, i);
        const found = dictionary.get(next);
        if (!found) throw new Error(`bad direction ${l}`);
        next = l === "L" ? found.left : found.right;
        i += 1;
    }
    return i;
};
