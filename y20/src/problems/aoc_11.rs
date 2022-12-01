pub fn main(input_string: String, verbose: bool) -> u64 {
    let y = input_string.split("\n");

    let neighbor_threshold = 5;
    let sight_max = 100000;

    let mut copy_y: Vec<&str> = Vec::new();
    let mut game_board: Vec<char> = Vec::new();
    for i in y {
        if i.len() > 0 {
            parse_line(i, &mut game_board, verbose);
        }
        copy_y.push(i);
    }

    let column_count: usize = copy_y[0].len();
    let row_count: usize = copy_y.len() -1;
    if verbose {
        print_board(&game_board, column_count, row_count);
    }

    for i in 0..game_board.len() {
        let neighbors = count_neighbors(
            &game_board,
            i,
            column_count,
            row_count,
            sight_max,
            verbose
        );
    }

    loop {
        let mut next_board: Vec<char> = Vec::new();
        step(
            &game_board,
            &mut next_board,
            column_count,
            row_count,
            neighbor_threshold,
            sight_max,
            verbose
        );
        if verbose {
            print_board(&next_board, column_count, row_count);
            print_neighbors(&next_board, column_count, row_count, sight_max);
        }
        if !is_board_changed(&game_board, &next_board, verbose) {
            return count_board(&next_board, verbose) as u64;
        }
        game_board = next_board;
    }
}

fn get_index(
    row: usize,
    column: usize,
    column_count: usize,
    row_count: usize
) -> usize {
    return row * (column_count) + column;
}

fn step(
    before: &Vec<char>,
    after: &mut Vec<char>,
    column_count: usize,
    row_count: usize,
    neighbor_threshold: usize,
    sight_max: usize,
    verbose: bool
) {
    *after = Vec::new();
    for i in 0..before.len() {
        let neighbors = count_neighbors(
            &before,
            i,
            column_count,
            row_count,
            sight_max,
            verbose
        );
        after.push(match before[i] {
            '#' => if neighbors >= neighbor_threshold { 'L' } else { '#' },
            'L' => if neighbors == 0 { '#' } else { 'L' },
            '.' => '.',
            _ => 'X',
        });
    }
}

fn parse_line(line: &str, game_board: &mut Vec<char>, verbose: bool) -> () {
    if verbose {
        println!("{}", line);
    }
    for i in line.chars() {
        &game_board.push(i);
    }
}

fn get_neighbor_indexes_line_of_sight(
    game_board: &Vec<char>,
    candidates: &mut Vec<usize>,
    i: usize,
    column_count: usize,
    row_count: usize,
    sight_max: usize,
    verbose: bool
) -> () {
    let old_row = (i / column_count) as i32;
    let old_column = (i % column_count) as i32;

    for row in -1..2 {
        for column in -1..2 {
            // Don't add self
            if row == 0 && column == 0 {
                continue;
            }

            let mut new_row = old_row;
            let mut new_column = old_column;
            for _ in 0..sight_max {
                new_row = new_row + row;
                new_column = new_column + column;

                // println!("({} {})", new_row, new_column);

                if new_row < 0
                    || new_column < 0
                    || new_row >= row_count as i32
                    || new_column >= column_count as i32 {
                    break;
                }

                let i = get_index(
                    new_row as usize,
                    new_column as usize,
                    column_count,
                    row_count
                );
                if game_board[i] != '.' {
                    &candidates.push(i);
                    break;
                }
            }
        }
    }
}

fn count_neighbors(
    game_board: &Vec<char>,
    index: usize,
    column_count: usize,
    row_count: usize,
    sight_max: usize,
    verbose: bool
) -> usize {
    let mut candidates:Vec<usize> = Vec::new();
    get_neighbor_indexes_line_of_sight(
        &game_board,
        &mut candidates,
        index,
        column_count,
        row_count,
        sight_max,
        verbose
    );
    return candidates.into_iter().filter(|&x| game_board[x] == '#').count();
}

fn count_board(game_board: &Vec<char>, verbose: bool) -> usize {
    return game_board.into_iter().filter(|&x| *x == '#').count();
}

fn print_board(game_board: &Vec<char>, column_count: usize, row_count: usize) -> () {
    println!("Board: c{}xr{}", column_count, row_count);
    for row in 0..row_count {
        for column in 0..column_count{
            print!("{}", &game_board[get_index(row, column, column_count, row_count)]);
        }
        println!("");
    }
    println!("");
}

fn print_neighbors(
    game_board: &Vec<char>,
    column_count: usize,
    row_count: usize,
    sight_max: usize
) -> () {
    println!("Neighbors: {}x{}", column_count, row_count);
    for row in 0..column_count {
        for column in 0..row_count {
            print!("{}", count_neighbors(
            &game_board,
            get_index(row, column, column_count, row_count),
            column_count,
            row_count,
            sight_max,
            false
        ));
        }
        println!("");
    }
    println!("");
}


fn is_board_changed(before: &Vec<char>, after: &Vec<char>, verbose: bool) -> bool {
    return before.iter().collect::<String>() != after.iter().collect::<String>();
}
