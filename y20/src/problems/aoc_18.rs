pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let mut sum = 0;
    for i in y {
        if i.len() <= 0 {
            continue;
        }
        sum += evaluate(i, verbose);
    }
    return sum as u64;
}


fn evaluate(expression: &str, verbose: bool) -> usize {
    if !(expression.contains("(")) {
        return evaluate_advanced(expression, verbose);
    }

    let (first_open_paren, close_paren) = get_paren_indexes(expression, verbose);


    let left_side = &expression[0..first_open_paren];
    let middle = &expression[first_open_paren+1..close_paren];
    let right_side = &expression[(close_paren + 1)..expression.len()];

    if verbose {
        println!("l{}", left_side);
        println!("m{}", middle);
        println!("r{}", right_side);
    }

    let expression_simple = [
        left_side.to_string(),
        evaluate(middle, verbose).to_string(),
        right_side.to_string(),
    ].join("");
    return evaluate(&expression_simple[..], verbose);
}

fn get_paren_indexes(expression: &str, verbose: bool) -> (usize, usize) {
    let first_open_paren = expression.find("(").unwrap();
    let mut close_paren = expression.len();
    let mut count = 1;
    for i in first_open_paren+1..expression.len() {
        let ch =  expression.chars().nth(i).unwrap();
        let add  = match ch {
            '(' => 1,
            ')' => -1,
            _ => 0,
        };
        count += add;

        if count == 0 {
            close_paren = i;
            break;
        }
    }
    return (first_open_paren, close_paren);
}


fn evaluate_advanced(expression: &str, verbose: bool) -> usize {
    let mut product = 1;
    for i in expression.split("*") {
        product *= evaluate_simple(i, verbose);
    }
    return product;
}

fn evaluate_simple(expression: &str, verbose: bool) -> usize {
    let mut value = 0;
    let mut operator = "+";
    for i in expression.split(" ") {
        match i {
            "+" => {
                operator = "+"
            },
            "*" => {
                operator = "*"
            },
            " " => (),
            "" => (),
            a => {
                let v = i.parse::<usize>().unwrap();
                if operator == "+" {
                    value += v;
                } else {
                    value *= v;
                }
            }
        }
    }
    return value;
}
