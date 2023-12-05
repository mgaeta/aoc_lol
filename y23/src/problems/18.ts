export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        if (options?.debug) console.log({ line });
        total += 1;
    }
    return total;
};
