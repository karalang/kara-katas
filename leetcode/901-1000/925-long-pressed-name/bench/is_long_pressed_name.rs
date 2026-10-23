// LeetCode #925: Long Pressed Name -- bench: two pointers.
// Mirrors is_long_pressed_name.kara.

fn is_long_pressed_name(name: &str, typed: &str) -> bool {
    let a = name.as_bytes();
    let b = typed.as_bytes();
    let mut i = 0;
    for j in 0..b.len() {
        if i < a.len() && a[i] == b[j] {
            i += 1;
        } else if j > 0 && b[j] == b[j - 1] {
            continue;
        } else {
            return false;
        }
    }
    i == a.len()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count) = (150, 1000);
    let mut seed = 925;
    // count names of 400 letters from "abc", each typed with about one key
    // in four held down for up to three more presses, and every third one
    // mistyped once
    let mut names: Vec<String> = Vec::new();
    let mut typings: Vec<String> = Vec::new();
    for p in 0..count {
        let mut name: Vec<u8> = Vec::new();
        let mut typed: Vec<u8> = Vec::new();
        for _ in 0..400 {
            let c = b'a' + (next_random(&mut seed) % 3) as u8;
            name.push(c);
            let extra = if next_random(&mut seed) % 4 == 0 {
                1 + next_random(&mut seed) % 3
            } else {
                0
            };
            for _ in 0..1 + extra {
                typed.push(c);
            }
        }
        if p % 3 == 0 {
            let at = (next_random(&mut seed) % typed.len() as i64) as usize;
            typed[at] = b'a' + (next_random(&mut seed) % 3) as u8;
        }
        names.push(String::from_utf8(name).unwrap());
        typings.push(String::from_utf8(typed).unwrap());
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every pair, starting from a different one
        for i in 0..count {
            let p = (r + i) % count;
            if is_long_pressed_name(&names[p], &typings[p]) {
                yes += 1;
                check = (check * 1000003 + p as i64 + 1) % 1000000007;
            }
        }
    }
    println!(
        "{rounds} rounds over {count} names of 400 letters: {yes} long pressed, checksum {check}"
    );
}
