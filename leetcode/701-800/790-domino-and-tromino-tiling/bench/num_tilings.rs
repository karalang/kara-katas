// LeetCode 790 — Domino and Tromino Tiling: the bench, in Rust.
// Mirrors num_tilings.kara: two growing tables of counts, full and
// ragged ends, for 300,000 random n.

fn num_tilings(n: usize) -> i64 {
    let modulus = 1000000007;
    let mut full: Vec<i64> = vec![1, 1];
    let mut ragged: Vec<i64> = vec![0, 1];
    for i in 2..n + 1 {
        full.push((full[i - 1] + full[i - 2] + 2 * ragged[i - 2]) % modulus);
        ragged.push((ragged[i - 1] + full[i - 1]) % modulus);
    }
    full[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 790;
    let rounds = 300000;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let n = 1 + next_random(&mut seed) % 1000;
        let ways = num_tilings(n as usize);
        sum = (sum + ways) % 1000000007;
        check = (check * 31 + ways) % 1000000007;
    }
    println!("{rounds} rounds of n up to 1000: answers sum to {sum}, checksum {check}");
}
