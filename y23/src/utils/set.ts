export const intersection = <T>(a: Set<T>, b: Set<T>): Set<T> =>
    new Set<T>(Array.from(a).filter(n => b.has(n)));

export const union = <T>(a: Set<T>, b: Set<T>): Set<T> =>
    new Set<T>([...Array.from(a), ...Array.from(b)]);

export const difference = <T>(a: Set<T>, b: Set<T>): Set<T> =>
    new Set<T>(Array.from(a).filter(n => !b.has(n)));

export const cardinality = <T>(input: T[] | Set<T>): number => {
    return new Set(input).size;
};
