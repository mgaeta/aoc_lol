use std::collections::HashMap;
use std::thread::current;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n").collect();

    let mut ring: Vec<usize> = Vec::new();
    for i in y[0].chars() {
        ring.push(i.to_string().parse::<usize>().unwrap());
    }

    let mut library: HashMap<usize, (usize, usize)> = HashMap::new();
    fill_library(&ring, &mut library, verbose);
    let root = ring[0];


    let moves = 10000000;
    let max_value = 1000000;

    pad_ring(root, &mut library, max_value, verbose);

    if verbose {
        print_library(&ring, &library);
    }


    let mut current = root;
    for i in 0..moves {
        if i % 100000 == 0 {
            println!("{}", i);
        }
        if verbose {
            println!("== move {} =================", i+1);
        }
        perform_loop(current, &mut library, max_value, verbose);
        let (before, after) = library.get(&current).unwrap();
        current = *after;
        if verbose {
            print_library(&ring, &library);
        }
    }

    let (_, x) = library.get(&1).unwrap();
    let (_, y) = library.get(&x).unwrap();
    println!("{} * {}", x, y);
    return (x * y) as u64
}

fn pad_ring(
    root: usize,
    library: &mut HashMap<usize, (usize, usize)>,
    max_value: usize,
    verbose: bool,
) {

    let &(last, first) = library.get(&root).unwrap();
    let &(before_last, _) = library.get(&last).unwrap();
    for i in 9..max_value {
        library.insert(i+1, (i, i+2));
    }
    library.insert(root, (max_value, first));
    library.insert(last, (before_last, 10));
    library.insert(10, (last, 11));
    library.insert(max_value, (max_value-1, root));
}

fn perform_loop(
    root: usize,
    library: &mut HashMap<usize, (usize, usize)>,
    max_value: usize,
    verbose: bool
) {
    let &(before_root, first) = library.get(&root).unwrap();

    let second = library.remove(&first).unwrap().1;
    let third = library.remove(&second).unwrap().1;
    let fourth = library.remove(&third).unwrap().1;
    let fifth = library.get(&fourth).unwrap().1;

    // first excise the group
    library.insert(root, (before_root, fourth));
    library.insert(fourth, (root, fifth));

    let destination = get_destination(
        root,
        max_value,
        &vec![first, second, third],
        verbose,
    );
    let &(before_destination, after_destination) = library.get(&destination).unwrap();
    let &(_, after_after_destination) = library.get(&after_destination).unwrap();


    if verbose {
        println!("root {}, pick up ({},{},{}), destination {}", root, first, second, third, destination);
    }

    library.insert(first, (destination, second));
    library.insert(second, (first, third));
    library.insert(third, (second, after_destination));
    library.insert(destination, (before_destination, first));
    library.insert(after_destination, (third, after_after_destination));
}

fn get_destination(
    root: usize,
    max_value: usize,
    not_candidates: &Vec<usize>,
    verbose: bool,
) -> usize {
    let mut destination = if root == 1 {
        max_value
    } else {
        root - 1
    };
    while not_candidates.contains(&destination) {
        destination = if destination == 1 {
            max_value
        } else {
            destination - 1
        }
    }
    return destination;
}

fn print_library(
    ring: &Vec<usize>,
    library: &HashMap<usize, (usize, usize)>
) {
    for i in ring {
        match library.get(&i) {
            Some((x,y)) => {
                println!("{} ({},{})", i, x, y);
            }
            _ => ()
        }
    }
}

fn fill_library(
    ring: &Vec<usize>,
    library: &mut HashMap<usize, (usize, usize)>,
    verbose: bool
) {
    for i in 0..ring.len() {
        if i == 0 {
            let before = ring[ring.len() - 1];
            let after = ring[i+1];
            library.insert(ring[i], (before, after));
        } else if i == ring.len() - 1 {
            let before = ring[i-1];
            let after = ring[0];
            library.insert(ring[i], (before, after));
        } else {
            let before = ring[i-1];
            let after = ring[i+1];
            library.insert(ring[i], (before, after));
        }
    }
}
