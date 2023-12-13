export const range = (count: number): number[] => rangeOf(0, count);

export const rangeOf = (start: number, end: number): number[] =>
    Array.from(Array(end - start)).map((_, i) => i + start);
