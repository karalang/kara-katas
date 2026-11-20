// LeetCode #1249 bench, in Rust: the ★ arm (a stack of the places of the
// `(` not yet closed, and a `Vec<bool>` of the characters to keep) on 50
// random strings of 100000 characters built once, each with its own share
// of parentheses, each asked 4 times; every kept string folded into a
// checksum.

fn min_remove_to_make_valid(s: &str) -> String {
    let chars: Vec<char> = s.chars().collect();
    let mut keep = vec![true; chars.len()];
    let mut open: Vec<usize> = Vec::new();
    for (i, &c) in chars.iter().enumerate() {
        if c == '(' {
            open.push(i);
        } else if c == ')' && open.pop().is_none() {
            keep[i] = false;
        }
    }
    for &i in &open {
        keep[i] = false;
    }
    let mut out = String::new();
    for (i, &c) in chars.iter().enumerate() {
        if keep[i] {
            out.push(c);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(n: i64, percent: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        if next_random(seed) % 100 < percent {
            s.push(if next_random(seed) % 2 == 0 { '(' } else { ')' });
        } else {
            s.push(['a', 'b', 'c', 'd', 'e'][(next_random(seed) % 5) as usize]);
        }
    }
    s
}

fn main() {
    let mut seed = 1249;
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..50 {
        let percent = next_random(&mut seed) % 101;
        texts.push(random_text(100000, percent, &mut seed));
    }
    let mut check: i64 = 0;
    for _ in 0..4 {
        for s in &texts {
            let kept = min_remove_to_make_valid(s);
            for c in kept.chars() {
                check = (check * 131 + c as i64) % 1000000007;
            }
        }
    }
    println!("4 rounds of 50 strings of 100000 characters: checksum {check}");
}
