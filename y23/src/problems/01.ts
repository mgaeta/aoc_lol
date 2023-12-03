import { range } from "../utils";
import { parseNumberWord } from "../utils/string/numbers";

export const main = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const line of input) {
        const foundDigits: number[] = [];
        for (const lastIndex of range(line.length)) {
            const lastCharacter = parseInt(line.charAt(lastIndex));
            if (isNaN(lastCharacter)) {
                for (const j of range(lastIndex)) {
                    const found = parseNumberWord(
                        line.substring(lastIndex - j - 1, lastIndex + 1)
                    );
                    if (found) {
                        foundDigits.push(found);
                        break;
                    }
                }
            } else {
                foundDigits.push(lastCharacter);
            }
        }
        total += foundDigits[0] * 10 + foundDigits[foundDigits.length - 1];
    }
    return total;
};


export const main1 = async (input: string[], options?: {
    debug?: boolean
}): Promise<string | number> => {
    let total = 0;
    for (const i of input) {
        const foundDigits: number[] = [];
        for (const c of i.split("")) {
            const r = parseInt(c);
            if (isNaN(r)) continue;
            foundDigits.push(r);
        }
        total += foundDigits[0] * 10 + foundDigits[foundDigits.length - 1];
    }

    return total;
};


