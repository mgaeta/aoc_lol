import { factor } from "./factor";
import { union } from "../set";

export const leastCommonMultiple = (numbers: number[]): number =>
    Array.from(
        numbers.reduce(
            (all, n) =>
                union(all, new Set<number>(factor(n))), new Set<number>()
        )
    ).reduce((product, next) => product * next, 1);
