use regex::Regex;
use std::collections::HashMap;


pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut instructions: Vec<String> = Vec::new();
    let mut memory: HashMap<usize, usize> = HashMap::new();
    for i in y {
        if i.len() > 0 {
            instructions.push(i.to_string());
        }
    }

    if verbose {
        print_instructions(&instructions);
    }
    run_program(&instructions, &mut memory, verbose);

    return sum_memory(&memory, verbose) as u64;
}

fn run_program(
    instructions: &Vec<String>,
    memory: &mut HashMap<usize, usize>,
    verbose: bool
){
    let mut current_mask: Vec<char> = Vec::new();

    for i in instructions {
        if i.starts_with("mask") {
            parse_mask(i, &mut current_mask, verbose);
        } else {
            if true {
                let (address, value) = parse_assignment(i, verbose);

                let mut masked_addresses: Vec<usize> = Vec::new();
                mask_address(
                    &current_mask,
                    &mut masked_addresses,
                    address,
                    verbose
                );
                for masked_address in masked_addresses {
                    memory.insert(masked_address, value);
                }
            } else {
                let (address, value) = parse_assignment(i, verbose);
                let masked_value = mask_value(&current_mask, value, verbose);
                memory.insert(address, masked_value);
            }
        }
    }
}

fn mask_address(
    current_mask: &Vec<char>,
    masked_addresses: &mut Vec<usize>,
    address: usize,
    verbose: bool
) {
    let mut address_as_bits: Vec<char> = Vec::new();
    let mut address_copy = address;
    while address_copy > 0 {
        let next = match address_copy % 2 {
            0 => '0',
            1 => '1',
            _ => 'X',
        };

        address_as_bits.push(next);
        address_copy >>= 1;
    }
    for i in 0..(36-address_as_bits.len()) {
        address_as_bits.push('0');
    }
    address_as_bits.reverse();

    let mut candidates: Vec<usize> = Vec::new();
    candidates.push(0);

    let mut next_candidates: Vec<usize> = Vec::new();

    for i in 0..36 {
        let next = match current_mask[i] {
            '0' => {
                for candidate in candidates {
                    let new_candidate = candidate << 1;
                    let value = match address_as_bits[i] {
                        '1' => 1,
                        _ => 0,
                    };
                    next_candidates.push(new_candidate + value);
                }
            },
            '1' => {
                for candidate in candidates {
                    next_candidates.push((candidate << 1) + 1);
                }
            },
            _ => {
                for candidate in candidates {
                    next_candidates.push((candidate << 1) + 1);
                    next_candidates.push(candidate << 1);
                }
            },
        };

        candidates = next_candidates;
        next_candidates = Vec::new();
    }

    for c in candidates {
        &masked_addresses.push(c);
    }
}

fn mask_value(current_mask: &Vec<char>, value: usize, verbose: bool) -> usize {
    let mut mask_1 = 0;
    let mut mask_2 = 0;
    for i in current_mask {
        let next = match i {
            'X' => 1,
            _ => 0,
        };
        mask_1 <<= 1; // push
        mask_1 += next;
    }

    for i in current_mask {
        let next = match i {
            '1' => 1,
            _ => 0,
        };
        mask_2 <<= 1; // push
        mask_2 += next;
    }

    if verbose {
        println!("mask_1 {} mask_2 {}", mask_1, mask_2);
    }

    return (mask_1 & value) | mask_2;
}

fn parse_assignment(assignment_string: &str, verbose: bool) -> (usize, usize) {
    let re = Regex::new(r"^mem\[(\d+)\] = (\d+)$").unwrap();
    let captures = re.captures(assignment_string).unwrap();

    let address = captures.get(1).map_or("", |m| m.as_str()).parse::<usize>().unwrap();
    let value = captures.get(2).map_or("", |m| m.as_str()).parse::<usize>().unwrap();

    if verbose {
        println!("mem[{}] = {}", address, value);
    }
    return (address, value);
}

fn parse_mask(mask_string: &str, mask: &mut Vec<char>, verbose: bool) {
    let re = Regex::new(r"^mask = (.*)$").unwrap();
    let captures = re.captures(mask_string).unwrap();

    let value = captures.get(1).map_or("", |m| m.as_str());
    if verbose {
        println!("captures[1] = {}", value);
    }
    *mask = value.chars().collect();
}


fn sum_memory(memory: &HashMap<usize, usize>, verbose: bool) -> usize {
    let mut sum = 0;
    if verbose {
        println!("- memory ---------------");
    }
    for (k, v) in memory {
        if verbose {
            println!("m[{}]= {}", k, v);
        }
        sum += v;
    }
    return sum;
}

fn print_instructions(instructions: &Vec<String>) {
    println!("- instructions ---------------");
    for i in instructions {
        println!("{}", i);
    }
    println!("------------------------------");
}
