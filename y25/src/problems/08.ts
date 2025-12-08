export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const board: Map<string, number[]> = new Map()
    for (const line of input) {
        const parts = line.split(",")

        board.set(
            line,
            [
                parseInt(parts[0]),
                parseInt(parts[1]),
                parseInt(parts[2]),
            ],
        )
    }

    const allDistances = new Map<string, number>()

    const clusterMemberships = new Map<string, string>();
    const clusterMembershipsReversed = new Map<string, string[]>();
    let id = 0
    for (const [key0, values0] of board.entries()) {
        for (const [key1, values1] of board.entries()){
            if (key0 === key1) {
                continue
            }
            const distance = Math.sqrt(
                Math.pow(values1[0] - values0[0], 2)
                + Math.pow(values1[1] - values0[1], 2) +
                Math.pow(values1[2] - values0[2], 2)
            )
            const key = `${key0}:${key1}`
            if (!allDistances.has(`${key1}:${key0}`)) {
                allDistances.set(key, distance)
            }
        }
        const circuitName = `${id++}`;
        clusterMemberships.set(key0, circuitName);
        clusterMembershipsReversed.set(circuitName, [key0]);
    }

    const xx = Array.from(allDistances.entries()).sort((
        [_, distance0], [__, distance1]) => {
        return distance1 - distance0
    })

    const memberCounts = new Map<string, number>();
    for (const circuitName of clusterMemberships.values()) {
        let found = memberCounts.get(circuitName)
        if (!found) {
            found = 0
        }


    }
    let lastKey0 = ''
    let lastKey1 = ''
    while (true) {
        const nextKey = xx.pop()
        if (!nextKey) {
            break
        }
        const parts = nextKey[0].split(":");
        const key0 = parts[0]
        const key1 = parts[1]
        const circuitName = clusterMemberships.get(key0)!
        const otherCircuitName = clusterMemberships.get(key1)!

        if (circuitName === otherCircuitName) {
            continue
        }

        lastKey0 = key0
        lastKey1 = key1

        const circuitMembers = clusterMembershipsReversed.get(otherCircuitName)!
        for (const member of circuitMembers) {
            clusterMemberships.set(member, circuitName)
        }
        clusterMembershipsReversed.set(otherCircuitName, [])
        const x = clusterMembershipsReversed.get(circuitName)!
        const nextList = x.concat(circuitMembers)
        clusterMembershipsReversed.set(circuitName, nextList)
        memberCounts.set(circuitName, nextList.length);
        memberCounts.set(otherCircuitName, 0);
        if (nextList.length === input.length) {
            break
        }
    }

    return parseInt(lastKey0.split(",")[0]) * parseInt(lastKey1.split(",")[0])
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const board: Map<string, number[]> = new Map()
    for (const line of input) {
        const parts = line.split(",")

        board.set(
            line,
            [
                parseInt(parts[0]),
                parseInt(parts[1]),
                parseInt(parts[2]),
            ],
        )
    }

    const allDistances = new Map<string, number>()

    const clusterMemberships = new Map<string, string>();
    const clusterMembershipsReversed = new Map<string, string[]>();
    let id = 0
    for (const [key0, values0] of board.entries()) {
        for (const [key1, values1] of board.entries()){
            if (key0 === key1) {
                continue
            }
            const distance = Math.sqrt(
                Math.pow(values1[0] - values0[0], 2)
                + Math.pow(values1[1] - values0[1], 2) +
                Math.pow(values1[2] - values0[2], 2)
            )
            const key = `${key0}:${key1}`
            if (!allDistances.has(`${key1}:${key0}`)) {
                allDistances.set(key, distance)
            }
        }
        const circuitName = `${id++}`;
        clusterMemberships.set(key0, circuitName);
        clusterMembershipsReversed.set(circuitName, [key0]);
    }

    const xx = Array.from(allDistances.entries()).sort((
        [_, distance0], [__, distance1]) => {
        return distance1 - distance0
    })

    // const COUNT = 10 ;
    const COUNT = 1000;
    for (let count = 0; count < COUNT; count ++) {
        const nextKey = xx.pop()
        if (!nextKey) {
            break
        }
        const parts = nextKey[0].split(":");
        const key0 = parts[0]
        const key1 = parts[1]
        const circuitName = clusterMemberships.get(key0)!
        const otherCircuitName = clusterMemberships.get(key1)!

        if (circuitName === otherCircuitName) {
            continue
        }

        const circuitMembers = clusterMembershipsReversed.get(otherCircuitName)!
        for (const member of circuitMembers) {
            clusterMemberships.set(member, circuitName)
        }
        clusterMembershipsReversed.set(otherCircuitName, [])
        const x = clusterMembershipsReversed.get(circuitName)!
        clusterMembershipsReversed.set(circuitName, x.concat(circuitMembers))
    }


    const memberCounts = new Map<string, number>();
    for (const circuitName of clusterMemberships.values()) {
        let found = memberCounts.get(circuitName)
        if (!found) {
            found = 0
        }

        memberCounts.set(circuitName, found + 1);
    }

    const ordered = Array.from(memberCounts.entries()).sort((
            [_, count0], [__, count1]) => {
            return count1 - count0
        }
    )

    return ordered[0][1] * ordered[1][1] * ordered[2][1];
};


