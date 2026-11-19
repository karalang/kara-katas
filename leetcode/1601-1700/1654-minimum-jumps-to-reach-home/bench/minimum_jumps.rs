// LeetCode #1654: Minimum Jumps to Reach Home -- the bench's Rust mirror:
// the ★ arm on 5000 random problems with a, b and x up to 2000 and up to
// 1000 forbidden positions, all drawn first.

use std::collections::VecDeque;

fn minimum_jumps(forbidden: &[i32], a: i32, b: i32, x: i32) -> i32 {
    let a = a as i64;
    let b = b as i64;
    let x = x as i64;
    let furthest = forbidden.iter().copied().max().unwrap_or(0) as i64;
    let limit = x.max(furthest) + a + b;
    let mut blocked = vec![false; (limit + 1) as usize];
    for &f in forbidden {
        blocked[f as usize] = true;
    }
    let mut seen = vec![[false, false]; (limit + 1) as usize];
    let mut queue: VecDeque<(i64, bool, i32)> = VecDeque::new();
    queue.push_back((0, false, 0));
    seen[0][0] = true;
    while let Some((p, back, jumps)) = queue.pop_front() {
        if p == x {
            return jumps;
        }
        let forward = p + a;
        if forward <= limit && !blocked[forward as usize] && !seen[forward as usize][0] {
            seen[forward as usize][0] = true;
            queue.push_back((forward, false, jumps + 1));
        }
        let backward = p - b;
        if !back && backward >= 0 && !blocked[backward as usize] && !seen[backward as usize][1] {
            seen[backward as usize][1] = true;
            queue.push_back((backward, true, jumps + 1));
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1654;
    let mut problems: Vec<(Vec<i32>, i32, i32, i32)> = Vec::new();
    for _ in 0..5000 {
        let a = (next_random(&mut seed) % 2000 + 1) as i32;
        let b = (next_random(&mut seed) % 2000 + 1) as i32;
        let x = (next_random(&mut seed) % 2001) as i32;
        let m = next_random(&mut seed) % 1001;
        let mut taken = vec![false; 2001];
        let mut forbidden: Vec<i32> = Vec::new();
        for _ in 0..m {
            let f = (next_random(&mut seed) % 2000 + 1) as i32;
            if f != x && !taken[f as usize] {
                taken[f as usize] = true;
                forbidden.push(f);
            }
        }
        problems.push((forbidden, a, b, x));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    let mut unreachable = 0;
    for (forbidden, a, b, x) in &problems {
        let answer = minimum_jumps(forbidden, *a, *b, *x) as i64;
        if answer < 0 {
            unreachable += 1;
        }
        total += answer;
        check = (check * 31 + answer + 2) % 1000000007;
    }
    println!("5000 problems up to 2000: jumps sum to {}, {} unreachable, checksum {}", total, unreachable, check);
}
