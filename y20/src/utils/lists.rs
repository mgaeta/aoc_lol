pub fn count_trues(bool_list: Vec<bool>) -> u64 {
    return bool_list.into_iter().filter(|&n| n).count() as u64
}

pub fn print_bool_list(bool_list: &[bool]) {
    for i in bool_list {
        println!("{:?}", i);
    }
}
