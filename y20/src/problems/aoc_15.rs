use std::collections::HashMap;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut inputs: Vec<usize> = Vec::new();
    let mut index: HashMap<usize, usize> = HashMap::new();
    for i in y {
        if i.len() > 0 {
            let next = i.parse::<usize>().unwrap();
            inputs.push(next);
            index.insert(next, inputs.len() - 1);
        }
    }

    index.remove(inputs.last().unwrap());


    let count_to = 30000000;
    // let count_to = 2020;
    // let count_to = 10;
    for i in 0..(count_to - inputs.len()) {
        if i % 10000 == 0 {
            println!("{}", i);
        }
        let next_number = get_next_number(&inputs, &mut index, verbose);
        inputs.push(next_number);
    }

    // the idea is to look for patterns


    if verbose {
        println!("- inputs ----------");
        for i in &inputs {
            println!("{}", i);
        }
        println!("-------------------");
    }

    return *inputs.last().unwrap() as u64;
}


fn get_next_number(inputs: &Vec<usize>, index: &mut HashMap<usize, usize>, verbose: bool) -> usize {
    let current_index = inputs.len() - 1;
    let last_number = *inputs.last().unwrap();
    if verbose {
        println!("current_index {} last_number {}", current_index, last_number);
    }

    let last_seen = match index.get(&last_number) {
        Some(last_seen) => current_index - *last_seen,
        None => 0
    };
    if verbose {
        println!("last_seen {}", last_seen);
    }

    index.insert(last_number, current_index);

    return last_seen;

}

