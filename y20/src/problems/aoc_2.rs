use crate::utils::lists;
use regex::Regex;


pub fn main(input_string: String, _verbose: bool) -> u64 {
    let y = input_string.lines();
    let v: Vec<bool> = y.into_iter().map(|x| is_line_valid(x)).rev().collect();

    return lists::count_trues(v);
}

fn is_line_valid(line: &str) -> bool {
    let re = Regex::new(r"^(\d+)-(\d+) ([A-Za-z]): ([A-Za-z]+)$").unwrap();

    let captures = re.captures(line).unwrap();

    let password = captures.get(4).map_or("", |m| m.as_str());
    let rule = captures.get(3).map_or("", |m| m.as_str());
    let min = captures.get(1).map_or("", |m| m.as_str()).parse::<u64>().unwrap();
    let max = captures.get(2).map_or("", |m| m.as_str()).parse::<u64>().unwrap();

    if true {
        return is_password_valid(password, rule, min, max);
    } else {
        return is_password_valid_2(password, rule, min, max);
    }
}

fn is_password_valid(password: &str, rule: &str, i0: u64, i1: u64) -> bool {
    let mut vec = Vec::new();
    vec.push(password.chars().nth((i0-1) as usize).unwrap().to_string() == rule);
    vec.push(password.chars().nth((i1-1) as usize).unwrap().to_string() == rule);

    return lists::count_trues(vec) == 1;
}

fn is_password_valid_2(password: &str, rule: &str, min: u64, max: u64) -> bool {
    let count = password.matches(rule).count() as u64;
    return count <= max && count >= min;
}
