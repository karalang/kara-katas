// LeetCode #886 bench: Rust mirror of possible_bipartition.kara (the ★
// arm, two colours by breadth-first search) on the same 4000 groups.

use std::collections::VecDeque;

fn possible_bipartition(n: i64, dislikes: &[Vec<i64>]) -> bool {
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n + 1];
    for d in dislikes {
        adj[d[0] as usize].push(d[1] as usize);
        adj[d[1] as usize].push(d[0] as usize);
    }
    let mut colour: Vec<i64> = vec![-1; n + 1];
    let mut queue: VecDeque<usize> = VecDeque::new();
    for start in 1..=n {
        if colour[start] >= 0 {
            continue;
        }
        colour[start] = 0;
        queue.push_back(start);
        while let Some(u) = queue.pop_front() {
            for &v in &adj[u] {
                if colour[v] < 0 {
                    colour[v] = 1 - colour[u];
                    queue.push_back(v);
                } else if colour[v] == colour[u] {
                    return false;
                }
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 886;
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..4000 {
        // n people, each disliking the people five distinct offsets on,
        // every offset below n / 2 so that no pair repeats: 5n pairs, up
        // to 10^4; the offsets odd, but one of them even half the time
        let n = 1000 + next_random(&mut seed) % 1001;
        let spoil = next_random(&mut seed) % 2 == 0;
        let mut offsets: Vec<i64> = Vec::new();
        while offsets.len() < 5 {
            let mut d = 1 + next_random(&mut seed) % (n / 2 - 1);
            if d % 2 == 0 && !(spoil && offsets.is_empty()) {
                d -= 1;
            }
            if !offsets.contains(&d) {
                offsets.push(d);
            }
        }
        let mut dislikes: Vec<Vec<i64>> = Vec::new();
        for a in 0..n {
            for k in 0..5 {
                dislikes.push(vec![a + 1, (a + offsets[k]) % n + 1]);
            }
        }
        let bit = if possible_bipartition(n, &dislikes) { 1 } else { 0 };
        yes += bit;
        check = (check * 3 + bit + 1) % 1000000007;
    }
    println!("4000 groups of up to 2000 people: {} can be split, checksum {}", yes, check);
}
