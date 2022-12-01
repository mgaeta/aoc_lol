use std::collections::HashMap;

static acceptable_gaps_len: usize = 3;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut numbers: Vec<usize> = Vec::new();
    numbers.push(0);
    for i in y {
        if i.len() < 1 {
            continue;
        }
        numbers.push(i.parse::<usize>().unwrap());
    }
    let final_joltage = numbers[numbers.len() - 1] + 3;
    // numbers.push(final_joltage);
    numbers.sort();

    if verbose {
        print_numbers(&numbers);
    }

    let mut memo: HashMap<usize, usize> = HashMap::new();

    if false {
        return part_one(&numbers, verbose) as u64;
    } else {
        return part_two(&mut memo, &numbers, 0, verbose) as u64;
    }
}

fn part_two(
    memo: &mut HashMap<usize, usize>,
    numbers: &Vec<usize>,
    head_index: usize,
    verbose: bool
) -> usize {
    match memo.get(&head_index) {
        Some(x) => return *x,
        None => ()
    }

    let current_number = numbers[head_index];
    let final_joltage = numbers[numbers.len() - 1] + 3;

    if verbose {
        println!("current_number {} final_joltage {}", current_number, final_joltage);
    }

    if (final_joltage - current_number) <= 3 {
        if verbose {
            println!("returning 1");
        }
        return 1;
    }

    let mut count = 0;
    for i in 0..acceptable_gaps_len {
        let next_index = head_index + i + 1;
        if next_index >= numbers.len() {
            break;
        }

        if verbose {
            println!("next_index {} numbers[head_index] {}", next_index, numbers[head_index]);
        }
        if (numbers[next_index] - numbers[head_index]) <= acceptable_gaps_len {
            count = count + part_two(memo, numbers,next_index, verbose);
        }
    }

    if verbose {
        println!("count {}", count);
    }
    memo.insert(head_index, count);
     return count;
}

fn part_one(numbers: &Vec<usize>, verbose: bool) -> usize {
    let mut gaps_counts: HashMap<usize, usize> = HashMap::new();

    for i in 0..acceptable_gaps_len+1 {
        gaps_counts.insert(i, 0 as usize);
    }

    let mut prev = 0;
    for i in &numbers[..] {
        let gap = (*i - prev) as usize;

        if verbose {
            println!("calculating {} - {}", *i, prev);
        }

        let new_value = gaps_counts.get(&gap).unwrap() + 1;
        gaps_counts.insert(gap, new_value);
        prev = *i;
    }

    if verbose {
        print_gaps(&gaps_counts);
    }

     // return gaps_counts.get(&1).unwrap() * (gaps_counts.get(&3).unwrap() + 1)  as u64;
    let ones = gaps_counts.get(&1).unwrap();
    let threes = gaps_counts.get(&3).unwrap();
    return ones * (threes + 1);
}

fn print_numbers(numbers: &Vec<usize>) {
    println!("print_numbers");
    for i in &numbers[..] {
        println!("{}", i);
    }
}

fn print_gaps(gaps: &HashMap<usize, usize>) {
    println!("print_gaps");
    for (i, j) in gaps {
        println!("{} {}", i, j);
    }
}
