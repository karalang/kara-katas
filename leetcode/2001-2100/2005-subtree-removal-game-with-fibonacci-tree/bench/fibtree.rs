// LeetCode #2005: Subtree Removal Game with Fibonacci Tree -- the benchmark's
// Rust twin, the same algorithm as fibtree.kara here.

fn find_game_winner(n: i64) -> bool {
    // value[k] is order(k)'s value; value[0] is unused
    let mut value = vec![0i64; (n + 1) as usize];
    for k in 2..=n as usize {
        let left = if k >= 3 { value[k - 2] + 1 } else { 0 };
        value[k] = left ^ (value[k - 1] + 1);
    }
    value[n as usize] != 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 500000 values of n from 1 to 100 drawn once, then the ★ arm on each, 10 rounds
    let mut seed = 2005i64;
    let queries: Vec<i64> = (0..500000).map(|_| next_random(&mut seed) % 100 + 1).collect();
    let (mut calls, mut alice, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..10 {
        for &n in queries.iter() {
            let wins = find_game_winner(n);
            calls += 1;
            if wins {
                alice += 1;
            }
            check = (check * 31 + if wins { n } else { 0 }) % 1000000007;
        }
    }
    println!("{} calls: Alice wins {}, checksum {}", calls, alice, check);
}
