import { factor } from "./factor";

export const leastCommonMultiple = (nn: number[], options?: {
    debug?: boolean
}): number => {
    const allFactors = new Set<number>();
    for (const n of nn) {
        const factors = factor(n);
        for (const f of factors) {
            allFactors.add(f);
        }
    }
    const output = Array.from(allFactors).reduce((product, next) => product * next, 1);
    if (options?.debug) console.log({ nn, allFactors, output });
    return output;
};
