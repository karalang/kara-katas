// LeetCode #1561: Maximum Number of Coins You Can Get -- bench: the ★ arm
// (sorted, every other pile past the n smallest) over 20 lists of 99999
// piles of 1 to 10000 coins, built once, each asked 10 times.
// Rust mirror of coins.kara.

fn max_coins(piles: &[i64]) -> i64 {
    let mut sorted = piles.to_vec();
    sorted.sort();
    let n = sorted.len() / 3;
    sorted[n..].iter().step_by(2).sum()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1561;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut piles = Vec::new();
        for _ in 0..99999 {
            piles.push(next_random(&mut seed) % 10000 + 1);
        }
        lists.push(piles);
    }
    let mut check = 0;
    let mut total = 0;
    for _ in 0..10 {
        for piles in &lists {
            let coins = max_coins(piles);
            total += coins;
            check = mix(check, coins);
        }
    }
    println!("10 passes over 20 lists of 99999 piles: {} coins, checksum {}", total, check);
}
