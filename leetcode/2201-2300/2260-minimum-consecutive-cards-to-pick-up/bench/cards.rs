// LeetCode #2260: Minimum Consecutive Cards to Pick Up -- Rust mirror of
// the ★ arm: a `HashMap` of where each value was last seen, every repeat
// a candidate run. Same workload and checksum as cards.kara.
use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_card_pickup(cards: &[i64]) -> i64 {
    let mut last: HashMap<i64, i64> = HashMap::new();
    let mut best = -1;
    for (i, &card) in cards.iter().enumerate() {
        let i = i as i64;
        if let Some(&j) = last.get(&card) {
            let run = i - j + 1;
            if best < 0 || run < best {
                best = run;
            }
        }
        last.insert(card, i);
    }
    best
}

fn main() {
    let mut seed = 2260;
    let mut check = 0;
    let tops = [1000000, 100000, 10000];
    for t in 0..300 {
        let mut cards = Vec::with_capacity(100000);
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            cards.push((hi * 32768 + next_random(&mut seed)) % tops[t % 3]);
        }
        check = (check * 31 + minimum_card_pickup(&cards) + 2) % 1000000007;
    }
    println!("300 hands of 10^5 cards: checksum {}", check);
}
