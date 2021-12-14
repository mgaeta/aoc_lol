use std::collections::HashMap;
use std::iter::FromIterator;
use regex::Regex;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n\n");
    let side_length = 10;

    // Parse tiles
    let mut tiles: HashMap<usize, Vec<char>> = HashMap::new();
    for i in y {
        if i.len() <= 0 {
            continue;
        }

        parse_tile(i, &mut tiles, verbose);
    }

    //
    let mut reverse_index: HashMap<String, Vec<(usize, char)>> = HashMap::new();
    get_reverse_index(&tiles, &mut reverse_index, side_length, verbose);

    if verbose {
        print_tiles(&tiles, side_length);
        print_reverse_index(&reverse_index)
    }

    // TODO maybe these should include orientation?
    let mut corners: Vec<usize> = Vec::new();
    let mut sides: Vec<usize> = Vec::new();
    let mut centers: Vec<usize> = Vec::new();

    get_pieces_by_type(
        &tiles,
        &reverse_index,
        &mut corners,
        side_length,
        2,
        verbose
    );

    get_pieces_by_type(
        &tiles,
        &reverse_index,
        &mut sides,
        side_length,
        3,
        verbose
    );
    get_pieces_by_type(
        &tiles,
        &reverse_index,
        &mut centers,
        side_length,
        4,
        verbose
    );

    if false {
        let mut game_board: Vec<(usize, char)> = Vec::new();
        part_two(
            &mut game_board,
            &tiles,
            &reverse_index,
            &corners,
            &sides,
            &centers,
            verbose
        );

        if verbose {
            print_game_board(&game_board);
        }
        return 0 as u64;
    } else {
        return calculate_answer(&corners) as u64;
    }
}

fn calculate_answer(corners: &Vec<usize>) -> usize {
    let mut product = 1;
    for i in corners {
        product *= i;
    }
    return product
}

fn get_sides(
    tile: &Vec<char>,
    sides: &mut HashMap<char, String>,
    side_length: usize,
    verbose: bool
) {
    let mut left_side: Vec<char> = Vec::new();
    let mut right_side = Vec::new();
    for i in 0..side_length {
        left_side.push(tile[i*side_length]);
        right_side.push(tile[(side_length-1) + i*side_length]);
    }

    sides.insert('t', String::from_iter(&tile[0..side_length]));
    sides.insert('r', String::from_iter(&right_side));
    sides.insert('b', String::from_iter(&tile[side_length*(side_length- 1)..tile.len()]));
    sides.insert('l', String::from_iter(&left_side));
    sides.insert('x', reverse_string(String::from_iter(&tile[0..side_length])));
    sides.insert('y', reverse_string(String::from_iter(right_side)));
    sides.insert('z', reverse_string(String::from_iter(&tile[side_length*(side_length- 1)..tile.len()])));
    sides.insert('w', reverse_string(String::from_iter(left_side)));
}

fn reverse_string(side: String) -> String {
    return String::from_iter(side.chars().rev()).to_string();
}

fn parse_tile(
    lines: &str,
    tiles: &mut HashMap<usize, Vec<char>>,
    verbose: bool
) {
    let x: Vec<&str> = lines.split("\n").collect::<Vec<&str>>();
    let line_0 = x[0];
    let title_regex = Regex::new(r"^Tile (\d+):$").unwrap();
    let captures = title_regex.captures(line_0).unwrap();
    let id: usize = captures.get(1).map_or("", |m| m.as_str()).parse::<usize>().unwrap();

    let mut chars: Vec<char> = Vec::new();
    for i in x[1..x.len()].iter() {
        let mut next_chars = i.chars().collect::<Vec<char>>();
        chars.append(&mut next_chars);
    }

    tiles.insert(id, chars);
}

fn print_tiles(tiles: &HashMap<usize, Vec<char>>, side_length: usize) {
    for (key, tile) in tiles {
        print!("{}: ", key);
        for i in tile {
            print!("{}", i);
        }
        println!("");
        let mut sides: HashMap<char, String> = HashMap::new();
        get_sides(tile, &mut sides, side_length, false);
        for (side_key, side_value) in sides {
            println!("{}: {}", side_key, side_value);
        }
    }
}

