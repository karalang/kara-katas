// LeetCode #629: K Inverse Pairs Array -- Rust mirror of the Kāra bench.
//
// The ★ arm's rolling DP with a window sum over the same inputs.

fn k_inverse_pairs(n: i64, k: i64) -> i64 {
    let modulus = 1000000007;
    let k = k as usize;
    let mut row = vec![0i64; k + 1];
    row[0] = 1;
    for i in 2..n as usize + 1 {
        let mut next = vec![0i64; k + 1];
        let mut window = 0;
        for j in 0..k + 1 {
            window = (window + row[j]) % modulus;
            if j >= i {
                window = (window - row[j - i] + modulus) % modulus;
            }
            next[j] = window;
        }
        row = next;
    }
    row[k]
}

fn main() {
    let rounds = 100;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let n = 500 + (r * 37) % 501;
        let k = 500 + (r * 91) % 501;
        let c = k_inverse_pairs(n, k);
        checksum = (checksum * 31 + c) % 1000000007;
    }
    println!("{} rounds: checksum {}", rounds, checksum);
}
