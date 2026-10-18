// LeetCode #736: Parse Lisp Expression -- tokens, recursion and a stack
// of scopes.
// Benchmark mirror of the Kara star arm: split the text into tokens,
// then evaluate by recursion, keeping the assignments of each open let
// in a scope of its own and looking a name up from the innermost.
use std::collections::HashMap;

fn tokenize(expression: &str) -> Vec<String> {
    let mut tokens: Vec<String> = Vec::new();
    let mut word = String::new();
    for c in expression.chars() {
        if c == '(' || c == ')' || c == ' ' {
            if !word.is_empty() {
                tokens.push(word);
                word = String::new();
            }
            if c != ' ' {
                tokens.push(c.to_string());
            }
        } else {
            word.push(c);
        }
    }
    if !word.is_empty() {
        tokens.push(word);
    }
    tokens
}

fn lookup(scopes: &[HashMap<String, i64>], name: &str) -> i64 {
    for scope in scopes.iter().rev() {
        if let Some(v) = scope.get(name) {
            return *v;
        }
    }
    0
}

fn eval(tokens: &[String], pos: &mut usize, scopes: &mut Vec<HashMap<String, i64>>) -> i64 {
    let t = tokens[*pos].clone();
    *pos += 1;
    if t != "(" {
        let first = t.as_bytes()[0];
        if first == b'-' || first.is_ascii_digit() {
            return t.parse().unwrap();
        }
        return lookup(scopes, &t);
    }
    let op = tokens[*pos].clone();
    *pos += 1;
    let value;
    if op == "add" {
        let a = eval(tokens, pos, scopes);
        let b = eval(tokens, pos, scopes);
        value = a + b;
    } else if op == "mult" {
        let a = eval(tokens, pos, scopes);
        let b = eval(tokens, pos, scopes);
        value = a * b;
    } else {
        scopes.push(HashMap::new());
        loop {
            let name = tokens[*pos].clone();
            if name != "(" && tokens[*pos + 1] != ")" {
                *pos += 1;
                let v = eval(tokens, pos, scopes);
                scopes.last_mut().unwrap().insert(name, v);
            } else {
                value = eval(tokens, pos, scopes);
                break;
            }
        }
        scopes.pop();
    }
    *pos += 1;
    value
}

fn evaluate(expression: &str) -> i64 {
    let tokens = tokenize(expression);
    let mut pos = 0;
    let mut scopes: Vec<HashMap<String, i64>> = Vec::new();
    eval(&tokens, &mut pos, &mut scopes)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_expr(seed: &mut i64, depth: i64, names: &Vec<String>) -> String {
    let kinds = if depth == 0 { 2 } else { 5 };
    let kind = next_random(seed) % kinds;
    if kind == 0 || (kind == 1 && names.is_empty()) {
        return format!("{}", next_random(seed) % 21 - 10);
    }
    if kind == 1 {
        return names[(next_random(seed) % names.len() as i64) as usize].clone();
    }
    if kind == 2 {
        let a = random_expr(seed, depth - 1, names);
        let b = random_expr(seed, depth - 1, names);
        return format!("(add {} {})", a, b);
    }
    if kind == 3 {
        let a = random_expr(seed, depth - 1, names);
        return format!("(mult {} {})", a, next_random(seed) % 5 - 2);
    }
    let pool = ["x", "y", "z", "a1", "b2"];
    let mut inner = names.clone();
    let mut text = "(let".to_string();
    let count = 1 + next_random(seed) % 3;
    for _ in 0..count {
        let name = pool[(next_random(seed) % 5) as usize].to_string();
        let v = random_expr(seed, depth - 1, &inner);
        text = format!("{} {} {}", text, name, v);
        if !inner.contains(&name) {
            inner.push(name);
        }
    }
    let body = random_expr(seed, depth - 1, &inner);
    format!("{} {})", text, body)
}

fn main() {
    let mut seed: i64 = 736;
    let mut exprs: Vec<String> = Vec::new();
    let mut chars = 0;
    while exprs.len() < 1000 {
        let e = random_expr(&mut seed, 8, &Vec::new());
        if e.len() >= 500 && e.len() <= 2000 {
            chars += e.len();
            exprs.push(e);
        }
    }
    let mut sum: i64 = 0;
    for _ in 0..40 {
        for e in exprs.iter() {
            let v = evaluate(e);
            sum = (sum * 31 + (v % 1000000007 + 1000000007) % 1000000007) % 1000000007;
        }
    }
    println!("40 rounds of 1000 expressions of {} characters in all: checksum {}", chars, sum);
}
