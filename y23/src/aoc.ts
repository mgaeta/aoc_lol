import { main } from "./problems";
import { pull, readInput, TestMode } from "./utils";

const TEST_MODE = TestMode.ALL;

(async () => {
    await pull();
    if ([TestMode.ALL, TestMode.ON].includes(TEST_MODE)) {
        const input = await readInput({ test: TestMode.ON });
        const result = await main(input, { debug: true });
        console.log("- test ------------");
        console.log(result);
        console.log("- /test -----------");
    }
    if ([TestMode.ALL, TestMode.OFF]) {
        const input = await readInput({ test: TestMode.OFF });
        const result = await main(input, { debug: false });
        console.log("===================");
        console.log(result);
        console.log("===================");
    }
})();
