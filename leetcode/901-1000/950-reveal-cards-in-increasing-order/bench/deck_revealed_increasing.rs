// Benchmark: LeetCode #950 Reveal Cards In Increasing Order -- the ★ arm,
// the reveals played on the places, on decks of 1000 cards, LeetCode's
// largest. Mirrors deck_revealed_increasing.kara, .c, .py and go-seq/.
use std::collections::{HashSet, VecDeque};

fn deck_revealed_increasing(deck: &[i64]) -> Vec<i64> {
    let mut sorted = deck.to_vec();
    sorted.sort();
    let n = deck.len();
    let mut places: VecDeque<usize> = (0..n).collect();
    let mut out = vec![0i64; n];
    for &card in &sorted {
        let place = places.pop_front().unwrap();
        out[place] = card;
        if let Some(next) = places.pop_front() {
            places.push_back(next);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n): (usize, usize, usize) = (1000, 20, 1000);
    let mut seed = 950;
    let mut decks: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut taken: HashSet<i64> = HashSet::new();
        let mut deck: Vec<i64> = Vec::new();
        while deck.len() < n {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            let v = 1 + (a * 32768 + b) % 1000000;
            if taken.insert(v) {
                deck.push(v);
            }
        }
        decks.push(deck);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let out = deck_revealed_increasing(&decks[(r + i) % count]);
            total += out[n - 1];
            check = (check * 1000003 + out[(r * 7 + i) % n]) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} decks of {n} cards: last cards adding to {total}, checksum {check}");
}
