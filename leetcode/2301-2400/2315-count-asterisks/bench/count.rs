// LeetCode #2315: Count Asterisks -- the bench, the ★ arm in Rust. One
// pass with a flag: each `|` flips whether the walk is inside a pair,
// and a `*` counts only outside one.

fn count_asterisks(s: &str) -> i64 {
    let mut inside = false;
    let mut count = 0i64;
    for c in s.chars() {
        if c == '|' {
            inside = !inside;
        } else if c == '*' && !inside {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2315i64;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let bars = next_random(&mut seed) % 8 + 2;
        let mut s = String::new();
        let mut count = 0;
        for _ in 0..999 {
            if next_random(&mut seed) % bars == 0 {
                s.push('|');
                count += 1;
            } else if next_random(&mut seed) % 2 == 0 {
                s.push('*');
            } else {
                s.push('a');
            }
        }
        s.push(if count % 2 == 1 { '|' } else { 'a' });
        strings.push(s);
    }
    let mut check = 0i64;
    for p in 0..100 {
        for a in 0..1000 {
            check = (check * 31 + count_asterisks(&strings[(7 * a + p) % 1000])) % 1000000007;
        }
    }
    println!("100 passes over 1000 strings of 1000 characters: checksum {}", check);
}
