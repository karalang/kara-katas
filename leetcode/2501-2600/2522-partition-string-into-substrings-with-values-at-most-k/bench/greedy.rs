// LeetCode #2522: Partition String Into Substrings With Values at Most K --
// Rust mirror of the benchmark (greedy.kara): the same strings, passes,
// order and checksum.

fn minimum_partition(s: &str, k: i64) -> i64 {
    let mut parts = 1;
    let mut value = 0;
    for b in s.bytes() {
        let d = (b - b'0') as i64;
        if d > k {
            return -1;
        }
        value = value * 10 + d;
        if value > k {
            parts += 1;
            value = d;
        }
    }
    parts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2522;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..20 {
        let mut s = String::new();
        for _ in 0..100000 {
            s.push(((next_random(&mut seed) % 9 + 1) as u8 + b'0') as char);
        }
        strings.push(s);
    }
    let passes = 50;
    let mut check: i64 = 0;
    for p in 0..passes {
        for s in &strings {
            check = (check * 31 + minimum_partition(s, check % 999999992 + 9) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 20 strings of 10^5 digits: checksum {check}");
}
