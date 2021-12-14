use crate::utils::lists;
use std::collections::HashMap;
use std::collections::HashSet;
use regex::Regex;


pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n\n");

    let mut passports: Vec<HashMap<String, String>> = Vec::new();
    for i in y {
        parse_passport_line(&mut passports, i, verbose);
    }

    let valid_passports = passports.iter().map(|p| is_valid_passport(p, verbose)).collect();

    return lists::count_trues(valid_passports);
}

fn is_valid_passport(passport: &HashMap<String, String>, verbose: bool) -> bool {
    let required_attributes = vec![
        "byr", //(Birth Year)
        "iyr", //(Issue Year)
        "eyr", //(Expiration Year)
        "hgt", //(Height)
        "hcl", //(Hair Color)
        "ecl", //(Eye Color)
        "pid" //(Passport ID)
    ];

    for required_attribute in required_attributes {
        let f = match required_attribute {
            "byr" => is_valid_byr,
            "iyr" => is_valid_iyr,
            "eyr" => is_valid_eyr,
            "hgt" => is_valid_hgt,
            "hcl" => is_valid_hcl,
            "ecl" => is_valid_ecl,
            "pid" => is_valid_pid,
            _ => panic!("unknown attribute {:?}", required_attribute)
        };



        let val = match passport.get(required_attribute) {
            Some(expr) => expr,
            None => "[missing]",
        };


        let is_valid = match passport.get(required_attribute) {
            Some(expr) => f(expr),
            None => false,
        };

        if verbose {
            println!("attr: {}, val: {} is_valid: {}", required_attribute, val, is_valid);
        }

        if !is_valid {
            return false;
        }

    }

    return true;
}


fn is_valid_year(val: &str, min: u64, max: u64) -> bool {
    let my_int = val.parse::<u64>().unwrap();
    return my_int <= max && my_int >= min;
}

fn is_valid_byr(val: &str) -> bool {
    return is_valid_year(val, 1920, 2002);
}
fn is_valid_iyr(val: &str) -> bool {
    return is_valid_year(val, 2010, 2020);
}
fn is_valid_eyr(val: &str) -> bool {
    return is_valid_year(val, 2020, 2030);
}
fn is_valid_hgt(val: &str) -> bool {
    let re = Regex::new(r"^(\d+)(cm|in)$").unwrap();
    if !re.is_match(val) {
        return false;
    }

    let captures = re.captures(val).unwrap();
    let unit = captures.get(2).map_or("", |m| m.as_str());
    let my_int = (captures.get(1).map_or("", |m| m.as_str())).parse::<u64>().unwrap();

    if unit == "in" {
        return (my_int >= 59 as u64) && (my_int <= 76 as u64);
    } else {
        return (my_int >= 150 as u64) && (my_int <= 193 as u64);
    }
}
fn is_valid_hcl(val: &str) -> bool {
    let re = Regex::new(r"^#[0-9a-f]{6}$").unwrap();
    return re.is_match(val);
}
fn is_valid_ecl(val: &str) -> bool {
    let mut eye_colors = HashSet::new();
    eye_colors.insert("amb");
    eye_colors.insert("blu");
    eye_colors.insert("brn");
    eye_colors.insert("gry");
    eye_colors.insert("grn");
    eye_colors.insert("hzl");
    eye_colors.insert("oth");

    return eye_colors.contains(val);
}
fn is_valid_pid(val: &str) -> bool {
    let re = Regex::new(r"^[0-9]{9}$").unwrap();
    return re.is_match(val);
}

fn parse_passport_line(passports: &mut Vec<HashMap<String, String>>, line: &str, verbose: bool) {
    let mut passport: HashMap<String, String> = HashMap::new();
    let parts = line.split_whitespace();
    for p in parts {
        let split = p.split(":");
        let vec = split.collect::<Vec<&str>>();
        passport.insert(vec[0].to_string(), vec[1].to_string());
    }

    if verbose {
        println!("{:?}", passport);
    }

    passports.push(passport);
}
