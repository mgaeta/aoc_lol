use std::collections::HashMap;
use regex::Regex;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n").collect();

    let public_key_card = y[0].parse::<usize>().unwrap();
    let public_key_door = y[1].parse::<usize>().unwrap();

    let max_loop_size = 100000000;

    let secret = 20201227;
    if verbose {
        println!("{} {}", public_key_card, public_key_door);
    }

    // example: 14897079

    // 84779276
    let mut card_loop= 0;
    let mut card_value = 1;
    for i in 0..max_loop_size {
        card_value = calculate(
            card_value,
            7,
            1,
            secret,
            verbose
        );
        if card_value == public_key_card {
            card_loop = i+1;
        }
    }
    println!("card loop {} ", card_loop);

    return calculate(
    1,
    public_key_door,
    84779276,
        secret,
        verbose
    ) as u64;

    // 19344394
}


fn calculate(
    start: usize,
    subject_number: usize,
    loop_size: usize,
    secret: usize,
    verbose: bool
) -> usize {
    let mut output = start;
    for i in 0..loop_size {
        output = output * subject_number;
        output = output % secret;
    }
    // println!("{}: {}", loop_size, output);
    return output;
}
