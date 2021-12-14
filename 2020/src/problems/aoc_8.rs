use std::collections::HashSet;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut original_instructions: Vec<(String, i32)> = Vec::new();
    for i in y {
        parse_line(i, &mut original_instructions, verbose);
    }

    for flip_index in 0..original_instructions.len() {
        if verbose {
            println!("--- flip {} ---------------------", flip_index);
        }
        let (op, _) = &original_instructions[flip_index];
        if *op == "acc" {
            continue;
        }

        let mut instructions = Vec::new();
        get_instructions_copy(
            &original_instructions,
            &mut instructions,
            flip_index,
            verbose
        );

        if verbose {
            print_instruction_set(&instructions);
        }

        let mut visited_indexes: HashSet<usize> = HashSet::new();
        let mut current_index: usize = 0;
        let mut accumulator: i32 = 0;
        loop {
            if verbose {
                println!("  {}", current_index);
            }
            if current_index >= instructions.len() {
                return accumulator as u64;
            }

            if visited_indexes.contains(&current_index) {
                break;
            }
            visited_indexes.insert(current_index);

            let (operation, value) = &instructions[current_index];
            match &(*operation)[..] {
                "nop" => {
                    current_index = current_index + 1;
                }
                "acc" => {
                    accumulator = accumulator + *value;
                    current_index = current_index + 1;
                }
                "jmp" => {
                    current_index = (current_index as i32 + *value) as usize ;
                }
                _ => {
                    panic!("bad operation")
                }
            }
        }
    }
    panic!("left the loop");
}

fn parse_line(
    line: &str,
    instructions: &mut Vec<(String, i32)>,
    verbose: bool
) {
    let split: Vec<&str> = line.split(" ").collect();
    if split.len() < 2 {
        return;
    }

    let operation = split[0];
    let value = split[1].parse::<i32>().unwrap();

    instructions.push((operation.to_string(), value));
}

fn get_instructions_copy(
    original_instructions: &Vec<(String, i32)>,
    instructions: &mut Vec<(String, i32)>,
    flip_index: usize,
    verbose: bool
) {
    for i in 0..original_instructions.len() {
        let (operation, value) = &original_instructions[i];


        let new_operation = if i == flip_index {
            match &(*operation)[..] {
                "nop" => "jmp",
                "jmp" => "nop",
                _ => panic!("bad instruction")
            }
        } else {
            &(*operation)[..]
        };

        if verbose {
            println!("{} {} {}", i, *operation, new_operation);
        }
        instructions.push((new_operation.to_string(), *value));
    }
}

fn print_instruction_set(instructions: &Vec<(String, i32)>) {
    for (a, b) in instructions {
        println!("{} {}", a, b);
    }
}
