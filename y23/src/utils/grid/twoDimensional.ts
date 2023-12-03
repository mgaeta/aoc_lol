import { getNeighbors as getNeighborsNDimensional } from "./nDimensional";

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
): Set<string> =>
    getNeighborsNDimensional(
        [point.x, point.y], {
            includeSelf: false,
            maxPoint: [options.length, options.width]
        }
    );
