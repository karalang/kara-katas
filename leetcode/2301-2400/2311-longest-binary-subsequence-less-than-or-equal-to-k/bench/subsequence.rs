// LeetCode #2311: Longest Binary Subsequence Less Than or Equal to K --
// the bench, the ★ arm in Rust. Greedy from the right: every `0` taken,
// and a `1` taken when its place still leaves the value at most `k`.

fn longest_subsequence(s: &str, k: i64) -> i64 {
    let bytes = s.as_bytes();
    let mut value = 0i64;
    let mut taken = 0i64;
    for i in (0..bytes.len()).rev() {
        if bytes[i] == b'0' {
            taken += 1;
        } else if taken < 31 && value + (1 << taken) <= k {
            value += 1 << taken;
            taken += 1;
        }
    }
    taken
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2311;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let odds = next_random(&mut seed) % 8 + 1;
        let mut s = String::new();
        for _ in 0..1000 {
            s.push(if next_random(&mut seed) % odds == 0 { '1' } else { '0' });
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for p in 0..100i64 {
        for a in 0..1000usize {
            check = (check * 31 + longest_subsequence(&strings[a], 10000000 * (p + 1) + a as i64)) % 1000000007;
        }
    }
    println!("100 passes over 1000 strings of 1000 bits: checksum {}", check);
}
