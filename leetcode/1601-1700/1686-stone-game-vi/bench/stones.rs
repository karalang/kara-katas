// LeetCode #1686: Stone Game VI -- the bench's Rust mirror: the ★ arm on 50
// random games of 100000 stones, all drawn first, each answered 10 times.

fn stone_game(alice: &[i32], bob: &[i32]) -> i32 {
    let n = alice.len();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| -(alice[i] + bob[i]));
    let mut difference: i32 = 0;
    for (turn, &i) in order.iter().enumerate() {
        if turn % 2 == 0 {
            difference += alice[i];
        } else {
            difference -= bob[i];
        }
    }
    difference.signum()
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let size = 100000;
    let rounds = 10;
    let mut seed = 1686;
    let mut games: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..count {
        let mut alice = Vec::new();
        let mut bob = Vec::new();
        for _ in 0..size {
            alice.push((next_random(&mut seed) % 100 + 1) as i32);
            bob.push((next_random(&mut seed) % 100 + 1) as i32);
        }
        games.push((alice, bob));
    }
    let mut wins = [0i64; 3];
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (alice, bob) in games.iter() {
            let answer = stone_game(alice, bob);
            wins[(answer + 1) as usize] += 1;
            check = (check * 31 + answer as i64 + 2 + r) % 1000000007;
        }
    }
    println!("{count} games of {size} stones, {rounds} rounds: Alice {}, Bob {}, draws {}, checksum {check}", wins[2], wins[0], wins[1]);
}
