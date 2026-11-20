// LeetCode #1208 bench, in Rust: the ★ arm (a window over the letters,
// widened one letter a step and shrunk from the left while it costs more
// than the budget) on 16 pairs of strings of 100000 letters drawn once,
// then 10 rounds over the pairs with the budgets 0, 1000, 100000 and
// 1000000, every answer folded into a checksum.

fn equal_substring(s: &str, t: &str, max_cost: i64) -> i64 {
    let a = s.as_bytes();
    let b = t.as_bytes();
    let mut best = 0i64;
    let mut cost = 0i64;
    let mut left = 0usize;
    for right in 0..a.len() {
        cost += (a[right] as i64 - b[right] as i64).abs();
        while cost > max_cost {
            cost -= (a[left] as i64 - b[left] as i64).abs();
            left += 1;
        }
        best = best.max((right + 1 - left) as i64);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1208i64;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..16 {
        let mut s = String::with_capacity(100000);
        let mut t = String::with_capacity(100000);
        let mut spread = 2;
        for i in 0..100000 {
            if i % 1000 == 0 {
                spread = if next_random(&mut seed) % 2 == 0 { 2 } else { 25 };
            }
            let x = next_random(&mut seed) % 26;
            let y = (x + next_random(&mut seed) % (spread + 1)) % 26;
            s.push((b'a' + x as u8) as char);
            t.push((b'a' + y as u8) as char);
        }
        pairs.push((s, t));
    }
    let budgets = [0i64, 1000, 100000, 1000000];
    let mut check: i64 = 0;
    for round in 0..10 {
        for (s, t) in &pairs {
            for &c in &budgets {
                check = (check * 131 + equal_substring(s, t, c) + round) % 1000000007;
            }
        }
    }
    println!("10 rounds over 16 pairs of 100000 letters: checksum {check}");
}
