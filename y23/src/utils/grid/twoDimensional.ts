export type Point = {
    x: number;
    y: number;
}

export const parsePoint = (pointString: string): Point => {
    const parts = pointString.split(":");
    return {
        x: parseInt(parts[0]),
        y: parseInt(parts[1]),
    };
};

export const serializePoint = (point: Point): string => `${point.x}:${point.y}`;


export const getNeighbors = (
    point: Point,
    options: {
        debug?: boolean
        length: number,
        width: number,
    }
): Set<string> => {
    const { length, width } = options;

    const output: Set<string> = new Set();
    const { y, x } = point;
    for (const xx of [-1, 0, 1]) {
        for (const yy of [-1, 0, 1]) {
            if (
                (y + yy >= 0) &&
                (y + yy < length) &&
                (x + xx >= 0) &&
                (x + xx < width)
            ) {
                output.add(serializePoint({
                    x: x + xx,
                    y: y + yy,
                }));
            }
        }
    }
    if (options?.debug) console.log({ point, output });
    return output;
};
