import { range } from "../utils";

const HASH_PRIME = 17;
const HASH_MAX = 256;

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const boxes: [string, number][][] = range(HASH_MAX).map(i => []);

    for (const part of input[0].split(",")) {
        if (part.includes("=")) {
            const [label, valueString] = part.split("=");
            const value = parseInt(valueString);
            const relevantBoxI = hashString(label);

            const before = boxes[relevantBoxI];

            let found: number | undefined = undefined;
            for (const j of range(before.length)) {
                const [bLabel, bValue] = before[j];
                if (bLabel === label) found = j;
            }

            const after = before;
            if (found !== undefined) {
                after[found] = [label, value];
            } else {
                after.push([label, value]);
            }
            boxes[relevantBoxI] = after;
        } else {
            // Remove case.
            const [label] = part.split("-");
            const relevantBoxI = hashString(label);

            const before = boxes[relevantBoxI];
            const after = before.filter(([bLabel, _]) => bLabel != label);
            boxes[relevantBoxI] = after;
        }
        if (options?.debug) printBoxes(boxes);
    }

    let total = 0;
    for (const i of range(boxes.length)) {
        let j = 0;
        for (const [_, value] of boxes[i]) {
            if (options?.debug) console.log({ i, j, value });
            total += (i + 1) * value * (j + 1);
            j += 1;
        }
    }
    return total;
};

const printBoxes = (boxes: [string, number][][]): void => {
    for (const i of range(boxes.length)) {
        let output = "";
        for (const [label, value] of boxes[i]) {
            output += `[${label} ${value}]`;
        }
        if (output) console.log(`Box ${i}: ` + output);
    }
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> =>
    input[0].split(",").reduce((total, part) => total + hashString(part));


const hashString = (input: string): number => {
    let output = 0;
    for (const char of input) {
        output += getAscii(char);
        output *= HASH_PRIME;
        output = output % HASH_MAX;
    }
    return output;
};

const getAscii = (char: string): number => char.charCodeAt(0);

