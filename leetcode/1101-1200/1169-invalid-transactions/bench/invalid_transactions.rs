// LeetCode #1169: Invalid Transactions -- the ★ arm's bench in Rust: each
// transaction split into its fields, the places of each name's
// transactions gathered in a `HashMap`, and every transaction compared with
// the others of its name.

use std::collections::HashMap;

struct Txn {
    name: String,
    time: i64,
    amount: i64,
    city: String,
}

fn parse(t: &str) -> Txn {
    let f: Vec<&str> = t.split(',').collect();
    Txn {
        name: f[0].to_string(),
        time: f[1].parse().unwrap(),
        amount: f[2].parse().unwrap(),
        city: f[3].to_string(),
    }
}

fn invalid_transactions(transactions: &[String]) -> Vec<String> {
    let txns: Vec<Txn> = transactions.iter().map(|t| parse(t)).collect();
    let mut by_name: HashMap<String, Vec<usize>> = HashMap::new();
    for (i, t) in txns.iter().enumerate() {
        by_name.entry(t.name.clone()).or_default().push(i);
    }
    let mut out = Vec::new();
    for (i, t) in txns.iter().enumerate() {
        let bad = t.amount > 1000
            || by_name[&t.name].iter().any(|&j| {
                let o = &txns[j];
                (o.time - t.time).abs() <= 60 && o.city != t.city
            });
        if bad {
            out.push(transactions[i].clone());
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn line(seed: &mut i64) -> String {
    let name = next_random(seed) % 200;
    let time = next_random(seed) % 1001;
    let amount = next_random(seed) % 1101;
    let city = next_random(seed) % 2;
    format!("n{},{},{},c{}", name, time, amount, city)
}

fn main() {
    let mut seed = 1169;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..16 {
        lists.push((0..1000).map(|_| line(&mut seed)).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..300 {
        for k in 0..16 {
            let at = (next_random(&mut seed) % 1000) as usize;
            lists[k][at] = line(&mut seed);
            let bad = invalid_transactions(&lists[k]);
            total += bad.len() as i64;
            for b in &bad {
                check = (check * 31 + b.len() as i64) % 1000000007;
            }
        }
    }
    println!("300 rounds over 16 lists of 1000 transactions: {} invalid, checksum {}", total, check);
}
