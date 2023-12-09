import { range } from "../utils";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        if (options?.debug) console.log({ line });
        const digits = line.split(" ").map(i => parseInt(i));
        const x = predictPreviousNumber(digits);
        total += x;
    }
    return total;
};

const predictPreviousNumber = (numbers: number []): number => {
    const allValues = new Set(numbers);
    if (allValues.size === 1) return Array.from(allValues).pop()!;

    const deltas: number[] = [];
    for (const i of range(numbers.length - 1)) {
        deltas.push(numbers[i + 1] - numbers[i]);
    }
    const next = predictPreviousNumber(deltas);
    return numbers[0] - next;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        if (options?.debug) console.log({ line });
        const digits = line.split(" ").map(i => parseInt(i));
        const x = predictNextNumber(digits);
        total += x;
    }
    return total;
};

const predictNextNumber = (numbers: number []): number => {
    const allValues = new Set(numbers);
    if (allValues.size === 1) return Array.from(allValues).pop()!;

    const deltas: number[] = [];
    for (const i of range(numbers.length - 1)) {
        deltas.push(numbers[i + 1] - numbers[i]);
    }
    const next = predictNextNumber(deltas);
    return numbers[numbers.length - 1] + next;
};
