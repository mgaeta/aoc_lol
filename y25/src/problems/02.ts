export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    const line = input[0]
    const ranges = line.split(",")
    for (const range of ranges) {
        const parts = range.split("-")
        const start = parseInt(parts[0])
        const end = parseInt(parts[1])

        for (let candidate = start; candidate <= end; candidate += 1) {
            const asString = `${candidate}`;
            for (let root = 1; root <= Math.floor(asString.length / 2); root += 1) {
                let cursor = root
                let previous = asString.substring(0, cursor)
                let found = false;

                while (true) {
                    if (cursor == asString.length) {
                        found = true
                        break
                    }
                    if (cursor + root > asString.length) {
                        break
                    }
                    const next = asString.substring(cursor, cursor + root)
                    if (next != previous) {
                        break
                    }
                    cursor += root
                }

                if (found) {
                    total += candidate;
                    break;
                }
            }
        }
    }
    return total;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    const line = input[0]

    const ranges = line.split(",")
    for (const range of ranges) {
        const parts = range.split("-")
        const start = parseInt(parts[0])
        const end = parseInt(parts[1])

        for (let i = start; i <= end; i += 1) {
            const asString = `${i}`;
            if ((asString.length % 2) != 0) {
                continue;
            }

            const middle = Math.floor(asString.length / 2);

            const a = asString.substring(0, middle);
            const b = asString.substring(middle, end);

            if (a == b) {
                total += i;
            }
        }
    }
    return total;
};

