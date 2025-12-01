export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let currentPosition = 50;
    let count = 0;

    for (const line of input) {
        const isLeft =  line.charAt(0) == "L"
        let x = parseInt(line.substring(1))

        count += Math.floor(x / 100)

        let nextPosition = currentPosition
        if (isLeft) {
            nextPosition -= x % 100
        } else {
            nextPosition += x % 100
        }

        if (
            (nextPosition > 0 && currentPosition < 0) ||
            (nextPosition < 0 && currentPosition > 0) ||
            (nextPosition > 100 && currentPosition < 100) ||
            (nextPosition < -100 && currentPosition > -100)
        ) {
            count  += 1
        }

        currentPosition = nextPosition % 100
        if (currentPosition == 0) {
            count += 1
        }

    }
    return count;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let currentPosition = 50;
    let count = 0;

    for (const line of input) {
        const isLeft =  line.charAt(0) == "L"
        const x = parseInt(line.substring(1))
        let next = currentPosition
        if (isLeft) {
            next -= x
        } else {
            next += x
        }

        currentPosition = next % 100

        if (currentPosition == 0) {
            count += 1
        }

    }
    return count;
};


