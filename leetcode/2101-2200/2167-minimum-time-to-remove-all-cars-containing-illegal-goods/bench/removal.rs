// LeetCode #2167: Minimum Time to Remove All Cars Containing Illegal Goods
// -- the benchmark's Rust mirror of removal.kara.

fn minimum_time(s: &str) -> i64 {
    let n = s.len() as i64;
    let mut left = 0i64;
    let mut best = n;
    for (i, c) in s.chars().enumerate() {
        let i = i as i64;
        if c == '1' {
            left = (left + 2).min(i + 1);
        }
        best = best.min(left + n - 1 - i);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2167i64;
    let mut train = String::new();
    for _ in 0..400000 {
        train.push(if next_random(&mut seed) % 3 == 0 { '1' } else { '0' });
    }
    let mut check = 0i64;
    for _ in 0..100 {
        let start = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 200001) as usize;
        let t = minimum_time(&train[start..start + 200000]);
        check = (check * 31 + t) % 1000000007;
    }
    println!("100 solves: checksum {}", check);
}
