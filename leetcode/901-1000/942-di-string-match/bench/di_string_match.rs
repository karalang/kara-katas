// Benchmark: LeetCode #942 DI String Match -- the ★ arm, the smallest
// and largest left, on 20 strings of 100000 letters, LeetCode's longest,
// in 50 rounds. Mirrors di_string_match.kara, .c, .py and go-seq/.

fn di_string_match(s: &str) -> Vec<i64> {
    let b = s.as_bytes();
    let n = b.len() as i64;
    let mut lo = 0;
    let mut hi = n;
    let mut perm: Vec<i64> = Vec::new();
    for &c in b {
        if c == b'I' {
            perm.push(lo);
            lo += 1;
        } else {
            perm.push(hi);
            hi -= 1;
        }
    }
    perm.push(lo);
    perm
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 50;
    let count = 20;
    let n = 100000;
    let mut seed = 942;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let odds = 1 + next_random(&mut seed) % 15;
        let mut s = String::new();
        for _ in 0..n {
            s.push(if next_random(&mut seed) % 16 < odds {
                'I'
            } else {
                'D'
            });
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let perm = di_string_match(&strings[(r + i) % count]);
            check = (check * 1000003 + perm[0] * 3 + perm[n / 2] * 5 + perm[n] * 7) % 1000000007;
        }
    }
    println!(
        "{} rounds over {} strings of {} letters: checksum {}",
        rounds, count, n, check
    );
}
