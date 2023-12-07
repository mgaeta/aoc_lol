import { range } from "../utils";

enum Category {
    HIGH_CARD = 0,
    ONE_PAIR = 1,
    TWO_PAIR = 2,
    THREE_OAK = 3,
    FULL_HOUSE = 4,
    FOUR_OAK = 5,
    FIVE_OAK = 6,
}

type Entry = {
    hand: string,
    bet: number,
}

const CARDS_ORDER_0 = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
};

const CARDS_ORDER = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 0,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
};


const sortEntries = (a: Entry, b: Entry): number => {
    for (const i of range(a.hand.length)) {
        const value = CARDS_ORDER[b.hand.charAt(i)] - CARDS_ORDER[a.hand.charAt(i)];
        if (value !== 0) return value;
    }
    throw new Error("bad card sort");
};

const histogram = (handString: string): Map<string, number> => {
    const output = new Map<string, number>();
    for (const char of handString.split("")) {
        const found = output.get(char);
        if (!found) {
            output.set(char, 1);
        } else {
            output.set(char, found + 1);
        }
    }
    return output;
};


const categorize = (hand: string): Category => {
    const frequencies = histogram(hand);
    let pairCount = 0;
    let threeCount = 0;
    let fourCount = 0;

    const jokers = frequencies.get("J");
    frequencies.delete("J");
    const jokerCount = jokers || 0;

    if (jokerCount >= 4) return Category.FIVE_OAK;

    for (const [card, count] of frequencies.entries()) {
        if (count === 5) return Category.FIVE_OAK;
        if (count === 4) fourCount += 1;
        if (count === 3) threeCount += 1;
        if (count === 2) pairCount += 1;
    }

    if (jokerCount === 0) {
        if (fourCount) return Category.FOUR_OAK;
        if (threeCount && pairCount) return Category.FULL_HOUSE;
        if (threeCount) return Category.THREE_OAK;
        if (pairCount >= 2) return Category.TWO_PAIR;
        if (pairCount) return Category.ONE_PAIR;
        return Category.HIGH_CARD;
    }
    if (jokerCount === 1) {
        if (fourCount) return Category.FIVE_OAK;
        if (threeCount) return Category.FOUR_OAK;
        if (pairCount >= 2) return Category.FULL_HOUSE;
        if (pairCount) return Category.THREE_OAK;
        return Category.ONE_PAIR;
    }
    if (jokerCount === 2) {
        if (threeCount) return Category.FIVE_OAK;
        if (pairCount) return Category.FOUR_OAK;
        return Category.THREE_OAK;
    }
    if (jokerCount === 3) {
        if (pairCount) return Category.FIVE_OAK;
        return Category.FOUR_OAK;
    }
    throw new Error(`joker count is out of control lol ${jokerCount}`);
};

const categorize0 = (hand: string): Category => {
    const frequencies = histogram(hand);
    let pairCount = 0;
    let threeCount = 0;

    for (const [card, count] of frequencies.entries()) {
        if (count === 5) return Category.FIVE_OAK;
        if (count === 4) return Category.FOUR_OAK;
        if (count === 3) threeCount += 1;
        if (count === 2) pairCount += 1;
    }

    if (threeCount && pairCount) return Category.FULL_HOUSE;
    if (threeCount) return Category.THREE_OAK;
    if (pairCount >= 2) return Category.TWO_PAIR;
    if (pairCount) return Category.ONE_PAIR;
    return Category.HIGH_CARD;
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const categories: Map<Category, Entry[]> = new Map<Category, Entry[]>;

    for (const line of input) {
        const [hand, betString] = line.split(" ");
        const bet = parseInt(betString);
        const category = categorize(hand);
        const nextEntry: Entry = { hand, bet };

        if (options?.debug) console.log({ hand, category });

        const found = categories.get(category);
        if (!found) {
            categories.set(category, [nextEntry]);
        } else {
            found.push(nextEntry);
            categories.set(category, found);
        }
    }

    let finalEntries: Entry[] = [];
    for (const category of [
        Category.FIVE_OAK,
        Category.FOUR_OAK,
        Category.FULL_HOUSE,
        Category.THREE_OAK,
        Category.TWO_PAIR,
        Category.ONE_PAIR,
        Category.HIGH_CARD
    ]) {
        const entries = categories.get(category);
        if (!entries) continue;
        entries.sort(sortEntries);
        for (const entry of entries) {
            finalEntries.push(entry);
        }
    }

    finalEntries.reverse();

    let total = 0;
    for (const i of range(finalEntries.length)) {
        const entry = finalEntries[i];
        if (options?.debug) console.log({ entry });
        total += (i + 1) * entry.bet;
    }

    return total;
};
