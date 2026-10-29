// LeetCode #1016: Binary String With Substrings Representing 1 To N --
// bench
// Mirrors query.kara; see ../README.md § Benchmarks.

fn query_string(s: &str, n: i64) -> bool {
    if n - n / 2 > 2 * s.len() as i64 {
        return false;
    }
    let mut x = n;
    while x > n / 2 {
        if !s.contains(&format!("{:b}", x)) {
            return false;
        }
        x -= 1;
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let strings = 200;
    let len = 1000;
    let most: i64 = 400;
    let mut seed = 1016;
    let mut holds = 0;
    let mut check: i64 = 0;
    for _ in 0..strings {
        let mut s = String::new();
        for _ in 0..len {
            s.push(if next_random(&mut seed) % 2 == 1 { '1' } else { '0' });
        }
        for n in 1..most + 1 {
            let answer = query_string(&s, n);
            if answer {
                holds += 1;
            }
            check = (check * 2 + if answer { 1 } else { 0 }) % 1000000007;
        }
    }
    println!("{} strings of {} bits, n = 1..{}: {} hold, checksum {}", strings, len, most, holds, check);
}
