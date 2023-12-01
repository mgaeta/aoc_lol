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

    // TODO MARCOS assuming there is a blank line at the end might be too dangerous.
    return dataRaw.trim().split("\n");
};
