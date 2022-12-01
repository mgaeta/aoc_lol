use std::collections::{HashMap, HashSet};
use regex::Regex;


pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n\n").collect();

    let rule_lines: Vec<&str> = y[0].split("\n").collect();
    let my_ticket_lines: Vec<&str> = y[1].split("\n").collect();
    let nearby_ticket_lines: Vec<&str> = y[2].split("\n").collect();

    let mut rules: HashMap<String, (usize, usize, usize, usize)> = HashMap::new();
    let mut nearby_tickets: Vec<Vec<usize>> = Vec::new();
    let mut my_tickets: Vec<Vec<usize>> = Vec::new();

    parse_rules(&rule_lines, &mut rules, verbose);
    parse_tickets(&my_ticket_lines, &mut my_tickets, verbose);
    parse_tickets(&nearby_ticket_lines, &mut nearby_tickets, verbose);
    if verbose {
        print_rules(&rules);
        print_tickets(&nearby_tickets);
    }
    if true {
        let mut possible_indexes: HashMap<String, HashSet<usize>> = HashMap::new();
        part_two(
            &mut possible_indexes,
            &rules,
            &nearby_tickets,
            &my_tickets[0],
            verbose
        );

        return part_three(&mut possible_indexes, &my_tickets[0], verbose) as u64;
    } else {
        return part_one(&rules, &nearby_tickets, verbose) as u64;
    }
}


fn part_one(
    rules: &HashMap<String, (usize, usize, usize, usize)>,
    tickets: &Vec<Vec<usize>>,
    verbose: bool
) -> usize {
    let mut count = 0;
    for ticket in tickets {
        for &field in ticket {
            let mut is_valid = false;
            for (rule, &(a, b , c, d)) in rules {
                if in_range(field, a, b, c, d) {
                    is_valid = true;
                    break;
                }
            }
            if !is_valid {
                if verbose {
                    println!("{}", field);
                }
                count += field;
            }
        }
    }
    return count;
}


fn part_two(
    possible_indexes: &mut HashMap<String, HashSet<usize>>,
    rules: &HashMap<String, (usize, usize, usize, usize)>,
    all_tickets: &Vec<Vec<usize>>,
    my_ticket: &Vec<usize>,
    verbose: bool
) {

    for (name, _) in rules {
        let mut set: HashSet<usize> = HashSet::new();
        for i in 0..my_ticket.len() {
            set.insert(i);
        }
        possible_indexes.insert(name[..].to_string(), set);
    }

    for ticket in all_tickets {
        for field_index in 0..ticket.len() {
            let field = ticket[field_index];

            // First pass is just to check total validity.
            let mut is_valid = false;
            for (_, &(a, b , c, d)) in rules {
                if in_range(field, a, b, c, d) {
                    is_valid = true;
                    break;
                }
            }
            if !is_valid {
                continue;
            }

            // Second pass
            for (name, &(a, b , c, d)) in rules {
                if !in_range(field, a, b, c, d) {
                    let x = possible_indexes.get_mut(name).unwrap();
                    x.remove(&field_index);
                }
            }
        }
    }
}

fn part_three(
    possible_indexes: &mut HashMap<String, HashSet<usize>>,
    my_ticket: &Vec<usize>,
    verbose: bool
) -> usize {
    if verbose {
        print_possible_indexes(&possible_indexes);
    }
    let mut all: HashMap<String, usize> = HashMap::new();

    loop {
        let (singleton_name, singleton_value) = find_singleton(&possible_indexes, verbose);
        if singleton_name == "" {
            break;
        }

        for (_, set) in &mut *possible_indexes {
            set.remove(&singleton_value);
        }
        &all.insert(singleton_name, singleton_value);
    }

    return calculate_answer(my_ticket, &all, verbose)
}

fn find_singleton(
    possible_indexes: &HashMap<String, HashSet<usize>>,
    _verbose: bool
) -> (String, usize) {
    for (name, vec) in possible_indexes {
        if vec.len() == 1 {
            let v: Vec<&usize> = vec.iter().collect::<Vec<&usize>>();
            return (name.to_string(), *v[0])
        }
    }
    return ("".to_string(), 0);
}

fn in_range(x: usize, a: usize, b: usize, c: usize, d: usize) -> bool {
    return (x >= a && x <= b) || (x >= c && x <= d);
}

fn parse_rules(lines: &Vec<&str>, rules: &mut HashMap<String, (usize, usize, usize, usize)>, verbose: bool) {
    let re = Regex::new(r"^(.*): (\d+)-(\d+) or (\d+)-(\d+)$").unwrap();
    for line in lines {
        let captures = re.captures(line).unwrap();

        let key = captures.get(1).map_or("", |m| m.as_str());
        let a = captures.get(2).map_or("", |m| m.as_str()).parse::<usize>().unwrap();
        let b = captures.get(3).map_or("", |m| m.as_str()).parse::<usize>().unwrap();
        let c = captures.get(4).map_or("", |m| m.as_str()).parse::<usize>().unwrap();
        let d = captures.get(5).map_or("", |m| m.as_str()).parse::<usize>().unwrap();

        rules.insert(key.to_string(), (a, b, c, d));
    }
}

fn parse_tickets(lines: &Vec<&str>, tickets: &mut Vec<Vec<usize>>, verbose: bool) {
    for line in lines {
        if line.len() <= 0 || line.contains(":") {
            continue;
        }

        let mut v: Vec<usize> = Vec::new();
        for i in line.split(",") {
            v.push(i.parse::<usize>().unwrap());
        }

        tickets.push(v);
    }
}

fn print_rules(rules: &HashMap<String, (usize, usize, usize, usize)>) {
    println!("- rules -------------------------");

    for (key, (a, b, c, d)) in rules {
        println!("{}: {}-{} {}-{}", key, a,b,c,d);
    }
    println!("---------------------------------");
}

fn print_tickets(tickets: &Vec<Vec<usize>>) {
    println!("- tickets -------------------------");

    for ticket in tickets {
        for i in ticket {
            print!("{}, ", i);
        }
        println!("");
    }
    println!("-----------------------------------");
}

fn print_possible_indexes(possible_indexes: &HashMap<String, HashSet<usize>>) {
    println!("- possible_indexes -------------------------");

    for (name, set) in possible_indexes {
        print!("{}:", name);
        let mut s: Vec<&usize> = set.iter().collect::<Vec<&usize>>();
        s.sort();
        for i in s {
            print!(" {}", i);
        }
        println!("");
    }
    println!("--------------------------------------------");
}

fn calculate_answer(
    ticket: &Vec<usize>,
    table: &HashMap<String, usize>,
    verbose: bool,
) -> usize {
    let mut product = 1;
    for (name, value) in table {
        if name.starts_with("departure") {
            product *= ticket[*value];
        }
    }
    return product;
}


fn get_intermediate(ticket: &Vec<usize>, possible_indexes: &HashMap<String, HashSet<usize>>) -> usize {
    let mut product = 1;
    for (name, indexes) in possible_indexes {
        if name.starts_with("departure") {
            let v: Vec<&usize> = indexes.iter().collect::<Vec<&usize>>();
            product *= ticket[*v[0]];
        }
    }
    return product;
}
