use std::collections::HashSet;
use std::collections::HashMap;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n\n").collect();

    let mut deck_0: Vec<usize> = Vec::new();
    let mut deck_1: Vec<usize> = Vec::new();

    parse_deck(y[0], &mut deck_0, verbose);
    parse_deck(y[1], &mut deck_1, verbose);


    let mut global_game_memo: HashMap<(String, String), bool> = HashMap::new();

    let play_0_won = if true {
        part_two(
            &mut deck_0,
            &mut deck_1,
            &mut global_game_memo,
            verbose
        )
    } else {
        part_one(&mut deck_0, &mut deck_1, verbose)
    };

    if play_0_won {
        return calculate_score(&deck_0, verbose) as u64;
    } else {
        return calculate_score(&deck_1, verbose) as u64;
    }
}

fn part_one(
    deck_0: &mut Vec<usize>,
    deck_1: &mut Vec<usize>,
    verbose: bool
) -> bool {
    while !(&deck_0).is_empty() && !(&deck_1).is_empty() {
        if verbose {
            println!("---------------------");
            print_deck(&deck_0);
            print_deck(&deck_1);
        }
        play_highest_card(deck_0, deck_1, verbose);
    }
    if verbose {
        print_deck(&deck_0);
        print_deck(&deck_1);
    }

    return deck_0.len() > 0;
}

fn part_two(
    deck_0: &mut Vec<usize>,
    deck_1: &mut Vec<usize>,
    global_game_memo: &mut HashMap<(String, String), bool>,
    verbose: bool
) -> bool {
    let mut decks_memo: HashSet<(String, String)> = HashSet::new();

    while !(&deck_0).is_empty() && !(&deck_1).is_empty() {
        let key = get_key(&deck_0, &deck_1);

        if decks_memo.contains(&key) {
            return true;
        } else {
            decks_memo.insert(key);
        }

        deck_0.reverse();
        deck_1.reverse();

        let player_0 = deck_0.pop().unwrap();
        let player_1 = deck_1.pop().unwrap();

        deck_0.reverse();
        deck_1.reverse();

        let should_play_recursive = player_0 <= deck_0.len() && player_1 <= deck_1.len();

        let mut player_0_won_round = true;
        if should_play_recursive {
            let game_key = get_key(&deck_0, &deck_1);
            match global_game_memo.get(&game_key) {
                Some(t) => {
                    player_0_won_round = t.clone();
                },
                None => {
                    let mut deck_0_copy: Vec<usize> = Vec::new();
                    let mut deck_1_copy: Vec<usize> = Vec::new();

                    for i in 0..player_0 {
                        deck_0_copy.push(deck_0[i].clone());
                    }
                    for i in 0..player_1 {
                        deck_1_copy.push(deck_1[i].clone());
                    }

                    player_0_won_round = part_two(
                        &mut deck_0_copy,
                        &mut deck_1_copy,
                        global_game_memo,
                        verbose
                    );
                    global_game_memo.insert(game_key, player_0_won_round);
                }
            }
        } else {
            player_0_won_round = player_0 > player_1;
        }

        if player_0_won_round {
            (deck_0).push(player_0);
            (deck_0).push(player_1);
        } else {
            (deck_1).push(player_1);
            (deck_1).push(player_0)
        }
    }
    if verbose {
        print_deck(&deck_0);
        print_deck(&deck_1);
    }
    return deck_0.len() > 0;
}

fn get_key(deck_0: &Vec<usize>, deck_1: &Vec<usize>) -> (String, String) {
    let x0: Vec<String> = deck_0.iter().map(|x| x.to_string()).collect();
    let x1: Vec<String> = deck_1.iter().map(|x| x.to_string()).collect();
    return (x0.join(","), x1.join(","));
}

fn play_highest_card(
    deck_0: &mut Vec<usize>,
    deck_1: &mut Vec<usize>,
    verbose: bool
) {
    deck_0.reverse();
    deck_1.reverse();

    let player_0 = deck_0.pop().unwrap();
    let player_1 = deck_1.pop().unwrap();

    deck_0.reverse();
    deck_1.reverse();

    if player_0 > player_1 {
        deck_0.push(player_0);
        deck_0.push(player_1);
    } else {
        deck_1.push(player_1);
        deck_1.push(player_0)
    }
}

fn parse_deck(
    lines: &str,
    deck: &mut Vec<usize>,
    verbose: bool
) {
    let line_vec: Vec<&str> = lines.split("\n").collect();
    // discard the first line
    for i in 1..line_vec.len() {
        let x = line_vec[i];
        if x.len() <= 0 {
            continue;
        }
        deck.push(x.parse::<usize>().unwrap());
    }
}


fn calculate_score(deck: &Vec<usize>, _verbose: bool) -> usize {
    let mut score = 0;
    for i in 0..deck.len() {
        score += (deck.len()- i) * deck[i];
    }
    return score;
}

fn print_deck(deck: &Vec<usize>) {
    print!("DECK");
    for i in deck {
        print!(" {}", i);
    }
    println!("");
}
