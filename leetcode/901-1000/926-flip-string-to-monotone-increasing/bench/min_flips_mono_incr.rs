// LeetCode #926: Flip String to Monotone Increasing -- bench: one pass.
// Mirrors min_flips_mono_incr.kara.

fn min_flips_mono_incr(s: &str) -> i64 {
    let mut flips: i64 = 0;
    let mut ones: i64 = 0;
    for c in s.bytes() {
        if c == b'1' {
            ones += 1;
        } else {
            flips = (flips + 1).min(ones);
        }
    }
    flips
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (20, 100, 100000);
    let mut seed = 926;
    // count strings of n characters, built once, leaning from 0 to 1
    let mut strings: Vec<String> = Vec::new();
    for i in 0..count {
        let lean = i as i64 % 101;
        let s: String = (0..n)
            .map(|_| {
                if next_random(&mut seed) % 100 < lean {
                    '1'
                } else {
                    '0'
                }
            })
            .collect();
        strings.push(s);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every string, starting from a different one
        for i in 0..count {
            let a = min_flips_mono_incr(&strings[(r + i) % count]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over {count} strings of {n}: answers summing to {total}, checksum {check}"
    );
}
