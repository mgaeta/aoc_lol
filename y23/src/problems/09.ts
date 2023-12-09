import { range } from "../utils";
import { cardinality } from "../utils/set";


const prepareInput = (input: string[]): number[][] =>
    input.map(line => line.split(" ").map(i => parseInt(i)));

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> =>
    prepareInput(input).reduce(
        (total, numbers) =>
            total + predictPreviousNumber(numbers),
        0
    );

const computeDeltas = (numbers: number[]): number[] =>
    range(numbers.length - 1).map(i => numbers[i + 1] - numbers[i]);

const predictPreviousNumber = (numbers: number []): number =>
    numbers[0] -
    cardinality(numbers) === 1
        ? 0
        : predictPreviousNumber(computeDeltas(numbers));

const predictNextNumber = (numbers: number []): number =>
    numbers[numbers.length - 1] +
    cardinality(numbers) === 1
        ? 0
        : predictNextNumber(computeDeltas(numbers));

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> =>
    prepareInput(input).reduce(
        (total, numbers) =>
            total + predictNextNumber((numbers)),
        0
    );

