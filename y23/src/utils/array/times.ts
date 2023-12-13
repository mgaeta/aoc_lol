import { range } from "./range";

export const concatTimes = <T>(input: T[], times: number): T[] =>
    range(times).reduce((output, i) => output.concat(input), [] as T[]);
