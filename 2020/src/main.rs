mod utils;
mod problems;

use std::collections::HashSet;
use std::env;
/**
    The main function should remain simple. Its only responsibility is to read
    command line arguments to determine which problem to execute and then print
    the output.
*/
fn main() {
    let args: Vec<String> = env::args().collect();
    let problem_id = &args[args.len()-1];

    let is_test_mode = collect_flag(&args, "t");
    let is_verbose = collect_flag(&args, "v");
    let is_fetch_mode = collect_flag(&args, "f");

    if is_fetch_mode {
        return fetch(problem_id)
    }

    let filename = utils::io::get_input_filename_for_problem(problem_id, is_test_mode);
    let input_as_string = utils::io::read_input(filename);
    let answer = match &problem_id[..] {
        "1" => problems::aoc_1::main(input_as_string, is_verbose),
        "2" => problems::aoc_2::main(input_as_string, is_verbose),
        "3" => problems::aoc_3::main(input_as_string, is_verbose),
        "4" => problems::aoc_4::main(input_as_string, is_verbose),
        "5" => problems::aoc_5::main(input_as_string, is_verbose),
        "6" => problems::aoc_6::main(input_as_string, is_verbose),
        "7" => problems::aoc_7::main(input_as_string, is_verbose),
        "8" => problems::aoc_8::main(input_as_string, is_verbose),
        "9" => problems::aoc_9::main(input_as_string, is_verbose),
        "10" => problems::aoc_10::main(input_as_string, is_verbose),
        "11" => problems::aoc_11::main(input_as_string, is_verbose),
        "12" => problems::aoc_12::main(input_as_string, is_verbose),
        "13" => problems::aoc_13::main(input_as_string, is_verbose),
        "14" => problems::aoc_14::main(input_as_string, is_verbose),
        "15" => problems::aoc_15::main(input_as_string, is_verbose),
        "16" => problems::aoc_16::main(input_as_string, is_verbose),
        "17" => problems::aoc_17::main(input_as_string, is_verbose),
        "18" => problems::aoc_18::main(input_as_string, is_verbose),
        "19" => problems::aoc_19::main(input_as_string, is_verbose),
        "20" => problems::aoc_20::main(input_as_string, is_verbose),
        "21" => problems::aoc_21::main(input_as_string, is_verbose),
        "22" => problems::aoc_22::main(input_as_string, is_verbose),
        "23" => problems::aoc_23::main(input_as_string, is_verbose),
        "24" => problems::aoc_24::main(input_as_string, is_verbose),
        "25" => problems::aoc_25::main(input_as_string, is_verbose),
        "26" => problems::aoc_26::main(input_as_string, is_verbose),
        _ => 0,
    };

    println!("{}", answer);
    println!("Done!");
}

fn fetch(problem_id: &str) {
    let filename = utils::io::get_input_filename_for_problem(problem_id, false);
    // if the file already exists, abort
    // get the session from configs? commandline?
    // download the data
    // write to file.
}


fn collect_flag(args: &Vec<String>, flag: &str) -> bool {
    let flags = &args[1..args.len()-1];
    let mut x = HashSet::new();
    for f in flags {
        let chars: Vec<char> = f.chars().collect();
        for ch in chars {
            x.insert(ch.to_string());
        }
    }
    return x.contains(&flag.to_string());
}
