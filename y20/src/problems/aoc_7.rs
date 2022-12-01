use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut rules: HashMap<String, HashMap<String, usize>> = HashMap::new();
    let mut reverse_rules: HashMap<String, HashSet<String>> = HashMap::new();
    for i in y {
        parse_line(&mut rules, &mut reverse_rules, i, verbose);
    }

    if verbose {
        println!("Rules:");
        print_rules(&rules);
        println!("Reverse Rules:");
        print_reverse_rules(&reverse_rules);
    }

    if true {
        return (traverse_rules(&rules, "shiny gold", verbose) - 1) as u64;
    } else {
        return traverse_reverse_rules(&reverse_rules, "shiny gold", verbose) as u64;
    }
}

fn traverse_rules(rules: &HashMap<String, HashMap<String, usize>>, root: &str, verbose: bool) -> usize {
    let mut count = 1;

    for (inner_bag, inner_count) in rules.get(root).unwrap() {
        count = count + inner_count * traverse_rules(rules, inner_bag, verbose);
    }

    return count;
}

fn traverse_reverse_rules(reverse_rules: &HashMap<String, HashSet<String>>, root: &str, verbose: bool) -> usize {
    let mut visited: HashSet<String> = HashSet::new();
    let mut to_visit: Vec<String> = Vec::new();

    to_visit.push(root.to_string());
    while to_visit.len() > 0 {
        let curr = to_visit.pop().unwrap();
        if reverse_rules.contains_key(&curr) {
            let parents = reverse_rules.get(&curr).unwrap();
            for p in parents {
                if verbose {
                    println!("p {:?}", p);
                }
                to_visit.push(p.to_string());
                visited.insert(p.to_string());
            }
        }
    }

    return visited.len()
}

fn parse_line(
    rules: &mut HashMap<String, HashMap<String, usize>>,
    reverse_rules: &mut HashMap<String, HashSet<String>>,
    line: &str,
    verbose: bool
) {
    let re = Regex::new(r"^(.*) bags contain (.*)\.$").unwrap();

    let captures = re.captures(line).unwrap();
    let outer_bag = captures.get(1).map_or("", |m| m.as_str());
    let contained_bags = captures.get(2).map_or("", |m| m.as_str());

    let mut new_rule: HashMap<String, usize> = HashMap::new();
    if contained_bags != "no other bags" {
        let split = contained_bags.split(", ");
        for c in split {
            let split_rule: Vec<&str> = c.split(" ").collect();
            let count = split_rule[0].parse::<usize>().unwrap();
            let inner_bag = split_rule[1..split_rule.len()-1].join(" ");
            new_rule.insert(inner_bag.to_string(), count);

            if !reverse_rules.contains_key(&inner_bag.to_string()) {
                reverse_rules.insert(inner_bag.to_string(), HashSet::new());
            }

            let rr = reverse_rules.get_mut(&inner_bag.to_string()).unwrap();
            rr.insert(outer_bag.to_string());
        }
    }

    rules.insert(outer_bag.to_string(), new_rule);
}

// TODO make this print out something nicer.
fn print_reverse_rules(rules: &HashMap<String, HashSet<String>>) {
    for (rule_name, rules_set) in rules.iter() {
        println!("{} {:?}", rule_name, rules_set);
    }
}

fn print_rules(rules: &HashMap<String, HashMap<String, usize>>) {
    for (rule_name, rules_map) in rules.iter() {
        for (inner_rule, count) in rules_map.iter() {
            println!("{} {:?}: {:?}", rule_name, inner_rule, count);
        }
    }
}
