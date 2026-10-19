// LeetCode 770 — Basic Calculator IV: benchmark, the ★ arm in Rust.
// Sixty-four random expressions of 40 leaves, built once; 20,000 rounds
// each simplify the next of them.
use std::collections::HashMap;

type Poly = HashMap<String, i64>;

fn tokenize(expression: &str) -> Vec<String> {
    let mut tokens = Vec::new();
    let mut word = String::new();
    for c in expression.chars() {
        if c.is_ascii_alphanumeric() {
            word.push(c);
        } else {
            if !word.is_empty() {
                tokens.push(word.clone());
                word = String::new();
            }
            if c != ' ' {
                tokens.push(c.to_string());
            }
        }
    }
    if !word.is_empty() {
        tokens.push(word);
    }
    tokens
}

fn names_of(key: &str) -> Vec<String> {
    if key.is_empty() {
        Vec::new()
    } else {
        key.split('*').map(|s| s.to_string()).collect()
    }
}

fn add_into(total: &mut Poly, p: Poly, sign: i64) {
    for (key, coef) in p {
        *total.entry(key).or_insert(0) += sign * coef;
    }
}

fn multiply(a: &Poly, b: &Poly) -> Poly {
    let mut product = Poly::new();
    for (ka, ca) in a {
        for (kb, cb) in b {
            let mut names = names_of(ka);
            names.extend(names_of(kb));
            names.sort();
            *product.entry(names.join("*")).or_insert(0) += ca * cb;
        }
    }
    product
}

struct Reader<'a> {
    tokens: Vec<String>,
    at: usize,
    known: &'a HashMap<String, i64>,
}

impl<'a> Reader<'a> {
    fn peek(&self) -> &str {
        if self.at < self.tokens.len() { &self.tokens[self.at] } else { "" }
    }

    fn expression(&mut self) -> Poly {
        let mut total = self.term();
        while self.peek() == "+" || self.peek() == "-" {
            let sign = if self.peek() == "+" { 1 } else { -1 };
            self.at += 1;
            let next = self.term();
            add_into(&mut total, next, sign);
        }
        total
    }

    fn term(&mut self) -> Poly {
        let mut product = self.factor();
        while self.peek() == "*" {
            self.at += 1;
            let next = self.factor();
            product = multiply(&product, &next);
        }
        product
    }

    fn factor(&mut self) -> Poly {
        let token = self.peek().to_string();
        self.at += 1;
        let mut p = Poly::new();
        if token == "(" {
            p = self.expression();
            self.at += 1;
        } else if token.as_bytes()[0].is_ascii_digit() {
            p.insert(String::new(), token.parse().unwrap());
        } else {
            match self.known.get(&token) {
                Some(&value) => {
                    p.insert(String::new(), value);
                }
                None => {
                    p.insert(token, 1);
                }
            }
        }
        p
    }
}

fn basic_calculator_iv(expression: &str, evalvars: &[&str], evalints: &[i64]) -> Vec<String> {
    let known: HashMap<String, i64> =
        evalvars.iter().zip(evalints).map(|(v, &i)| (v.to_string(), i)).collect();
    let mut reader = Reader { tokens: tokenize(expression), at: 0, known: &known };
    let poly = reader.expression();
    let mut terms: Vec<(i64, String, i64)> = poly
        .into_iter()
        .filter(|&(_, c)| c != 0)
        .map(|(k, c)| (-(names_of(&k).len() as i64), k, c))
        .collect();
    terms.sort();
    terms
        .into_iter()
        .map(|(_, k, c)| if k.is_empty() { format!("{}", c) } else { format!("{}*{}", c, k) })
        .collect()
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn random_expression(rng: &mut Rng, size: i64) -> String {
    if size <= 1 {
        let pick = rng.next() % 9;
        if pick < 3 {
            return format!("{}", rng.next() % 10);
        }
        return ["a", "b", "c", "d", "x", "y"][(pick - 3) as usize].to_string();
    }
    let left = 1 + rng.next() % (size - 1);
    let a = random_expression(rng, left);
    let b = random_expression(rng, size - left);
    let op = [" + ", " - ", " * "][(rng.next() % 3) as usize];
    if rng.next() % 3 == 0 {
        format!("({}{}{})", a, op, b)
    } else {
        format!("{}{}{}", a, op, b)
    }
}

fn main() {
    let rounds: i64 = 20000;
    let mut rng = Rng(770);
    let pool: Vec<String> = (0..64).map(|_| random_expression(&mut rng, 40)).collect();
    let longest = pool.iter().map(|e| e.len()).max().unwrap();
    let mut terms = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let answer = basic_calculator_iv(&pool[(round % 64) as usize], &["x"], &[round % 7 - 3]);
        terms += answer.len();
        for t in &answer {
            for b in t.bytes() {
                check = (check * 31 + b as i64) % 1000000007;
            }
        }
    }
    println!(
        "{} expressions of up to {} characters: {} terms in all, checksum {}",
        rounds, longest, terms, check
    );
}
