use std::collections::HashMap;
use regex::Regex;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n").collect();

    let mut lines: Vec<Vec<String>> = Vec::new();
    for i in y {
        if i.len() <= 0 {
            continue;
        }
        parse_line(i, &mut lines, verbose);
    }

    let mut tiles: Vec<HashMap<String, i32>> = Vec::new();
    calculate_tiles(&lines, &mut tiles, verbose);

    if verbose {
        print_lines(&lines);
        print_tiles(&tiles);
    }

    let mut answers: HashMap<(i32,i32), usize> = HashMap::new();
    get_answers(&tiles, &mut answers, verbose);

    let rounds = 100;
    // let rounds = 10;
    for i in 0..rounds {
        if verbose {
            println!("{} => {}", i, sum_answers(&answers, verbose));
        }

        let mut middle_answers: HashMap<(i32,i32), usize> = HashMap::new();
        for (&(x, y), count) in &answers {
            let mut neighbors: Vec<(i32, i32)> = Vec::new();
            get_neighbors(x, y, &mut neighbors, verbose);
            for (nx, ny) in neighbors {
                let k = (nx, ny);
                let nc = answers.get(&k).unwrap_or(&0);
                if nc % 2 == 0 {
                    middle_answers.insert(k, 0);
                }
            }

            let b = is_tile_black(x, y, &answers, verbose);
            if b {
                middle_answers.insert((x,y), 1);
            } else {
                middle_answers.insert((x,y), 0);
            }
        }
        answers = middle_answers;

        let mut next_answers: HashMap<(i32,i32), usize> = HashMap::new();
        for (&(x, y), count) in &answers {
            // let mut neighbors: Vec<(i32, i32)> = Vec::new();
            // get_neighbors(x,y, &mut neighbors, verbose);
            // for (nx, ny) in neighbors {
            //     let k = (nx, ny);
            //     let nc = answers.get(&k).unwrap_or(&0);
            //     if nc % 2 == 0 {
            //         next_answers.insert(k, 0);
            //     }
            // }

            let count = count_neighbors(x,y, &answers, verbose);
            let black = is_tile_black(x, y, &answers, verbose);
            let key = (x, y);
            if black {
                if count == 0 || count > 2 {
                    next_answers.insert(key, 0);
                } else {
                    next_answers.insert(key, 1);
                }
            } else if !black && count == 2 {
                next_answers.insert(key, 1);
            }
        }
        answers = next_answers;

    }

    return sum_answers(&answers, verbose) as u64
}

fn count_neighbors(
    x: i32,
    y: i32,
    answers: &HashMap<(i32,i32), usize>,
    verbose: bool
) -> usize {
    let mut neighbors: Vec<(i32, i32)> = Vec::new();
    get_neighbors(x, y, &mut neighbors, verbose);
    let mut output = 0;
    for (nx, ny) in neighbors {
        if is_tile_black(nx, ny, answers, verbose) {
            output += 1;
        }
    }
    return output;
}

fn get_neighbors(
    x: i32,
    y: i32,
    neighbors: &mut Vec<(i32, i32)>,
    verbose: bool,
) {
    neighbors.push((x + 1, y + 0));
    neighbors.push((x + 1, y - 1));
    neighbors.push((x + -1, y + 0));
    neighbors.push((x + -1, y + 1));
    neighbors.push((x + 0, y + 1));
    neighbors.push((x + 0, y - 1));
}

fn is_tile_black(
    x: i32,
    y: i32,
    answers: &HashMap<(i32,i32), usize>,
    verbose: bool
) -> bool {
    let key = (x, y);
    return answers.get(&key).unwrap_or(&0) % 2 == 1;
}

fn sum_answers(
    answers: & HashMap<(i32,i32), usize>,
    verbose: bool
) -> usize {
    let mut output = 0;
    println!("==");
    for ((x,y), c) in answers {
        if verbose {
            // println!("({},{})={}", x,y, c)
        }
        if c % 2 == 1 {
            output += 1;
        }
    }
    return output;
}

fn get_answers(
    tiles: &Vec<HashMap<String, i32>>,
    answers: &mut HashMap<(i32,i32), usize>,
    verbose: bool
) {
    for tile in tiles {
        let ne = tile.get(&"ne".to_string()).unwrap();
        let e = tile.get(&"e".to_string()).unwrap();
        let se = tile.get(&"se".to_string()).unwrap();

        let key = (*ne - *se, *e + *se);
        if verbose {
            println!("key: ({},{})", key.0, key.1);
        }
        let prev = answers.get(&key).unwrap_or(&0);
        &answers.insert(key, prev+1);
    }
}

fn calculate_tiles(
    lines: &Vec<Vec<String>>,
    tiles: &mut Vec<HashMap<String, i32>>,
    verbose: bool
) {
    for line in lines {
        let mut coordinates: HashMap<String, i32> = HashMap::new();
        coordinates.insert("e".to_string(), 0);
        coordinates.insert("ne".to_string(), 0);
        coordinates.insert("se".to_string(), 0);

        for i in line {
            let mut to_add = 0;
            let mut dir: String;
            let (dir, to_add) = match i.as_str() {
                "sw" => ("ne", -1),
                "se" => ("se", 1),
                "nw" => ("se", -1),
                "ne" => ("ne", 1),
                "w" => ("e", -1),
                "e" => ("e", 1),
                _ => panic!("bad dir")
            };

            let prev = coordinates.get(&dir.to_string()).unwrap();
            &coordinates.insert(dir.to_string(), prev + to_add);
        }
        tiles.push(coordinates);
    }
}

fn parse_line(
    line: &str,
    lines: &mut Vec<Vec<String>>,
    verbose: bool
) {
    let mut output: Vec<String> = Vec::new();
    let re = Regex::new(r"(se)|(sw)|(nw)|(ne)|(e)|(w)").unwrap();

    for i in re.find_iter(line).map(|x| x.as_str()) {
        output.push(i.to_string());
    }

    lines.push(output);
}

fn print_lines(lines: &Vec<Vec<String>>) {
    println!("- lines -------------------------");
    for line in lines {
        print!("line:");
        for i in line {
            print!(" {}", i);
        }
        println!("");
    }
}

fn print_tiles(tiles: &Vec<HashMap<String, i32>>) {
    println!("- tiles -------------------------");
    for tile in tiles {
        print!("tile:");
        for (dir, val) in tile {
            print!(" {}.{}", dir, val);
        }
        println!("");
    }
}
