// LeetCode #2264: Largest 3-Same-Digit Number in String -- Rust mirror of
// the ★ arm (good.kara): one pass over the bytes, the largest digit seen
// three times running, three times over or "". Output is byte-identical
// to good.kara.

fn largest_good_integer(num: &str) -> String {
    let b = num.as_bytes();
    let mut best: Option<u8> = None;
    for i in 2..b.len() {
        if b[i - 2] == b[i] && b[i - 1] == b[i] {
            if best.is_none() || b[i] > best.unwrap() {
                best = Some(b[i]);
            }
        }
    }
    match best {
        Some(d) => (d as char).to_string().repeat(3),
        None => String::new(),
    }
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2264;
    let mut check: i64 = 0;
    for t in 0..2000 {
        let digits = if t % 2 == 0 { 4 } else { 10 };
        let mut num = String::new();
        for _ in 0..1000 {
            num.push((b'0' + (next_random(&mut seed) % digits) as u8) as char);
        }
        let good = largest_good_integer(&num);
        let score: i64 = if good.is_empty() { 1000 } else { good.parse().unwrap() };
        check = (check * 31 + score) % 1000000007;
    }
    println!("2000 numbers of 1000: checksum {check}");
}
