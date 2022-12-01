use std::fs::File;
use std::io::prelude::*;


pub fn get_input_filename_for_problem(problem: &str, test_mode: bool) -> String {
    if test_mode {
        return format!("inputs/{}_test.txt", problem);
    } else {
        return format!("inputs/{}.txt", problem);
    }
}

pub fn read_input(filename: String) -> String {
    let mut file = File::open(filename).expect("file not found");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("read_to_string failed somehow");
    return contents;
}

// TODO
// pub fn read_input_as_int_list(filename: String) -> String {}
