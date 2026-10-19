// LeetCode 789 — Escape The Ghosts: the bench, in Rust.
// Mirrors escape_ghosts.kara: every ghost's distance to the target
// against yours, stopping at the first that is no farther.

fn escape_ghosts(ghosts: &[[i64; 2]], target: [i64; 2]) -> bool {
    let mine = target[0].abs() + target[1].abs();
    for g in ghosts {
        if (g[0] - target[0]).abs() + (g[1] - target[1]).abs() <= mine {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 789;
    let mut boards: Vec<Vec<[i64; 2]>> = Vec::new();
    for _ in 0..64 {
        let mut ghosts: Vec<[i64; 2]> = Vec::new();
        for _ in 0..100 {
            let x = next_random(&mut seed) % 20001 - 10000;
            let y = next_random(&mut seed) % 20001 - 10000;
            ghosts.push([x, y]);
        }
        boards.push(ghosts);
    }
    let rounds = 10000000;
    let mut escapes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let x = next_random(&mut seed) % 2001 - 1000;
        let y = next_random(&mut seed) % 2001 - 1000;
        if escape_ghosts(&boards[r % 64], [x, y]) {
            escapes += 1;
            check = (check * 31 + (r % 1000) as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds of 100-ghost boards: {escapes} escapes, checksum {check}");
}
