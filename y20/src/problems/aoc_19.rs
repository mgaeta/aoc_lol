use regex::Regex;
use std::collections::HashMap;

pub fn main(input_string: String, verbose: bool) -> u64 {
    let y: Vec<&str> = input_string.split("\n\n").collect();

    let mut rules: HashMap<usize, String> = HashMap::new();
    let mut messages: Vec<String> = Vec::new();

    parse_rules(y[0], &mut rules, verbose);
    parse_messages(y[1], &mut messages, verbose);

    if verbose {
        print_rules(&rules);
    }

    let rule_0 = rules.get(&0).unwrap();
    let regex_string = format!("^{}$", construct_regex(
        rule_0.to_string(),
        &rules,
        verbose
    ));
    let re = Regex::new(&regex_string[..]).unwrap();
    if verbose {
        println!("REGEX: {}", regex_string);
    }
    let mut count = 0;
    for i in messages {
        if re.is_match(&i[..]) {
            count += 1;
        }
    }
    return count as u64;
}

fn parse_messages(
    lines: &str,
    messages: &mut Vec<String>,
    verbose: bool
) {
    for i in lines.split("\n") {
        if i.len() <= 0 {
            continue;
        }
        messages.push(i.to_string());
    }
}

fn construct_regex(
    rule: String,
    rules: &HashMap<usize, String>,
    verbose: bool
) -> String {
    // TODO memoize


    if rule == "42" {
        return format!(
            "({})+",
            construct_regex(
            rules
                    .get(&42)
                    .unwrap()
                    .to_string(),
                &rules,
            verbose
            )
        );
    }

    if rule == "42 31" {
        let rule_42 = construct_regex(
        rules
                .get(&42)
                .unwrap()
                .to_string(),
            &rules,
        verbose
        );

        let rule_31 = construct_regex(
        rules
                .get(&31)
                .unwrap()
                .to_string(),
            &rules,
        verbose
        );
        return format!(
            "(({})|({})|({})|({})|({}))",
            vec![rule_42.to_string(), rule_31.to_string()].join(""),
            vec![rule_42.to_string(), rule_42.to_string(), rule_31.to_string(), rule_31.to_string()].join(""),
            vec![rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string()].join(""),
            vec![rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string()].join(""),
            vec![rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string()].join(""),
            // vec![rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_42.to_string(), rule_31.to_string(),rule_31.to_string(),rule_31.to_string(), rule_31.to_string(), rule_31.to_string(), rule_31.to_string()].join(""),
        );
    }

    if verbose {
        println!("construct_regex {}", rule);
    }

    if rule.contains("\"") {
        return rule[1..2].to_string();
    }

    if rule.contains("|") {
        return format!(
            "({})",
            rule
                .split(" | ")
                .map(|part|
                    construct_regex(
                        part.to_string(),
                        &rules,
                        verbose
                    )
                )
                .collect::<Vec<String>>()
                .join("|")
        );
    }

    return rule
        .split(" ")
        .map(|part| construct_regex(
            rules
                    .get(&part.parse::<usize>().unwrap())
                    .unwrap()
                    .to_string(),
                &rules,
            verbose
        ))
        .collect::<Vec<String>>()
        .join("");
}

fn parse_rules(
    lines: &str,
    rules: &mut HashMap<usize, String>,
    verbose: bool
) {
    for i in lines.split("\n") {
        if i.len() <= 0 {
            continue;
        }
        let parts: Vec<&str> = i.split(": ").collect();
        let key = parts[0].parse::<usize>().unwrap();
        let rule = parts[1].to_string();
        rules.insert(key, rule);
    }
}

fn print_rules(rules: &HashMap<usize, String>) {
    for (key, value) in rules {
        println!("{}: {}", key, construct_regex(value.to_string(), &rules, false));
    }
}
