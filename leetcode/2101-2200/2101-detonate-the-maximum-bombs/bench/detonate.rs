// LeetCode #2101: Detonate the Maximum Bombs -- Rust mirror of the ★ arm's
// benchmark (detonate.kara): the same 2000 fields of 100 bombs, adjacency
// lists and a breadth-first search from each bomb.
use std::collections::VecDeque;

fn maximum_detonation(bombs: &[[i64; 3]]) -> i64 {
    let n = bombs.len();
    let mut reach: Vec<Vec<usize>> = vec![Vec::new(); n];
    for i in 0..n {
        for j in 0..n {
            let dx = bombs[i][0] - bombs[j][0];
            let dy = bombs[i][1] - bombs[j][1];
            if i != j && dx * dx + dy * dy <= bombs[i][2] * bombs[i][2] {
                reach[i].push(j);
            }
        }
    }
    let mut best = 0;
    for start in 0..n {
        let mut seen = vec![false; n];
        seen[start] = true;
        let mut queue = VecDeque::new();
        queue.push_back(start);
        let mut count = 0;
        while let Some(i) = queue.pop_front() {
            count += 1;
            for &j in &reach[i] {
                if !seen[j] {
                    seen[j] = true;
                    queue.push_back(j);
                }
            }
        }
        best = best.max(count);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2101;
    let mut total = 0;
    let mut check: i64 = 0;
    for _ in 0..2000 {
        let mut bombs: Vec<[i64; 3]> = Vec::new();
        for _ in 0..100 {
            let x = next_random(&mut seed) % 1000 + 1;
            let y = next_random(&mut seed) % 1000 + 1;
            let r = next_random(&mut seed) % 150 + 1;
            bombs.push([x, y, r]);
        }
        let got = maximum_detonation(&bombs);
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    println!("2000 fields: {total} bombs in all, checksum {check}");
}
