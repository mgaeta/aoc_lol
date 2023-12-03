const NUMBER_DICTIONARY = "1234567890";

const TABLE: { [key: string]: number } = {
    "eight": 8,
    "five": 5,
    "four": 4,
    "nine": 9,
    "one": 1,
    "seven": 7,
    "six": 6,
    "three": 3,
    "two": 2,
    "zero": 0,
};

export const isCharacterANumber = (character: string): boolean =>
    NUMBER_DICTIONARY.includes(character);

export const parseNumberWord = (word: string): number | undefined => TABLE[word];
