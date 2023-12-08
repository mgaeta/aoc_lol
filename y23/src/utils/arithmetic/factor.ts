import { rangeOf } from "../array";

export const factor = (n: number, options?: {
    includeObvious?: boolean,
    debug?: boolean
}): number[] => {
    const factors: number[] = [];
    for (const i of rangeOf(2, Math.ceil(Math.sqrt(n)))) {
        if (n % i === 0) {
            factors.push(i);
            factors.push(n / i);
        }
    }
    if (options?.includeObvious) {
        factors.push(1);
        factors.push(n);
    }

    if (options?.debug) console.log({ n, factors });
    return factors;
};
