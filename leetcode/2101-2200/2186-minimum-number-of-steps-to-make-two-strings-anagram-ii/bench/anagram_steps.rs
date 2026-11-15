// LeetCode #2186: Minimum Number of Steps to Make Two Strings Anagram II
// -- the benchmark's Rust mirror of anagram_steps.kara, over slices of
// the row: one balance of 26 counts.

fn min_steps(s: &[u8], t: &[u8]) -> i64 {
    let mut balance = [0i64; 26];
    for &b in s {
        balance[(b - 97) as usize] += 1;
    }
    for &b in t {
        balance[(b - 97) as usize] -= 1;
    }
    let mut steps = 0;
    for d in balance.iter() {
        steps += d.abs();
    }
    steps
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2186;
    let mut row: Vec<u8> = Vec::with_capacity(1000000);
    for _ in 0..1000000 {
        row.push((97 + next_random(&mut seed) % 26) as u8);
    }
    let mut check: i64 = 0;
    for _ in 0..200 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let c = next_random(&mut seed);
        let d = next_random(&mut seed);
        let i = ((a * 32768 + b) % 800001) as usize;
        let j = ((c * 32768 + d) % 800001) as usize;
        let steps = min_steps(&row[i..i + 200000], &row[j..j + 200000]);
        check = (check * 31 + steps) % 1000000007;
    }
    println!("200 solves: checksum {}", check);
}
