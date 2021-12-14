use regex::Regex;
use std::collections::{HashMap, HashSet};


pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut input: Vec<(HashSet<String>, HashSet<String>)> = Vec::new();
    let mut every_allergy: HashMap<String, usize> = HashMap::new();
    let mut every_food: HashMap<String, usize> = HashMap::new();

    for i in y {
        if i.len() > 1 {
            parse_line(
                i,
                &mut input,
                &mut every_allergy,
                &mut every_food,
                verbose
            );
        }
    }

    // this might be more useful as counts.
    let mut allergy_index: HashMap<String, HashSet<String>> = HashMap::new();
    let mut food_index: HashMap<String, HashSet<String>> = HashMap::new();

    for (allergies, foods) in input {
        part_1(
            &allergies,
            &foods,
            &every_allergy,
            &every_food,
            &mut allergy_index,
            &mut food_index,
            verbose
        );
    }

    if verbose {
        print_every_allergy(&every_allergy);
        print_every_food(&every_food);
        print_allergy_index(&allergy_index);
        print_food_index(&food_index);
    }

    return 0 as u64;
}


fn parse_line(
    line: &str,
    input: &mut Vec<(HashSet<String>, HashSet<String>)>,
    every_allergy: &mut HashMap<String, usize>,
    every_food: &mut HashMap<String, usize>,
    verbose: bool,
) {
    let re = Regex::new(r"^(.+) \(contains (.+)\)$").unwrap();
    let captures = re.captures(line).unwrap();
    let foods_string = captures.get(1).map_or("", |m| m.as_str());
    let allergies_string = captures.get(2).map_or("", |m| m.as_str());

    let foods: Vec<&str> = foods_string.split(" ").collect::<Vec<&str>>();
    let allergies: Vec<&str> = allergies_string.split(", ").collect::<Vec<&str>>();


    let mut allergy_set: HashSet<String> = HashSet::new();
    let mut food_set: HashSet<String> = HashSet::new();

    for f in foods {
        food_set.insert(f.to_string());
        let count = every_food.get(&f.to_string()).unwrap_or(&0);
        every_food.insert(f.to_string(), count + 1);
    }
    for a in allergies {
        allergy_set.insert(a.to_string());
        let count = every_allergy.get(&a.to_string()).unwrap_or(&0);
        every_allergy.insert(a.to_string(), count + 1);
    }

    input.push((allergy_set, food_set));
}

fn part_1(
    allergies: &HashSet<String>,
    foods: &HashSet<String>,
    every_allergy: &HashMap<String, usize>,
    every_food: &HashMap<String, usize>,
    allergy_index: &mut HashMap<String, HashSet<String>>,
    food_index: &mut HashMap<String, HashSet<String>>,
    verbose: bool,
) {
    for food in foods {
        let found = food_index.entry(food.to_string()).or_insert(every_allergy.keys().cloned().collect());
        for (allergy, _) in every_allergy {
            if !allergies.contains(&allergy.to_string()) {
                found.remove(&allergy.to_string());
            }
        }
    }

    for allergy in allergies {
        let found = allergy_index.entry(allergy.to_string()).or_insert(every_food.keys().cloned().collect());
        for (food, _) in every_food {
            if !foods.contains(&food.to_string()) {
                found.remove(&food.to_string());
            }
        }
    }
}

fn print_allergy_index(allergy_index: &HashMap<String, HashSet<String>>) {
    println!("- allergy_index ------------------------------");
    for (key, value) in allergy_index {
        print!("{}:", key);
        for i in value.iter() {
            print!(" {}", i);
        }
        println!("");
    }
    println!("----------------------------------------------");
}

fn print_food_index(food_index: &HashMap<String, HashSet<String>>) {
    println!("- food_index ------------------------------");
    for (key, value) in food_index {
        print!("{}:", key);
        for i in value.iter() {
            print!(" {}", i);
        }
        println!("");
    }
    println!("----------------------------------------------");
}

fn print_every_allergy(every_allergy: &HashMap<String, usize>) {
    println!("- every_allergy ({}) ------------------------------", every_allergy.len());
    for (a, count) in every_allergy {
        println!("{} {}", a, count);
    }
    println!("----------------------------------------------");
}

fn print_every_food(every_food: &HashMap<String, usize>) {
    println!("- every_food ({}) ------------------------------", every_food.len());
    for (a, count) in every_food {
        println!("{} {}", a, count);
    }
    println!("----------------------------------------------");
}
