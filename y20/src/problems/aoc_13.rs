pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let chunks: Vec<&str> = y.into_iter().collect();
    let mut bus_ids: Vec<usize> = Vec::new();
    get_bus_ids(&mut bus_ids, chunks[1], verbose);
    if verbose {
        print_bus_ids(&bus_ids);
    }
    if false {
        let target = chunks[0].parse::<usize>().unwrap();
        return step_one(target, &bus_ids, verbose);
    } else {
        return step_two(&bus_ids, verbose);
    }
}

fn step_one(target: usize, bus_ids: &Vec<usize>, verbose: bool) -> u64 {
    let mut smallest_gap = u32::MAX as usize;
    let mut correct_bus = 0;

    for bus_id in bus_ids  {
        let mut current = *bus_id;
        if *bus_id == 0 {
            continue;
        }
        while current < target {
            current = current + *bus_id;
        }
        if verbose {
            println!("bus {} current {}", bus_id, current);
        }
        let gap = current - target;
        if gap < smallest_gap {
            smallest_gap = gap;
            correct_bus = *bus_id;
        }
    }
    if verbose {
        println!("smallest gap {}", smallest_gap);
        println!("correct_bus {}", correct_bus);
    }
    return (smallest_gap * correct_bus) as u64;
}

fn step_two(bus_ids: &Vec<usize>, verbose: bool) -> u64 {
    let mut last_answer = 0 as u64;

    for buses_to_consider in 1..bus_ids.len() {
        if verbose {
            println!("---- considering {} buses ------", buses_to_consider);
        }
        let mut guess = last_answer;
        loop {
            if verbose {
                println!("guess {}", guess);
            }
            let mut is_valid = true;
            for i in 0..buses_to_consider+1 {
                let bus_id = bus_ids[i];
                if bus_id == 0 {
                    continue;
                }
                let next_time = guess + i as u64;
                let gap = next_time % bus_id as u64;
                if gap > 0 as u64 {
                    is_valid = false;
                    break;
                }
            }
            if is_valid {
                last_answer = guess;
                break;
            }
            let mut big_number = 1;
            for i in 0..buses_to_consider {
                if bus_ids[i] > 0 {
                    big_number = big_number * bus_ids[i];
                }
            }
            guess = guess + big_number as u64;
        }
    }
    return last_answer;
}

fn get_bus_ids(bus_ids: &mut Vec<usize>, line: &str, verbose: bool) {
    for i in line.split(","){
        let mut next = 0;
        if i != "x" {
            next = i.parse::<usize>().unwrap();
        }
        bus_ids.push(next);
    }
}

fn print_bus_ids(bus_ids: &Vec<usize>) {
    println!("- bus_ids ------------");
    for i in bus_ids {
        println!("{}", i);
    }
}
