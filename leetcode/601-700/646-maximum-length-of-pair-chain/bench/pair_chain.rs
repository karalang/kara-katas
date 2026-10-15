// LeetCode #646: Maximum Length of Pair Chain -- Rust mirror of the Kāra
// bench.
//
// The ★ arm's greedy over the same inputs and rounds: the pairs cloned
// and sorted by right end, then every pair kept that starts after the
// last one kept ended.

fn find_longest_chain(pairs: &Vec<Vec<i64>>) -> i64 {
    let mut order = pairs.clone();
    order.sort_by(|a, b| a[1].cmp(&b[1]));
    let mut count = 0;
    let mut end = 0;
    for p in &order {
        if count == 0 || p[0] > end {
            count += 1;
            end = p[1];
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let inputs = 20;
    let rounds = 200;
    let mut seed: i64 = 646;
    let mut all: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..inputs {
        let longest = 10 + next_random(&mut seed) % 991;
        let mut pairs = Vec::new();
        for _ in 0..10000 {
            let left = next_random(&mut seed) % 30000;
            let right = left + 1 + next_random(&mut seed) % longest;
            pairs.push(vec![left, right]);
        }
        all.push(pairs);
    }
    let mut sum: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let c = find_longest_chain(&all[(r * 7) % inputs]);
        sum += c;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    println!("{} inputs, {} rounds: total {}, checksum {}", inputs, rounds, sum, checksum);
}
