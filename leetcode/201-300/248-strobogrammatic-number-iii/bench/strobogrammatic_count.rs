// Benchmark workload for LeetCode #248 — Strobogrammatic Number III (Rust mirror).
// Mirrors strobogrammatic_count.kara algorithm-for-algorithm: closed form for
// interior lengths, boundary lengths enumerated and filtered.

const PAIR_A: [&str; 5] = ["0", "1", "6", "8", "9"];
const PAIR_B: [&str; 5] = ["0", "1", "9", "8", "6"];

fn pow5(e: i64) -> i64 {
    let mut acc = 1i64;
    for _ in 0..e {
        acc *= 5;
    }
    acc
}

fn count_of_length(len: i64) -> i64 {
    if len <= 0 {
        return 0;
    }
    if len == 1 {
        return 3;
    }
    let mut total = 4 * pow5(len / 2 - 1);
    if len % 2 == 1 {
        total *= 3;
    }
    total
}

fn build(k: i64, n: i64) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    if k == 0 {
        out.push(String::new());
        return out;
    }
    if k == 1 {
        out.push("0".to_string());
        out.push("1".to_string());
        out.push("8".to_string());
        return out;
    }
    let inner = build(k - 2, n);
    for s in &inner {
        for p in 0..5 {
            if PAIR_A[p] == "0" && k == n {
                continue;
            }
            let mut t = String::from(PAIR_A[p]);
            t.push_str(s);
            t.push_str(PAIR_B[p]);
            out.push(t);
        }
    }
    out
}

fn cmp_digits(a: &str, b: &str) -> i64 {
    let (xs, ys) = (a.as_bytes(), b.as_bytes());
    if xs.len() != ys.len() {
        return if xs.len() < ys.len() { -1 } else { 1 };
    }
    for i in 0..xs.len() {
        if xs[i] != ys[i] {
            return if xs[i] < ys[i] { -1 } else { 1 };
        }
    }
    0
}

fn count_bounded(len: i64, low: &str, high: &str, use_lo: bool, use_hi: bool) -> i64 {
    let cands = build(len, len);
    let mut n = 0i64;
    for s in &cands {
        let mut keep = true;
        if use_lo && cmp_digits(s, low) < 0 {
            keep = false;
        }
        if use_hi && cmp_digits(s, high) > 0 {
            keep = false;
        }
        if keep {
            n += 1;
        }
    }
    n
}

fn count_in_range(low: &str, high: &str) -> i64 {
    let lo_len = low.as_bytes().len() as i64;
    let hi_len = high.as_bytes().len() as i64;
    if lo_len > hi_len {
        return 0;
    }
    if lo_len == hi_len {
        if cmp_digits(low, high) > 0 {
            return 0;
        }
        return count_bounded(lo_len, low, high, true, true);
    }
    let mut total = count_bounded(lo_len, low, high, true, false);
    total += count_bounded(hi_len, low, high, false, true);
    let mut len = lo_len + 1;
    while len < hi_len {
        total += count_of_length(len);
        len += 1;
    }
    total
}

fn digits_of(v: i64) -> String {
    if v == 0 {
        return "0".to_string();
    }
    let mut rev: Vec<i64> = Vec::new();
    let mut x = v;
    while x > 0 {
        rev.push(x % 10);
        x /= 10;
    }
    let mut s = String::new();
    for i in (0..rev.len()).rev() {
        s.push_str(&format!("{}", rev[i]));
    }
    s
}

fn main() {
    let queries: i64 = 1000;
    let mut state: i64 = 248248;
    let mut sink: i64 = 0;

    for _ in 0..queries {
        state = (state * 1103515245 + 12345) & 2147483647;
        let da = (state / 65536) % 8 + 1;
        state = (state * 1103515245 + 12345) & 2147483647;
        let db = (state / 65536) % 8 + 1;

        state = (state * 1103515245 + 12345) & 2147483647;
        let ra = (state / 65536) % 9000 + 1;
        state = (state * 1103515245 + 12345) & 2147483647;
        let rb = (state / 65536) % 9000 + 1;

        let mut a = ra;
        let mut i = 1i64;
        while i < da {
            a = a * 10 % 1000000000000000 + (i % 10);
            i += 1;
        }
        let mut b = rb;
        let mut j = 1i64;
        while j < db {
            b = b * 10 % 1000000000000000 + (j % 10);
            j += 1;
        }
        if a > b {
            std::mem::swap(&mut a, &mut b);
        }

        let n = count_in_range(&digits_of(a), &digits_of(b));
        sink = (sink + n) % 1000000007;
    }
    println!("{}", sink);
}
