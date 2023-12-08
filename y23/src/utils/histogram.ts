export const histogram = <T>(inputs: T[]): Map<T, number> => {
    const output = new Map<T, number>();
    for (const value of inputs) {
        output.set(value, (output.get(value) || 0) + 1);
    }
    return output;
};
