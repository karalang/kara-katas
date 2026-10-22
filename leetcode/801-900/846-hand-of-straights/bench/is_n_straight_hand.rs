// Benchmark for #846: Hand of Straights -- Rust twin of the Kāra open-groups
// arm (sorted runs and a queue of open groups).
use std::collections::VecDeque;

fn is_n_straight_hand(hand: &[i64], group_size: i64) -> bool {
    if hand.len() as i64 % group_size != 0 {
        return false;
    }
    let mut cards = hand.to_vec();
    cards.sort();
    let mut started: VecDeque<i64> = VecDeque::new();
    let mut open = 0;
    let mut last = 0;
    let mut i = 0;
    while i < cards.len() {
        let value = cards[i];
        let mut count = 0;
        while i < cards.len() && cards[i] == value {
            count += 1;
            i += 1;
        }
        if open > 0 && (value != last + 1 || count < open) {
            return false;
        }
        started.push_back(count - open);
        last = value;
        open = count;
        if started.len() as i64 == group_size {
            open -= started.pop_front().unwrap();
        }
    }
    open == 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 3000;
    let n = 10000;
    let sizes = [1, 2, 4, 5, 10, 16, 100, 1000];
    let mut seed: i64 = 846;
    let mut hands: Vec<Vec<i64>> = Vec::new();
    let mut group_sizes: Vec<i64> = Vec::new();
    for g in 0..count {
        let group_size = sizes[g % 8];
        let window = 1 + next_random(&mut seed) % 20000;
        let mut hand: Vec<i64> = Vec::new();
        while hand.len() < n {
            let start = 999000000 + next_random(&mut seed) % window;
            for j in 0..group_size {
                hand.push(start + j);
            }
        }
        for i in 0..n {
            let j = i + (next_random(&mut seed) % (n - i) as i64) as usize;
            hand.swap(i, j);
        }
        if g % 4 == 3 {
            let at = (next_random(&mut seed) % n as i64) as usize;
            hand[at] += 1;
        }
        hands.push(hand);
        group_sizes.push(group_size);
    }
    let mut splits = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let ok = is_n_straight_hand(&hands[round % count], group_sizes[round % count]);
        if ok {
            splits += 1;
        }
        checksum = (checksum * 31 + (round % count) as i64 + if ok { 1 } else { 0 }) % 1000000007;
    }
    println!("{} rounds of {} hands: {} split, checksum {}", rounds, count, splits, checksum);
}
