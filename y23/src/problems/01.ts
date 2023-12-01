import { range } from "../utils";

const TABLE: { [key: string]: number } = {
    "eight": 8,
    "five": 5,
    "four": 4,
    "nine": 9,
    "one": 1,
    "seven": 7,
    "six": 6,
    "three": 3,
    "two": 2,
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        const foundDigits: number[] = [];
        for (const lastIndex of range(line.length)) {
            const lastCharacter = parseInt(line.charAt(lastIndex));
            if (isNaN(lastCharacter)) {
                for (const j of range(lastIndex)) {
                    const found: number = TABLE[line.substring(lastIndex - j - 1, lastIndex + 1)];
                    if (found) {
                        foundDigits.push(found);
                        break;
                    }
                }
            } else {
                foundDigits.push(lastCharacter);
            }
        }
        total += foundDigits[0] * 10 + foundDigits[foundDigits.length - 1];
    }
    return total;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const i of input) {
        const foundDigits: number[] = [];
        for (const c of i.split("")) {
            const r = parseInt(c);
            if (isNaN(r)) continue;
            foundDigits.push(r);
        }
        total += foundDigits[0] * 10 + foundDigits[foundDigits.length - 1];
    }

    return total;
};


