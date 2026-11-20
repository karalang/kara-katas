// LeetCode #1705: Maximum Number of Eaten Apples -- the bench's Rust
// mirror: the ★ arm on 50 random trees of 20000 days, all drawn first,
// each answered 10 times.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

// each day the rotten crops dropped and one apple eaten from the soonest to rot
fn eaten_apples(apples: &[i32], days: &[i32]) -> i32 {
    let n = apples.len() as i64;
    let mut queue: BinaryHeap<Reverse<(i64, i32)>> = BinaryHeap::new();
    let mut eaten = 0;
    let mut day: i64 = 0;
    while day < n || !queue.is_empty() {
        if day < n && apples[day as usize] > 0 {
            queue.push(Reverse((day + days[day as usize] as i64, apples[day as usize])));
        }
        while let Some(&Reverse((rot, _))) = queue.peek() {
            if rot > day {
                break;
            }
            queue.pop();
        }
        if let Some(Reverse((rot, left))) = queue.pop() {
            eaten += 1;
            if left > 1 {
                queue.push(Reverse((rot, left - 1)));
            }
        }
        day += 1;
    }
    eaten
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 10;
    let n = 20000;
    let mut seed = 1705;
    let mut trees: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..count {
        let mut apples: Vec<i32> = Vec::new();
        let mut days: Vec<i32> = Vec::new();
        for _ in 0..n {
            // one day in four grows nothing
            let grown = if next_random(&mut seed) % 4 == 0 { 0 } else { next_random(&mut seed) % 20000 + 1 };
            apples.push(grown as i32);
            days.push(if grown == 0 { 0 } else { (next_random(&mut seed) % 20000 + 1) as i32 });
        }
        trees.push((apples, days));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (apples, days) in trees.iter() {
            let answer = eaten_apples(apples, days) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} trees of {n} days, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
