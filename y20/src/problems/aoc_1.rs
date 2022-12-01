use std::collections::HashSet;


pub fn main(input_string: String, _verbose: bool) -> u64 {
    let y = input_string.lines();
    let (a, b, c) = get_matching_numbers_from_list(2020, y);
    return a * b * c;
}

pub fn get_matching_numbers_from_list(target: u64, inputs: std::str::Lines) -> (u64, u64, u64) {
    let mut x = HashSet::new();
    for number in inputs  {
        let my_int = number.parse::<u64>().unwrap();
        x.insert(my_int);
    }

    for i in &x  {
        for j in &x  {
            if (i + j) > target {
                continue
            }
            let candidate = target - i - j;
            if x.contains(&candidate) {
                return (candidate, *i, *j);
            }
        }
    }

    panic!("bad input");
}
