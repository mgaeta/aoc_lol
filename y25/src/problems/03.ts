
export const inner = (
    input: string[],
    count: number,
    options?: {
        debug?: boolean
    }
): string => {
    // base case: no more to find
    if (count == 0) {
        return ""
    }

    // base case: there are exactly enough digits left
    if (input.length == count) {
        return input.join("")
    }

    const leftIndex = findMaxIndex(input, count)
    return input[leftIndex] + inner(input.slice(leftIndex + 1), count -1, options)
}

export const findMaxIndex = (
    input: string[],
    count: number,
    options?: {
        debug?: boolean
    }
): number => {
    let maxLeft = -1
    let leftIndex = -1
    for (let i = 0; i < input.length - count + 1; i += 1) {
        const battery = parseInt(input[i])
        if (battery > maxLeft) {
            maxLeft = battery
            leftIndex = i
        }
    }
    return leftIndex
}



export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        const found = inner(line.split(""), 12)
        total += parseInt(found)

    }
    return total;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        const parts = line.split("")

        let maxLeft = -1
        let previousMax = -1
        let leftIndex = 0

        for (let i = 0; i < parts.length; i += 1) {
            const battery = parseInt(parts[i])
            if (battery > maxLeft) {
                previousMax = maxLeft
                maxLeft = battery
                leftIndex = i
            }
        }

        if (leftIndex == parts.length - 1) {
            total += parseInt(previousMax + parts[leftIndex])
        } else {
            let maxRight = -1
            let rightIndex = parts.length - 1
            for (let i = leftIndex+1; i < parts.length; i += 1) {
                const battery = parseInt(parts[i])
                if (battery > maxRight) {
                    maxRight = battery
                    rightIndex = i
                }
            }
            total += parseInt(parts[leftIndex] + parts[rightIndex])
        }
    }
    return total;
};

