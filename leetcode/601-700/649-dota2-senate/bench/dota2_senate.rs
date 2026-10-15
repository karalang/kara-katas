// LeetCode #649: Dota2 Senate -- Rust mirror of the Kāra bench.
//
// The ★ arm over the same senates and rounds: a `VecDeque` of each
// party's senators by when they vote, the front two meeting and the
// earlier going to the back `n` places later.

use std::collections::VecDeque;

fn predict_party_victory(senate: &str) -> String {
    let bytes = senate.as_bytes();
    let n = bytes.len() as i64;
    let mut radiant: VecDeque<i64> = VecDeque::new();
    let mut dire: VecDeque<i64> = VecDeque::new();
    for i in 0..n {
        if bytes[i as usize] == b'R' {
            radiant.push_back(i);
        } else {
            dire.push_back(i);
        }
    }
    while !radiant.is_empty() && !dire.is_empty() {
        let r = radiant.pop_front().unwrap();
        let d = dire.pop_front().unwrap();
        if r < d {
            radiant.push_back(r + n);
        } else {
            dire.push_back(d + n);
        }
    }
    if !radiant.is_empty() { "Radiant".to_string() } else { "Dire".to_string() }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let inputs = 20;
    let rounds = 500;
    let mut seed: i64 = 649;
    let mut senates: Vec<String> = Vec::new();
    for _ in 0..inputs {
        let radiant = 45 + next_random(&mut seed) % 11;
        let mut s = String::new();
        for _ in 0..100000 {
            s.push(if next_random(&mut seed) % 100 < radiant { 'R' } else { 'D' });
        }
        senates.push(s);
    }
    let mut wins = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let won = predict_party_victory(&senates[(r * 7) % inputs]) == "Radiant";
        if won {
            wins += 1;
        }
        checksum = (checksum * 2 + if won { 1 } else { 0 }) % 1000000007;
    }
    println!("{} senates, {} rounds: Radiant wins {}, checksum {}", inputs, rounds, wins, checksum);
}
