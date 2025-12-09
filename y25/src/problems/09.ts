export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const points: string[] = []

    const reverseIndex = new Map<string, number>()
    let index = 0
    for (const line of input) {
        const parts = line.split(',');
        reverseIndex.set(line, index++)
        points.push(line)
    }

    let maxArea = -1
    for (const p0 of points) {
        const parts0 = p0.split(',');
        const x0 = parseInt(parts0[0])
        const y0 = parseInt(parts0[1])

        for (const p1 of points) {
            if (p0 === p1) {
                continue
            }

            const parts1 = p1.split(',');
            const x1 = parseInt(parts1[0])
            const y1 = parseInt(parts1[1])

            const deltaX = Math.abs(x1 - x0)
            const deltaY = Math.abs(y1 - y0)
            const nextArea = (deltaY + 1) * (deltaX + 1)

            if (nextArea > maxArea) {
                // this is a candidate!

                const minX = Math.min(x0, x1)
                const maxX = Math.max(x0, x1)
                const minY = Math.min(y0, y1)
                const maxY = Math.max(y0, y1)

                let found = false
                for (const p2 of points) {
                    if (p0 === p2 || p1 === p2) {
                        continue
                    }

                    const parts2 = p2.split(',');
                    const x2 = parseInt(parts2[0])
                    const y2 = parseInt(parts2[1])

                    const nextIndex = (reverseIndex.get(p2)! + 1) % points.length;


                    const p3 = points[nextIndex]
                    const parts3 = p3.split(',');
                    const x3 = parseInt(parts3[0])
                    const y3 = parseInt(parts3[1])

                    if (!(
                        (y2 >= maxY && y3 >= maxY) ||
                        (y2 <= minY && y3 <= minY) ||
                        (x2 >= maxX && x3 >= maxX) ||
                        (x2 <= minX && x3 <= minX)
                    )){
                        found = true
                        break
                    }
                }
                if (!found) {
                    maxArea = nextArea
                }
            }
        }
    }

    return maxArea;
};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const points: string[] = []

    for (const line of input) {
        const parts = line.split(',');
        points.push(line)
    }

    let maxArea = -1
    for (const p0 of points) {
        const parts0 = p0.split(',');
        const x0 = parseInt(parts0[0])
        const y0 = parseInt(parts0[1])

        for (const p1 of points) {
            if (p0 === p1) {
                continue
            }

            const parts1 = p1.split(',');
            const x1 = parseInt(parts1[0])
            const y1 = parseInt(parts1[1])

            const deltaX = Math.abs(x1 - x0)
            const deltaY = Math.abs(y1 - y0)
            const nextArea = (deltaY + 1) * (deltaX + 1)
            maxArea = Math.max(maxArea, nextArea)
        }
    }
    return maxArea;
};


