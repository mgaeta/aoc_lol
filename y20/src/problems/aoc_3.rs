use crate::utils::lists;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.lines();
    let ski_map: Vec<Vec<bool>> = y.into_iter().map(|x| line_to_bool_vec(x)).collect();


    let slopes = [
        (1 as u64, 1 as u64),
        (3 as u64, 1 as u64),
        (5 as u64, 1 as u64),
        (7 as u64, 1 as u64),
        (1 as u64, 2 as u64)
    ];
    let mut product = 1 as u64;
    for (dx, dy) in slopes.iter() {
        let trees = trace_slope(&ski_map[..], 0, 0, *dx, *dy, verbose);

        if verbose {
            lists::print_bool_list(&trees[..]);
        }

        product = product * lists::count_trues(trees) as u64;
    }

    return product;
}

pub fn trace_slope(ski_map: &[Vec<bool>], x0: u64, y0: u64, dx: u64, dy: u64, verbose: bool) -> Vec<bool> {
    let length = ski_map.len() as u64;
    let mut trees: Vec<bool> = Vec::new();
    for i in 0..length {
        if y0 + i * dy > length {
            continue;
        }
        let tree = get_value_at_coordinates(ski_map, x0 + i * dx, y0 + i * dy);
        if verbose {
            println!("({}, {}) {}", x0 + i * dx, y0 + i * dy, tree);
        }
        trees.push(tree);
    }

    return trees;
}


pub fn line_to_bool_vec(line: &str) -> Vec<bool> {
    return line.chars().map(|x| x == '#').collect();
}

fn get_value_at_coordinates(ski_map: &[Vec<bool>], x: u64, y: u64) -> bool {
    let row = ski_map.get(y as usize).unwrap();
    let width = row.len();
    let row_index = (x as usize) % (width);

    return *row.get(row_index).unwrap()
}
