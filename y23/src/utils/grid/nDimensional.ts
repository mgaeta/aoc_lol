import { range } from "../array";

const SEPARATOR = ":";

export type Point = number[];

export const parsePoint = (pointString: string): Point =>
    pointString.split(SEPARATOR).map(i => parseInt(i));

export const serializePoint = (point: Point): string => point.join(SEPARATOR);


/**
 *  Get a list of candidate neighbor points in N-dimensional space.
 *  TODO get neighbors at radius or in "t-shape".
 *
 * @param point                 The base point.
 * @param [options]
 * @param [options.debug]       When true, display log lines.
 * @param [options.includeSelf] When true, include base point in output.
 * @param [options.maxPoint]    When present, the "bottom-leftmost" point in a
 *                              grid. The point does not need to be a
 *                              two-dimensional vector. When omitted, assume
 *                              that the grid is _infinite_.
 */
export const getNeighbors = (
    point: Point,
    options?: {
        debug?: boolean
        includeSelf?: boolean,
        maxPoint?: Point,
        minPoint?: Point,
    }
): Set<string> => {
    const dimensionality = validateDimensionality(point, options);

    // This will have to be RECURSIVE.
    const deltaTable = getDeltaTable(dimensionality);

    const output: Set<string> = new Set();
    for (const deltas of deltaTable) {
        const candidate = point.map((v, index) => v + deltas[index]);
        if (
            isInBounds(candidate, options)
        ) {
            output.add(serializePoint(candidate));
        }
    }
    if (!options?.includeSelf) output.delete(serializePoint(point));
    if (options?.debug) console.log({ point, output });
    return output;
};

export const getDeltaTable = (dimensionality: number): number[][] => {
    if (!dimensionality) return [[]];

    const output: number[][] = [];
    for (const t of getDeltaTable(dimensionality - 1)) {
        for (const i of [-1, 0, 1]) {
            output.push([...t, i]);
        }
    }
    return output;
};

const validateDimensionality = (
    basePoint: Point,
    options?: {
        maxPoint?: Point,
        minPoint?: Point,
    }
): number => {
    const b = serializePoint(basePoint);
    if (options?.maxPoint && basePoint.length !== options.maxPoint.length) {
        const m = serializePoint(options.maxPoint);
        throw new Error(`Max point (${m}) does not match dimensionality of base point (${b})`);
    }
    if (options?.minPoint && basePoint.length !== options.minPoint.length) {
        const m = serializePoint(options.minPoint);
        throw new Error(`Min point (${m}) does not match dimensionality of base point (${b})`);
    }
    return basePoint.length;
};

const isInBounds = (
    point: Point,
    options?: {
        minPoint?: Point
        maxPoint?: Point
    }
): boolean => {
    const dimensionality = validateDimensionality(point, options);
    return (
        // Assume infinite grid.
        (!options?.maxPoint && !options?.minPoint) ||
        range(dimensionality).every(i => (
            (point[i] >= (options?.minPoint ? options.minPoint[i] : 0)) ||
            (point[i] <= (options?.maxPoint ? options.maxPoint[i] : Number.MAX_SAFE_INTEGER))
        ))
    );
};
