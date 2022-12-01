use std::collections::HashSet;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n\n");

    let mut declarations: Vec<HashSet<char>> = Vec::new();
    for i in y {
        parse_line(&mut declarations, i, verbose);
    }

    let mut count = 0;
    for d in declarations {
        count = count + d.len();
        if verbose {
            println!("{:?}", d.len());
        }
    }

    return count as u64
}

fn parse_line(passports: &mut Vec<HashSet<char>>, line: &str, verbose: bool) {
    let mut started = false;
    let mut declarations: HashSet<char> = HashSet::new();
    let parts = line.split_whitespace();
    for p in parts {
        let mut individual_declarations: HashSet<char> = HashSet::new();
        let char_list: Vec<char> = p.chars().collect();
        for ch in char_list {
            individual_declarations.insert(ch);
        }
        if started {
            let mut overwrite: HashSet<char> = HashSet::new();
            for &a in declarations.intersection(&individual_declarations) {
                overwrite.insert(a);
            }
            declarations = overwrite;

        } else {
            declarations = individual_declarations;
            started = true;
        }
    }

    if verbose {
        println!("{:?}", declarations);
    }

    passports.push(declarations);
}
