import { range } from "../utils";


export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { times, distances } = getRaces2(input);
    console.log({ times, distances });

    const ways: number[] = [];
    for (const i of range(times.length)) {
        let w = 0;
        const time = times[i];
        const distance = distances[i];

        // TODO MARCOS BINARY SEARCH?
        for (const j in range(time)) {
            const d = distanceForTime(time, j);
            if (d > distance) w += 1;
        }
        ways.push(w);
    }

    return ways.reduce((total, next) => next * total, 1);

};

export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    const { times, distances } = getRaces(input);
    console.log({ times, distances });

    const ways: number[] = [];
    for (const i of range(times.length)) {
        let w = 0;
        const time = times[i];
        const distance = distances[i];
        for (const j in range(time)) {
            const d = distanceForTime(time, j);
            if (d > distance) w += 1;
        }
        ways.push(w);
    }

    return ways.reduce((total, next) => next * total, 1);

};

const getRaces2 = (input: string[]) => {
    const [timesHeader, timesRest] = input[0].split(":");

    const times = [parseInt(timesRest.replace(/ /g, ""))];
    const [distanceHeader, distanceRest] = input[1].split(":");
    const distances = [parseInt(distanceRest.replace(/ /g, ""))];

    return { times, distances };
};

const getRaces = (input: string[]) => {
    const [timesHeader, timesRest] = input[0].split(":");
    const times = timesRest.trim().split(/\s+/).map(i => parseInt(i));
    const [distanceHeader, distanceRest] = input[1].split(":");
    const distances = distanceRest.trim().split(/\s+/).map(i => parseInt(i));

    return { times, distances };
};

const distanceForTime = (duration: number, powerUp: number): number => {
    return (duration - powerUp) * powerUp;
};
