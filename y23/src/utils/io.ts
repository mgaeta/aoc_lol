import path from "path";
import { readFile } from "fs/promises";

import { TestMode } from "./tests";
import { today } from "./today";

export const readInput = async (options?: {
    day?: string,
    test?: TestMode,
}) => {
    const { day, test } = options || {};

    const optionalSuffix = test === TestMode.ON ? "_test" : "";
    const inputFilename = `${day || today}${optionalSuffix}.txt`;
    const inputFilePath = path.join("inputs", inputFilename);
    console.log({ inputFilePath });

    const dataRaw = await readFile(inputFilePath, { encoding: "utf8" });

    return dataRaw.trim().split("\n");
};


export const splitInputs = (input: string[]): string[][] => {
    const output: string[][] = [];
    let buffer: string[] = [];
    for (const line of input) {
        if (line === "") {
            output.push(buffer);
            buffer = [];
        } else {
            buffer.push(line);
        }
    }
    // Finally, flush the rest of the buffer.
    output.push(buffer);
    return output;
};
