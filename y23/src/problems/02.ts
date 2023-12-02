const LIMITS = {
    "blue": 14,
    "green": 13,
    "red": 12,
};

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const game of input) {
        const maximums = {
            "red": 0,
            "green": 0,
            "blue": 0,
        };
        const [_, rest0] = game.split(":");
        const rolls = rest0.split(";").map(i => i.trim());

        for (const game of rolls) {
            const items = game.split(", ");
            for (const item of items) {
                const [count, color] = item.split(" ");
                if (options?.debug) console.log({ count, color });
                maximums[color] = Math.max(maximums[color], parseInt(count));
            }
        }
        total += maximums["red"] * maximums["green"] * maximums["blue"];
    }
    return total;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const game of input) {
        const [part0, rest0] = game.split(":");
        const [_, idString] = part0.split(" ");
        const rolls = rest0.split(";").map(i => i.trim());

        let isGameValid = true;
        for (const game of rolls) {
            const items = game.split(", ");
            for (const item of items) {
                const [count, color] = item.split(" ");
                if (options?.debug) console.log({ count, color });
                if (LIMITS[color] < parseInt(count)) {
                    isGameValid = false;
                    break;
                }
            }
        }
        if (isGameValid) {
            total += parseInt(idString);
        }

    }
    return total;
};

