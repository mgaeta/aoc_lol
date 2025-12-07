export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const board: string[][] = []
    let beamCount: number[] = Array(input[0].length).fill(0)
    for (let y = 0; y < input.length; y += 1) {
        board.push([])
        const line = input[y]

        for (let x = 0; x < line.length; x+= 1) {
            const found = line.charAt(x);
            if (found == "S") {
                beamCount[x] += 1
            }
            board[y][x] = found
        }
    }

    let y = 0
    while (y < input.length - 1) {
        let nextBeamCount: number[] = Array.from(beamCount)
        for (let x = 0; x < input[y].length; x += 1) {
            if (board[y][x] == "^") {
                nextBeamCount[x] = 0
                if (x > 0) {
                    nextBeamCount[x - 1] += beamCount[x]
                }
                if (x < input[y].length - 1) {
                    nextBeamCount[x + 1] += beamCount[x]
                }
            }
        }

        beamCount = nextBeamCount
        y += 1
    }

    let count = 0
    for (const item of beamCount) {
        count += item
    }

    return count;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let count = 0;

    const board: string[][] = []
    let sources: Set<number> = new Set()
    for (const _ of input) {
        for (let y = 0; y < input.length; y += 1) {
            board.push([])
            const line = input[y]

            for (let x = 0; x < line.length; x+= 1) {
                const found = line.charAt(x);
                if (found == "S") {
                    sources.add(x)
                }
                board[y][x] = found
            }
        }
    }

    let y = 0

    while (y < input.length - 1) {
        let nextSources: Set<number> = new Set();
        for (const source of sources) {
            const next = board[y+1][source]
            if (next === "^") {
                count += 1
                nextSources.add(source + 1)
                nextSources.add(source - 1)
            } else {
                nextSources.add(source)
            }
        }

        sources = nextSources
        y += 1
    }
    return count;
};


