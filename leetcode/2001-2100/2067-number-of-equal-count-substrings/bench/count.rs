// LeetCode #2067: Number of Equal Count Substrings -- Rust mirror of the
// ★ arm's benchmark (count.kara): 60 texts of 30000 letters from 1 to 26
// kinds, half in runs of `count`, count 1 to 7.

fn equal_count_substrings(s: &[u8], count: i64) -> i64 {
    let n = s.len() as i64;
    let mut total = 0;
    for k in 1..=26 {
        let len = k * count;
        if len > n {
            break;
        }
        let mut seen = [0i64; 26];
        let mut exact = 0;
        for i in 0..n {
            let c = (s[i as usize] - b'a') as usize;
            seen[c] += 1;
            if seen[c] == count {
                exact += 1;
            } else if seen[c] == count + 1 {
                exact -= 1;
            }
            if i >= len {
                let d = (s[(i - len) as usize] - b'a') as usize;
                if seen[d] == count {
                    exact -= 1;
                }
                seen[d] -= 1;
                if seen[d] == count {
                    exact += 1;
                }
            }
            if i + 1 >= len && exact == k {
                total += 1;
            }
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn text_of(n: i64, k: i64, count: i64, p: i64, seed: &mut i64) -> Vec<u8> {
    let mut out = Vec::new();
    let mut len = 0;
    while len < n {
        let c = b'a' + (next_random(seed) % k) as u8;
        let run = if next_random(seed) % 100 < p { count } else { 1 };
        for _ in 0..run.min(n - len) {
            out.push(c);
        }
        len += run.min(n - len);
    }
    out
}

fn main() {
    let mut seed = 2067;
    let mut total = 0;
    let mut check = 0;
    for t in 0..60 {
        let count = t % 7 + 1;
        let s = text_of(30000, t % 26 + 1, count, 50, &mut seed);
        let a = equal_count_substrings(&s, count);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("60 texts: sum {}, checksum {}", total, check);
}