fn get_pieces_by_type(
    tiles: &HashMap<usize, Vec<char>>,
    reverse_index: &HashMap<String, Vec<(usize, char)>>,
    corners: &mut Vec<usize>,
    side_length: usize,
    x: usize,
    verbose: bool
) {
    for (&key, tile) in tiles {
        let mut tile_sides: HashMap<char, String> = HashMap::new();
        get_sides(tile, &mut tile_sides, side_length, verbose);

        let mut not_uniques = 0;
        for (orientation, side) in tile_sides {
            let l = match reverse_index.get(&side) {
                Some(v) => v.len(),
                _ => 0
            };
            if l == 2 {
                not_uniques += 1;
            }
        }

        if not_uniques == x {
            if verbose {
                println!("x {}", key);
            }
            corners.push(key);
        }
    }
}

fn get_reverse_index(
    tiles: &HashMap<usize, Vec<char>>,
    reverse_index: &mut HashMap<String, Vec<(usize, char)>>,
    side_length: usize,
    verbose: bool
) {
    for (&key, tile) in tiles {
        let mut sides: HashMap<char, String> = HashMap::new();
        get_sides(tile, &mut sides, side_length, verbose);

        for (orientation, side) in sides {
            let old_tile_ids: Vec<(usize, char)> = match reverse_index.get(&side) {
                Some(t) => t.to_vec(),
                None => Vec::new(),
            };

            let mut answer: Vec<(usize, char)> = Vec::new();
            answer.push((key, orientation));
            for i in old_tile_ids {
                answer.push(i);
            }
            reverse_index.insert(side, answer);
        }
    }
}

fn print_reverse_index(reverse_index: &HashMap<String, Vec<(usize, char)>>,) {
    println!("- reverse ------------------------");
    for (key, value) in reverse_index {
        print!("{}:", key);
        for (i, j) in value {
            print!(" {}.{}", i, j);
        }
        println!("");
    }
    println!("----------------------------------");
}

// TODO for now this returns a single board but I might want to return a list of orientations.
fn part_two(
    game_board: &mut Vec<(usize, char)>,
    tiles: &HashMap<usize, Vec<char>>,
    reverse_index: &HashMap<String, Vec<(usize, char)>>,
    corners: &Vec<usize>,
    sides: &Vec<usize>,
    centers: &Vec<usize>,
    verbose: bool,
) {
    // base case: 0x0
    if centers.len() == 0 {
        return;
    }

    // base case: 1x1
    if centers.len() == 1 {
        game_board.push((centers[0], 't'));
    }

    let first_corner_id = corners[0];
    let first_corner_orientation = 't';

    let mut sequence: Vec<(usize, char)> = Vec::new();
    calculate_sequence(
        &mut sequence,
        0,
        &tiles,
        &corners,
        &sides,
        verbose
    );
}


fn calculate_sequence(
    sequence: &mut Vec<(usize, char)>,
    start: usize,
    tiles: &HashMap<usize, Vec<char>>,
    corners: &Vec<usize>,
    sides: &Vec<usize>,
    verbose: bool,
) {
    // starting with a corner, there will be two sequences.
    // for each direction?
    let mut next_id = start;
    while false {
        sequence.push((next_id, 't'));
        next_id = 0;
    }
}

// TODO why isn't this used?
// TODO there are 8 orientations, not 4!
fn next_orientation(orientation: char) -> char {
    return match orientation {
        't' => 'r',
        'r' => 'b',
        'b' => 'l',
        'l' => 't',
        _ => panic!("bad orientation"),
    }
}

// TODO pass in prev, next?
fn rotate_tile(tile: &Vec<char>, orientation: char) -> Vec<char>{
    // TODO pass in N times?
    let mut new_vec: Vec<char> = Vec::new();

    return new_vec;
}


fn print_game_board(game_board: &Vec<(usize, char)>) {
    println!("- gameboard --------");
    for (i, j) in game_board {
        print!("{} {}", i, j);
    }
    println!("\n--------------------");
}

// If we know corners and sides
// start with a corner at 0
// there will be exactly 1 side that will attach.
//
