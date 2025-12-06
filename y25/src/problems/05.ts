export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let count = 0;

    const ranges = new Map<number, number>();

    let maxNumber = -1
    for (const line of input) {
        if (line == "") {
            break
        }
        const parts = line.split("-")
        const start = parseInt(parts[0])
        const end = parseInt(parts[1])

        const found = ranges.get(start)
        ranges.set(start, Math.max(found || -1, end))

        maxNumber = Math.max(maxNumber, end)
    }

    const sortedKeys = Array.from(ranges.keys()).sort((a, b)  => {return a - b;})

    let maxIncluded = -1
    for (let i = 0; i < sortedKeys.length; i += 1) {
        const start = sortedKeys[i]
        const end = ranges.get(start)!
        const actualStart = Math.max(maxIncluded + 1, start)

        maxIncluded = Math.max(maxIncluded, end)

        count += Math.max(end - actualStart + 1, 0)
    }

    return count;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let count = 0;

    const ranges = new Map<number, number>();

    let startMode = true
    for (const line of input) {
        if (startMode) {
            const parts = line.split("-")
            const start = parseInt(parts[0])
            const end = parseInt(parts[1])

            const found = ranges.get(start)
            ranges.set(start, Math.max(found || -1, end))

            if (line == "") {
                startMode = false
            }
        } else {
            const itemId = parseInt(line)
            let found = false
            for (const [key, value] of ranges.entries()) {
                if (itemId >= key && itemId <= value) {
                    found = true
                    break
                }
            }
            if (found) {
                count += 1
            }
        }

    }
    return count;
};


