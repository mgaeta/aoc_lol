import { range } from "../utils";
import { intersection } from "../utils/set";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const results = await prepareResults(input, options);

    const copies = Object.fromEntries(range(input.length).map(i => [i + 1, 0]));

    let cardsToProcess = range(input.length).map(i => i + 1);
    while (true) {
        const card = cardsToProcess.pop();
        if (!card) break;
        copies[card] += 1;
        for (const i of range(results.get(card) || 0)) {
            cardsToProcess.push(card + i + 1);
        }
    }
    if (options?.debug) console.log({ copies });

    return Object.values(copies).reduce((total, next) => total + next, 0);
};

const parseNumbers = (numberString: string): Set<number> => new Set(
    numberString.trim().split(/\s+/).map(i => parseInt(i.trim()))
);

export const prepareResults = async (input: string[], options?: {
    debug?: boolean
}): Promise<Map<number, number>> => {
    // mapping ID to number of intersections
    const results = new Map<number, number>();

    for (const line of input) {
        // Keep this line around so that it can be quickly duplicated.
        if (options?.debug) console.log(line);

        const [card, rest] = line.split(":");
        const [_, idString] = card.split("Card");
        const id = parseInt(idString.trim());
        const [winning, have] = rest.split("|");
        const winningNumbers = parseNumbers(winning);
        const haveNumbers = parseNumbers(have);

        results.set(id, intersection(haveNumbers, winningNumbers).size);
    }
    return results;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const results = await prepareResults(input, options);

    return Array.from(results.values()).reduce(
        (total, intersectionCount) =>
            total + (
                intersectionCount
                    ? 2 ** (intersectionCount - 1)
                    : 0
            ),
        0
    );
};
