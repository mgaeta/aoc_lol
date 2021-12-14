use std::collections::HashMap;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n").collect();

    let tests = [
        (100,        100),
    ].to_vec();

    for (play_count, max_int) in tests {
        let (a,b) = part_two(
            y[0].chars().collect(),
            play_count,
            max_int,
            verbose
        );
        println!("{}, {}, ({},{})", play_count, max_int, a, b);
    }


    return 0 as u64
}

fn part_two(
    y: Vec<char>,
    play_count: usize,
    max_int: usize,
    verbose: bool
) -> (usize, usize) {
    let mut cache: HashMap<String, usize> = HashMap::new();
    let mut ring: Vec<usize> = Vec::new();
    for i in y {
        ring.push(i.to_string().parse::<usize>().unwrap());
    }

    let pickup_count = 3;
    let init_size = ring.len();


    for i in init_size..max_int {
        ring.push(i+1);
    }

    if verbose {
        println!("{}", ring.len());
        for i in &ring {
            println!("{}", i);
        }
    }

    let mut answer: String;

    for j in 0..play_count {
        if j % 100000 == 0 {
            println!("{}", j);
        }

        let pivot = ring[0];
        let mut middle = ring[1..4].to_vec();
        let mut right = ring[4..].to_vec();

        let destination = get_destination(pivot, max_int, &right);


        if verbose {
            println!("- round {} -------------------------------", j+1);
            println!("cups ({}){}{}", pivot, array_to_string(&middle), array_to_string(&right));
            println!("pick up: {}", array_to_string(&middle));
            println!("right: {}", array_to_string(&right));
            println!("dest: {}", destination);
            println!("--------------------------------");
        }

        let mut put_in_0 = true;
        let mut split_0: Vec<usize> = Vec::new();
        let mut split_1: Vec<usize> = Vec::new();
        for i in right {
            if i == destination {
                put_in_0 = false;
            } else if put_in_0 {
                split_0.push(i);
            } else {
                split_1.push(i);
            }
        }

        let mut output: Vec<usize> = Vec::new();
        output.append(&mut split_0);
        output.push(destination);
        output.append(&mut middle);
        output.append(&mut split_1);
        output.push(pivot);

        if verbose {
            println!("answer: {}", array_to_string(&output));
        }
        answer = array_to_string(&output);
        if cache.contains_key(&answer) {
            println!("PANIC {}", j);
            panic!("DONE");
        }
        cache.insert(answer, j);
        ring = output;
    }


    return find_answer(&ring);
}

fn get_destination(pivot: usize, max_int: usize, right: &Vec<usize>) -> usize {
    let mut next = pivot - 1;
    while !right.contains(&next) {
        if next == 0 {
            next = max_int
        } else {
            next -= 1;
        }
    }
    return next;
}


fn array_to_string(a: &Vec<usize>) -> String {
    return a.iter().map(|x| format!("{} ",x)).collect();
}

fn find_answer(ring: &Vec<usize>) -> (usize, usize) {
    // print!("answer");
    // for i in ring {
    //     print!(" {}", i);
    // }
    // println!("");

    let mut index = 0;
    while ring[index] != 1 {
        index += 1;
    }

    if index == ring.len() -1 {
        return (ring[0], ring[1]);
    }
    if index == ring.len() -2 {
        return (ring[ring.len() - 1], ring[0]);
    }
    return (ring[index + 1], ring[index + 2]);
}
