// Benchmark for #822: Card Flipping Game -- the ★ arm (a set of the doubles).
//
// Mirrors flipgame.kara: the numbers on both sides of one card go in a
// set, and the answer is the smallest number on any card that is not in
// it, or 0.

use std::collections::HashSet;

fn flipgame(fronts: &[i64], backs: &[i64]) -> i64 {
    let mut doubles: HashSet<i64> = HashSet::new();
    for i in 0..fronts.len() {
        if fronts[i] == backs[i] {
            doubles.insert(fronts[i]);
        }
    }
    let mut best = 0;
    for i in 0..fronts.len() {
        for x in [fronts[i], backs[i]] {
            if !doubles.contains(&x) && (best == 0 || x < best) {
                best = x;
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64usize;
    let rounds = 50000usize;
    let mut seed: i64 = 822;
    let mut all_fronts: Vec<Vec<i64>> = Vec::new();
    let mut all_backs: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut fronts = Vec::new();
        let mut backs = Vec::new();
        for _ in 0..1000 {
            let f = 1 + next_random(&mut seed) % 2000;
            fronts.push(f);
            if next_random(&mut seed) % 2 == 0 {
                backs.push(f);
            } else {
                backs.push(1 + next_random(&mut seed) % 2000);
            }
        }
        all_fronts.push(fronts);
        all_backs.push(backs);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = round % count;
        let answer = flipgame(&all_fronts[g], &all_backs[g]);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    println!("{rounds} rounds of {count} hands: total {total}, checksum {checksum}");
}
