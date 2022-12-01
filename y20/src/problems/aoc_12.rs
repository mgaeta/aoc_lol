use regex::Regex;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut data: Vec<(char, usize)> = Vec::new();
    for i in y {
        if i.len() == 0 {
            continue;
        }
        parse_line(i, &mut data);
    }
    if verbose {
        print_data(&data);
    }

    let mut direction = 0; // east
    let mut absolute_x: i32 = 0;
    let mut absolute_y: i32 = 0;
    let mut x: i32 = 10;
    let mut y: i32 = 1;

    for (instruction, value) in data {
        if true {
            step(instruction, value, &mut absolute_x, &mut absolute_y,&mut x, &mut y, verbose);
            if verbose {
               print_state(instruction, value, &absolute_x, &absolute_y, &x, &y);
            }
        } else {
            step_absolute(instruction, value, &mut absolute_x, &mut absolute_y, &mut direction, verbose);
            if verbose {
               print_state_2(instruction, value, &absolute_x, &absolute_y, &direction)
            }
        }

    }
    return (absolute_x.abs() + absolute_y.abs())  as u64;
}

fn print_state(instruction: char, value: usize, absolute_x: & i32, absolute_y: &i32, x: & i32, y: &i32) {
    println!("{}{}: abs({},{}) way({},{})", instruction, value, absolute_x, absolute_y, x, y);
}

fn print_state_2(
    instruction: char,
    value: usize,
    x: & i32,
    y: &i32,
    direction : &usize
) {
    println!("{}{}: ({},{}) {}", instruction, value, x, y, direction);
}

fn step(
    instruction: char,
    value: usize,
    absolute_x: &mut i32,
    absolute_y: &mut i32,
    x: &mut i32,
    y: &mut i32,
    verbose: bool,
) {
    match instruction {
        'N' => {
            *y = *y + value as i32;
        },
        'S' => {
            *y = *y - value as i32;
        },
        'E' => {
            *x = *x + value as i32;
        },
        'W' => {
            *x = *x - value as i32;
        },
        'L' => {
            match value {
                270 => {
                    let temp = *x;
                    *x = *y;
                    *y = -temp;
                },
                180 => {
                    *x = -*x;
                    *y = -*y;
                },
                90 => {
                    let temp = *x;
                    *x = -*y;
                    *y = temp;
                },
                _ => panic!("bad direction")
            }
        },
        'R' => {
            match value {
                90 => {
                    let temp = *x;
                    *x = *y;
                    *y = -temp;
                },
                180 => {
                    *x = -*x;
                    *y = -*y;
                },
                270 => {
                    let temp = *x;
                    *x = -*y;
                    *y = temp;
                },
                _ => panic!("bad direction")
            };
        },
        'F' => {
            *absolute_x = *absolute_x + (*x * value as i32) ;
            *absolute_y = *absolute_y + (*y * value as i32) ;
        },
        _ => panic!("bad char")
    }
}

fn step_absolute(
    instruction: char,
    value: usize,
    x: &mut i32,
    y: &mut i32,
    direction: &mut usize,
    verbose: bool
) {
    match instruction {
        'N' => {
            *y = *y + value as i32;
        },
        'S' => {
            *y = *y - value as i32;
        },
        'E' => {
            *x = *x + value as i32;
        },
        'W' => {
            *x = *x - value as i32;
        },
        'L' => {
            *direction = (720 + *direction - value) % 360;
        },
        'R' => {
            *direction = (*direction + value) % 360;
        },
        'F' => {
            let new_instruction = match direction {
                0 => 'E',
                90 => 'S',
                180 => 'W',
                270 => 'N',
                _ => panic!("bad direction")
            };
            step_absolute(new_instruction, value, x,y,direction, verbose);
        },
        _ => panic!("bad char")
    }
}

fn parse_line(line: &str, data: &mut Vec<(char, usize)>) {
    let re = Regex::new(r"^([A-Za-z])(\d+)").unwrap();
    let captures = re.captures(line).unwrap();
    let instruction = captures.get(1).map_or("", |m| m.as_str()).chars().collect::<Vec<char>>()[0];
    let value = captures.get(2).map_or("", |m| m.as_str()).parse::<usize>().unwrap();
    data.push((instruction, value));
}

fn print_data(data: &Vec<(char, usize)>) {
    for (a, b) in data {
        println!("{}{}", *a, *b);
    }
}
