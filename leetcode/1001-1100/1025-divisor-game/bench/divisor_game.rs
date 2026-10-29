// LeetCode #1025: Divisor Game -- bench
// Mirrors ./divisor_game.kara; see ../README.md § Benchmarks.

fn divisor_game(n: i64) -> bool {
    let n = n as usize;
    let mut divisors: Vec<Vec<i64>> = vec![Vec::new(); n + 1];
    for x in 1..n / 2 + 1 {
        let mut m = 2 * x;
        while m <= n {
            divisors[m].push(x as i64);
            m += x;
        }
    }
    let mut wins: Vec<bool> = vec![false; n + 1];
    for m in 2..n + 1 {
        wins[m] = divisors[m].iter().any(|&x| !wins[m - x as usize]);
    }
    wins[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 100;
    let mut seed = 1025;
    let mut games: Vec<i64> = Vec::new();
    for _ in 0..count {
        games.push(500 + next_random(&mut seed) % 501);
    }
    let mut wins = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for &n in games.iter() {
            let alice = divisor_game(n);
            if alice {
                wins += 1;
            }
            check = (check * 131 + n * 2 + if alice { 1 } else { 0 }) % 1000000007;
        }
    }
    println!(
        "{count} games of n from 500 to 1000, {rounds} rounds: Alice wins {wins}, checksum {check}"
    );
}
