pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.lines();

    let binary_seats: Vec<String> = y.map(|p| convert_to_binary(p, verbose)).collect();
    let seats: Vec<u64> = binary_seats.iter().map(|p| convert_to_integer(p.to_string(), verbose)).collect();

    println!("{:?}", seats);

    return 0 as u64
}


fn convert_to_binary(val: &str, verbose: bool) -> String {
    return val.chars()
    .map(|x| match x {
        'B' => '1',
        'F' => '0',
        'L' => '0',
        'R' => '1',
        _ => x
    }).collect::<String>();
}

fn convert_to_integer(val: String, verbose: bool) -> u64 {
    return isize::from_str_radix(&val[..], 2).unwrap() as u64;
}
