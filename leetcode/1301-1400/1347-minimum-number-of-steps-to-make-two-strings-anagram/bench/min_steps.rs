// LeetCode #1347 bench -- Rust: one count per letter, up for s and down
// for t, the positive counts summed.

fn min_steps(s: &str, t: &str) -> i32 {
    let mut count = [0i32; 26];
    for b in s.bytes() {
        count[(b - b'a') as usize] += 1;
    }
    for b in t.bytes() {
        count[(b - b'a') as usize] -= 1;
    }
    count.iter().filter(|&&c| c > 0).sum()
}

fn main() {
    let mut seed: i64 = 1347;
    let mut text = String::with_capacity(1000000);
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        text.push((b'a' + ((seed / 65536) % 26) as u8) as char);
    }
    let mut check: i64 = 0;
    for q in 0..1000i64 {
        let n = 40000 + check % 10001;
        let a = (check % (1000000 - n)) as usize;
        let b = ((check / 7) % (1000000 - n)) as usize;
        let n = n as usize;
        let steps = min_steps(&text[a..a + n], &text[b..b + n]) as i64;
        check = (check * 31 + steps + q) % 1000000007;
    }
    println!("1000 queries over a text of 10^6: checksum {}", check);
}
