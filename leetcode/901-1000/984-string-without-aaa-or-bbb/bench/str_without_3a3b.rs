// Benchmark: LeetCode #984 String Without AAA or BBB -- the ★ arm, greedy,
// reading the tail, on every pair of counts up to LeetCode's 100.
// Mirrors str_without_3a3b.kara, .c, .py and go-seq/.

fn str_without_3a3b(a: i64, b: i64) -> String {
    let mut s = String::new();
    let mut left_a = a;
    let mut left_b = b;
    while left_a > 0 || left_b > 0 {
        let write_a = if s.ends_with("aa") {
            false
        } else if s.ends_with("bb") {
            true
        } else {
            left_a >= left_b
        };
        if write_a {
            s.push('a');
            left_a -= 1;
        } else {
            s.push('b');
            left_b -= 1;
        }
    }
    s
}

fn main() {
    let rounds: i64 = 100;
    let mut pairs: Vec<(i64, i64)> = Vec::new();
    for a in 0..101i64 {
        for b in 0..101i64 {
            if a + b > 0 && a <= 2 * b + 2 && b <= 2 * a + 2 {
                pairs.push((a, b));
            }
        }
    }
    let n = pairs.len() as i64;
    let mut letters: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..n {
            let (a, b) = pairs[((r + i) % n) as usize];
            let s = str_without_3a3b(a, b);
            let len = s.len() as i64;
            let middle = if s.as_bytes()[(len / 2) as usize] == b'a' { 1 } else { 2 };
            letters += len;
            check = (check * 31 + len * 3 + middle) % 1000000007;
        }
    }
    println!("{} rounds over {} pairs up to 100: {} letters, checksum {}", rounds, n, letters, check);
}
