// Benchmark twin for LeetCode #294 — same algorithm as flipgame2.kara.
//
// PARITY NOTE. Memoized backtracking with a fresh map per board, the map keyed
// by the board string and holding an owned copy of it. Successors are built one
// character at a time rather than by slicing, because Kāra's String is
// append-only and that is its natural form; see #293's bench header for what
// happened the last time the mirrors drifted into different algorithms.

use std::collections::HashMap;

const LEN: usize = 22;
const BOARDS: usize = 300;

fn next_rand(s: i64) -> i64 { (s.wrapping_mul(1103515245).wrapping_add(12345)) & 2147483647 }

fn next_states(s: &str) -> Vec<String> {
    let cs: Vec<char> = s.chars().collect();
    let n = cs.len();
    let mut out = Vec::new();
    for i in 0..n.saturating_sub(1) {
        if cs[i] == '+' && cs[i + 1] == '+' {
            let mut t = String::new();
            for j in 0..n {
                t.push(if j == i || j == i + 1 { '-' } else { cs[j] });
            }
            out.push(t);
        }
    }
    out
}

fn can_win(s: &str, memo: &mut HashMap<String, bool>) -> bool {
    if let Some(&v) = memo.get(s) {
        return v;
    }
    for t in next_states(s) {
        if !can_win(&t, memo) {
            memo.insert(s.to_string(), true);
            return true;
        }
    }
    memo.insert(s.to_string(), false);
    false
}

fn main() {
    let mut seed: i64 = 20260821;
    let densities = [15i64, 50, 85];
    let mut wins: i64 = 0;
    let mut checksum: i64 = 0;

    for &d in densities.iter() {
        for _ in 0..BOARDS {
            let mut s = String::new();
            for _ in 0..LEN {
                seed = next_rand(seed);
                s.push(if ((seed / 65536) % 100) < d { '+' } else { '-' });
            }
            let mut memo: HashMap<String, bool> = HashMap::new();
            if can_win(&s, &mut memo) {
                wins += 1;
            }
            checksum = (checksum * 31 + memo.len() as i64) % 1_000_000_007;
        }
    }
    println!("wins {} checksum {}", wins, checksum);
}
