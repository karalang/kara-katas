// LeetCode #1209 bench, in Rust: the ★ arm (a stack of runs, each a letter
// and how many times it has come in a row, a run popped when it reaches
// `k`) on 12 strings of 100000 letters drawn once, then 10 rounds over the
// strings with k = 2, 3 and 4, each answer's length and last letter folded
// into a checksum.

fn remove_duplicates(s: &str, k: i64) -> String {
    let mut runs: Vec<(char, i64)> = Vec::new();
    for c in s.chars() {
        match runs.last_mut() {
            Some(top) if top.0 == c => {
                top.1 += 1;
                if top.1 == k {
                    runs.pop();
                }
            }
            _ => runs.push((c, 1)),
        }
    }
    let mut out = String::with_capacity(s.len());
    for &(c, n) in &runs {
        for _ in 0..n {
            out.push(c);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(seed: &mut i64, n: usize, letters: i64) -> String {
    let mut out = String::with_capacity(n);
    for _ in 0..n {
        out.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    out
}

fn main() {
    let mut seed = 1209i64;
    let mut texts: Vec<String> = Vec::new();
    for i in 0..12 {
        if i < 4 {
            texts.push(random_text(&mut seed, 100000, 2));
        } else if i < 8 {
            texts.push(random_text(&mut seed, 100000, 3));
        } else {
            let half = random_text(&mut seed, 50000, 26);
            let mirror: String = half.chars().rev().collect();
            texts.push(format!("{half}{mirror}"));
        }
    }
    let mut check: i64 = 0;
    for round in 0..10 {
        for s in &texts {
            for k in 2..5 {
                let answer = remove_duplicates(s, k);
                let last = answer.as_bytes().last().map_or(0, |&b| b as i64);
                check = (check * 131 + answer.len() as i64 + last + round) % 1000000007;
            }
        }
    }
    println!("10 rounds over 12 strings of 100000 letters: checksum {check}");
}
