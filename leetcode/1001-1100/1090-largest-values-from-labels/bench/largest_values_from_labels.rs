// Benchmark: LeetCode #1090 Largest Values From Labels -- Rust mirror of the
// ★ arm: (value, label) pairs sorted by value from the largest (`sort_by`,
// stable, as Kāra's), taken while their label has uses left (a `HashMap` of
// uses per label, SipHash as Kāra's `Map`). Same workload and sink as
// largest_values_from_labels.kara.

use std::collections::HashMap;

fn largest_vals_from_labels(values: &[i64], labels: &[i64], num_wanted: i64, use_limit: i64) -> i64 {
    let mut items: Vec<(i64, i64)> = Vec::new();
    for i in 0..values.len() {
        items.push((values[i], labels[i]));
    }
    items.sort_by(|a, b| b.0.cmp(&a.0));
    let mut used: HashMap<i64, i64> = HashMap::new();
    let mut taken = 0;
    let mut sum = 0;
    for &(value, label) in items.iter() {
        if taken == num_wanted {
            break;
        }
        let uses = used.get(&label).copied().unwrap_or(0);
        if uses < use_limit {
            used.insert(label, uses + 1);
            sum += value;
            taken += 1;
        }
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1090;
    let mut problems: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..100 {
        let mut values = Vec::new();
        let mut labels = Vec::new();
        for _ in 0..20000 {
            values.push(next_random(&mut seed) % 20001);
            labels.push(next_random(&mut seed) % 1000);
        }
        problems.push((values, labels));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..20i64 {
        for (k, p) in problems.iter().enumerate() {
            let k = k as i64;
            let num_wanted = (round * 7919 + k * 31) % 20000 + 1;
            let use_limit = (round * 13 + k) % 20 + 1;
            let answer = largest_vals_from_labels(&p.0, &p.1, num_wanted, use_limit);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("20 rounds over 100 problems of 2 * 10^4 items: answers sum to {}, checksum {}", total, check);
}
