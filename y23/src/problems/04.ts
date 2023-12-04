import { range } from "../utils";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const results = await prepareResults(input, options);

    const copies = Object.fromEntries(range(input.length).map(i => [i + 1, 0]));

    let cardsToProcess = range(input.length).map(i => i + 1);
    while (cardsToProcess.length) {
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

export const prepareResults = async (input: string[], options?: {
    debug?: boolean
}): Promise<Map<number, number>> => {
    // mapping ID to number of intersections
    const results = new Map<number, number>();

    for (const line of input) {
        // Keep this line around so that it can be quickly duplicated.
        if (options?.debug) console.log(line);

        const [card, rest] = line.split(": ");
        const [_, idString] = card.split("Card");
        const id = parseInt(idString.trim());
        const [winning, have] = rest.split(" | ");
        const winningNumbers = new Set(
            winning.trim().split(/\s+/).map(i => parseInt(i.trim()))
        );
        const haveNumbers = new Set(
            have.trim().split(/\s+/).map(i => parseInt(i.trim()))
        );

        results.set(id, Array.from(haveNumbers).filter(n => winningNumbers.has(n)).length);
    }
    return results;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const results = await prepareResults(input, options);
    let total = 0;
    for (const [_, intersectionCount] of results.entries()) {
        if (intersectionCount >= 1) {
            total += 2 ** (intersectionCount - 1);
        }
    }

    return total;
};
