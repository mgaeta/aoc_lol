import { readFile, writeFile } from "fs/promises";
import { parse } from "ini";
import path from "path";
import fetch from "node-fetch";

import { currentYear, today, todayRaw } from "./utils/today";

const BASE_URL = "https://adventofcode.com";
const CONFIG_FILENAME = "config.ini";

export const pull = async (): Promise<void> => {
    const data = await readFile(path.join("..", CONFIG_FILENAME), "utf-8");
    const { token, email } = parse(data)["secrets"];
    const sourceUrl = path.join(BASE_URL, currentYear, "day", todayRaw, "input");
    const destinationPath = path.join("inputs", `${today}.txt`);

    // Read
    const response = await fetch(sourceUrl, {
        headers: {
            "User-Agent": email,
            Cookie: `session=${token}`
        },
    });
    const text = await response.text();

    // Write
    await writeFile(destinationPath, text);
};

pull();
