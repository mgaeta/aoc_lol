import {
    main01,
    main02,
    main03,
    main04,
    main05,
    main06,
    main07,
    main08,
    main09,
    main10,
    main11,
    main12,
    main13,
    main14,
    main15,
    main16,
    main17,
    main18,
    main19,
    main20,
    main21,
    main22,
    main23,
    main24,
    main25,
} from "./problems";
import { readInput, TestMode, today } from "./utils";

const TEST_MODE = TestMode.ALL;

const getMain = () => {
    switch (today) {
        case "01":
            return main01;
        case "02":
            return main02;
        case "03":
            return main03;
        case "04":
            return main04;
        case "05":
            return main05;
        case "06":
            return main06;
        case "07":
            return main07;
        case "08":
            return main08;
        case "09":
            return main09;
        case "10":
            return main10;
        case "11":
            return main11;
        case "12":
            return main12;
        case "13":
            return main13;
        case "14":
            return main14;
        case "15":
            return main15;
        case "16":
            return main16;
        case "17":
            return main17;
        case "18":
            return main18;
        case "19":
            return main19;
        case "20":
            return main20;
        case "21":
            return main21;
        case "22":
            return main22;
        case "23":
            return main23;
        case "24":
            return main24;
        case "25":
            return main25;
        default:
            throw new Error(`Unknown day ${today}`);
    }
};

(async () => {
    const main = getMain();
    // await pull();
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
