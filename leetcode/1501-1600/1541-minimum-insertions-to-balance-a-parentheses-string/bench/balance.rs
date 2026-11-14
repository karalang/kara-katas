// LeetCode #1541: Minimum Insertions to Balance a Parentheses String --
// bench: the ★ arm (one pass keeping the ')' still wanted) over 100 strings
// of 1 to 100000 parentheses, built once, each asked 10 times. Rust mirror
// of balance.kara.

fn min_insertions(s: &str) -> i64 {
    let mut inserted = 0i64;
    let mut need = 0i64;
    for c in s.chars() {
        if c == '(' {
            if need % 2 == 1 {
                inserted += 1;
                need -= 1;
            }
            need += 2;
        } else {
            need -= 1;
            if need < 0 {
                inserted += 1;
                need = 1;
            }
        }
    }
    inserted + need
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1541i64;
    let mut strings = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let chance = next_random(&mut seed) % 101;
        let mut s = String::new();
        for _ in 0..n {
            s.push(if next_random(&mut seed) % 100 < chance { '(' } else { ')' });
        }
        strings.push(s);
    }
    let mut check = 0i64;
    for _ in 0..10 {
        for s in &strings {
            check = mix(check, min_insertions(s));
        }
    }
    println!("10 passes over 100 strings of up to 100000 parentheses: checksum {}", check);
}
