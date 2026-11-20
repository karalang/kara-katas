// LeetCode #2268: Minimum Number of Keypresses -- the bench, the ★ arm.

fn minimum_keypresses(s: &str) -> i64 {
    let mut count = vec![0i64; 26];
    for b in s.bytes() {
        count[(b - b'a') as usize] += 1;
    }
    count.sort_by(|a, b| b.cmp(a));
    let mut total = 0;
    for (i, c) in count.iter().enumerate() {
        total += c * (i as i64 / 9 + 1);
    }
    total
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2268;
    let mut check = 0;
    for t in 0..40 {
        let k = [3, 10, 12, 26][t % 4];
        let mut s = String::new();
        for _ in 0..100000 {
            s.push((b'a' + (next_random(&mut seed) % k) as u8) as char);
        }
        check = (check * 31 + minimum_keypresses(&s)) % 1000000007;
    }
    println!("40 strings of 10^5: checksum {check}");
}
