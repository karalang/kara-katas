// LeetCode #1415 bench, Rust: the first letter from (k - 1) / 2^(n - 1),
// and each letter after it the lower or the higher of the two that differ
// from the one before, workload and checksum as get_happy_string.kara.

fn get_happy_string(n: i32, k: i32) -> String {
    let per_first: i32 = 1 << (n - 1);
    if k > 3 * per_first {
        return String::new();
    }
    let letters = ['a', 'b', 'c'];
    let mut rest = k - 1;
    let mut last = letters[(rest / per_first) as usize];
    rest %= per_first;
    let mut s = String::new();
    s.push(last);
    let mut bit = per_first / 2;
    while bit > 0 {
        let options: Vec<char> = letters.iter().filter(|&&c| c != last).cloned().collect();
        last = options[if rest >= bit { 1 } else { 0 }];
        if rest >= bit {
            rest -= bit;
        }
        s.push(last);
        bit /= 2;
    }
    s
}

fn main() {
    let mut seed: i64 = 1415;
    let mut check: i64 = 0;
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let n = 1 + seed / 65536 % 10;
        let k = 1 + seed / 1024 % 100;
        let s = get_happy_string(n as i32, k as i32);
        let mut sum: i64 = 0;
        for &b in s.as_bytes() {
            sum = sum * 3 + b as i64;
        }
        check = (check * 131 + sum + s.len() as i64) % 1000000007;
    }
    println!("10^6 cases: checksum {}", check);
}
