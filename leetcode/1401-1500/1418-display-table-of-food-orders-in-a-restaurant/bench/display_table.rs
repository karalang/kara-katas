use std::collections::{BTreeMap, BTreeSet};

fn display_table(orders: &[Vec<String>]) -> Vec<Vec<String>> {
    let mut tables: BTreeMap<i64, BTreeMap<String, i64>> = BTreeMap::new();
    let mut foods: BTreeSet<String> = BTreeSet::new();
    for order in orders.iter() {
        let table: i64 = order[1].parse().unwrap();
        foods.insert(order[2].clone());
        *tables.entry(table).or_insert_with(BTreeMap::new).entry(order[2].clone()).or_insert(0) += 1;
    }
    let mut header = vec!["Table".to_string()];
    header.extend(foods.iter().cloned());
    let mut out = vec![header];
    for (table, counts) in tables.iter() {
        let mut row = vec![format!("{}", table)];
        for food in foods.iter() {
            row.push(format!("{}", counts.get(food).copied().unwrap_or(0)));
        }
        out.push(row);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1418;
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let mut dishes: Vec<String> = Vec::new();
    for _ in 0..30 {
        let n = 1 + next_random(&mut seed) % 20;
        let mut s = String::new();
        for _ in 0..n {
            let r = next_random(&mut seed);
            if r % 6 == 0 {
                s.push(' ');
            } else {
                s.push(letters[(r / 6 % 52) as usize]);
            }
        }
        dishes.push(s);
    }
    let mut pool: Vec<Vec<String>> = Vec::new();
    for _ in 0..200000 {
        let r = next_random(&mut seed);
        let food = dishes[(next_random(&mut seed) % 30) as usize].clone();
        pool.push(vec![format!("guest{}", r % 100), format!("{}", 1 + r / 100 % 500), food]);
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        let start = (next_random(&mut seed) % 150001) as usize;
        let table = display_table(&pool[start..start + 50000]);
        for row in table.iter() {
            for cell in row.iter() {
                for b in cell.bytes() {
                    check = (check * 131 + b as i64) % 1000000007;
                }
                check = (check * 131 + 7) % 1000000007;
            }
        }
    }
    println!("100 windows of 5 * 10^4 orders: checksum {}", check);
}
