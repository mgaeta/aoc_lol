use std::collections::HashMap;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut game_board: HashMap<(i32, i32, i32, i32), char> = HashMap::new();
    let lines: Vec<&str> = y.collect();
    for row in 0..lines.len() {
        let line = lines[row];
        if line.len() <= 0 {
            continue;
        }

        let chars: Vec<char> = line.chars().collect();
        for column in 0..chars.len() {
            let i = chars[column];
            &game_board.insert((row as i32, column as i32, 0, 0),i);
        }
    }

    let steps = 6;
    for i in 0..steps {
        if verbose {
            println!("{} {}", i, count_active(&game_board, verbose));
        }

        let mut new_game_board: HashMap<(i32, i32, i32, i32), char> = HashMap::new();
        step(&game_board, &mut new_game_board, verbose);
        game_board = new_game_board.clone();
    }

    return count_active(&game_board, verbose) as u64;
}

fn step(
    old_game_board: &HashMap<(i32, i32, i32, i32), char>,
    new_game_board: &mut HashMap<(i32, i32, i32, i32), char>,
    verbose: bool
) {
    let mut queue: Vec<(i32, i32, i32, i32)> = Vec::new();
    for (&a, _) in old_game_board {
        queue.push(a);
    }

    while !queue.is_empty() {
        let (x, y, z, w) = queue.pop().unwrap();
        let val = match old_game_board.get(&(x, y, z, w)) {
            Some(&v) => v,
            _ => '.',
        };
        if verbose {
            println!("get({},{},{},{}) {}", x, y, z, w, val);
        }

        // first, get the candidates.
        let mut candidates: Vec<(i32, i32, i32, i32)> = Vec::new();
        get_neighbor_coordinates(
            &old_game_board,
            &mut candidates,
            x,
            y,
            z,
            w,
            verbose
        );

        let mut count= 0;
        for &(nx, ny, nz, nw) in &candidates {
            match old_game_board.get(&(nx, ny, nz, nw)) {
                Some('#') => {
                    count += 1;
                },
                Some('.') => (),
                None => {
                    if val == '#' && !old_game_board.contains_key(&(nx, ny, nz, nw)) {
                        if verbose {
                            println!("adding ({},{},{},{})", nx, ny, nz, nw);
                        }
                        queue.push((nx, ny, nz, nw));
                    }
                },
                _ => {
                    panic!("asdf")
                }
            }
        }
        if verbose {
            println!("count ({},{},{},{}) {}", x, y, z, w, count);
        }

        let next_val = if val == '.' && count == 3 {
            '#'
        } else if val == '#' && count <= 3 && count >= 2 {
            '#'
        } else {
            '.'
        };
        new_game_board.insert((x, y, z, w), next_val);
    }
}

fn count_active(game_board: &HashMap<(i32, i32, i32, i32), char>, verbose: bool) -> usize {
    let mut count= 0;
    for (_, &val) in game_board {
        if val == '#' {
            count += 1;
        }
    }
    return count;
}


fn get_neighbor_coordinates(
    game_board: &HashMap<(i32, i32, i32, i32), char>,
    candidates: &mut Vec<(i32, i32, i32, i32)>,
    x: i32,
    y: i32,
    z: i32,
    w: i32,
    verbose: bool
) -> () {
    for row in -1..2 {
        for column in -1..2 {
            for stack in -1..2 {
                for hyper in -1..2 {
                    // Don't add self
                    if row == 0 && column == 0 && stack == 0 && hyper == 0 {
                        continue;
                    }

                    let new_row = x + row;
                    let new_column = y + column;
                    let new_stack = z + stack;
                    let new_hyper = w + hyper;

                    &candidates.push((new_row, new_column, new_stack, new_hyper));
                }
            }
        }
    }
}
