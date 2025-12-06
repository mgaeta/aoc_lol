export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let count = 0;

    const operators = input.pop()!.trim().split(/\s+/).reverse()

    const board: string[][] = []

    for (let y = 0; y < input.length; y += 1) {
        board.push([])
        const line = input[y]

        for (let x = line.length -1; x >= 0; x -= 1) {
            board[y][x] = line.charAt(x)
        }
    }

    const problems: number[][] = []
    let currentProblem: number[] = []
    for (let x = board[0].length; x >= 0; x -= 1) {
        let accumulator = ""
        for (let y = 0; y < board.length; y += 1) {
            accumulator += board[y][x] || ""
        }
        if (accumulator === (" ".repeat(board.length))) {
            problems.push(currentProblem)
            currentProblem = []
        } else {
            const n = parseInt(accumulator.trim())
            if (!isNaN(n)) {
                currentProblem.push(n)
            }
        }
    }
    problems.push(currentProblem)

    for (let i = 0; i < problems.length; i += 1) {
        const operator = operators[i]
        let total
        if (operator === "+") {
            total = 0
        } else {
            total = 1
        }
        for (const x of problems[i]) {
            if (operator === "+") {
                total += x
            } else {
                total *= x
            }
        }
        count += total
    }

    return count;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let count = 0;


    const problems: number[][] = []

    const lastline = input.pop()!.trim()
    const llparts = lastline.split(/\s+/)
    for (const _ of llparts) {
        problems.push([])
    }

    for (const line of input) {
        const parts = line.trim().split(/\s+/)
        for (let i = 0; i < parts.length; i+= 1) {
            const part = parts[i]
            const next = parseInt(part)
            problems[i].push(next)
        }
    }

    for (let i = 0; i < llparts.length; i += 1) {
        const operator = llparts[i]
        let total
        if (operator === "+") {
            total = 0
        } else {
            total = 1
        }

        for (const x of problems[i]) {
            if (operator === "+") {
                total += x
            } else {
                total *= x
            }
        }
        count += total
    }

    return count;
};


