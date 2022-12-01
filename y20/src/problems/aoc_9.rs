pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");
    let mut numbers: Vec<i64> = Vec::new();
    for i in y {
        if i.len() > 0 {
            numbers.push(i.parse::<i64>().unwrap());
        }
    }

    if verbose {
        println!("- numbers ---------------");
        for i in &numbers {
            println!("{}", i)
        }
        println!("-------------------------");
    }
    let len_preamble = 25;
    let target = 25918798;
    // let len_preamble = 5;
    // let target = 127;

    if true {
      return find_sequence(&numbers, target, verbose);
    } else {
        return find_invalid_entry(&numbers, len_preamble, verbose);
    }
}

fn find_sequence(
    numbers: &Vec<i64>,
    target: i64,
    verbose: bool
) -> u64 {
    let mut queue: Vec<i64> = Vec::new();
    let mut current_sum = 0;
    let mut next_index: usize = 0;

    loop {
        if verbose {
            println!("sum: {}", current_sum);
            print_queue(&queue);
        }
        if current_sum == target {
            if verbose {
                println!("found it");
            }
            print_queue(&queue);
            return 0 as u64;
        } else if current_sum < target {
            queue.push(numbers[next_index]);
            current_sum = current_sum + numbers[next_index];
            next_index = next_index + 1;
        } else {
            let evicted = queue.remove(0);
            current_sum = current_sum - evicted;
        }
        if next_index == numbers.len() {
            panic!("not found");
        }
    }
}


fn find_invalid_entry(
    numbers: &Vec<i64>,
    len_preamble: usize,
    verbose: bool
) -> u64 {
    let mut queue: Vec<i64> = Vec::new();

    for i in 0..len_preamble {
        queue.push(numbers[i]);
    }

    for i in len_preamble..numbers.len() {
        if is_valid(&queue, numbers[i]) {
            if verbose {
                println!("{}", numbers[i]);
            }
            queue.remove(0);
            queue.push(numbers[i]);
        } else {
            return numbers[i] as u64;
        }
    }
    panic!("not found")
}

fn is_valid(queue: &Vec<i64>, target: i64) -> bool {
    for i in queue {
        if !(*i == target - i) && queue.contains(&(target - i)) {
            return true;
        }
    }
    return false;
}

fn print_queue(queue: &Vec<i64>) {
    print!("queue: ");
    for i in queue {
        print!("{} ",i);
    }
    println!("");
}
