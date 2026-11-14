// LeetCode #1156 bench -- mirrors max_rep_opt1.kara: the same 64 texts,
// the same passes, the ★ arm's runs.

fn max_rep_opt1(text: &str) -> i64 {
    let b = text.as_bytes();
    let mut count = vec![0i64; 26];
    for &c in b.iter() {
        count[(c - b'a') as usize] += 1;
    }
    let mut runs: Vec<(u8, i64)> = Vec::new();
    let mut i = 0;
    while i < b.len() {
        let mut j = i;
        while j < b.len() && b[j] == b[i] {
            j += 1;
        }
        runs.push((b[i], (j - i) as i64));
        i = j;
    }
    let mut best = 0;
    for r in 0..runs.len() {
        let (c, len) = runs[r];
        let have = count[(c - b'a') as usize];
        best = best.max((len + 1).min(have));
        if r + 2 < runs.len() && runs[r + 1].1 == 1 && runs[r + 2].0 == c {
            best = best.max((len + runs[r + 2].1 + 1).min(have));
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let passes = 100;
    let mut seed = 1156;
    let mut texts: Vec<String> = Vec::new();
    for t in 0..64 {
        let mut b: Vec<u8> = Vec::new();
        while b.len() < 20000 {
            if t % 4 == 3 {
                for _ in 0..1 + next_random(&mut seed) % 40 {
                    b.push(b'a');
                }
                b.push(b'b' + (next_random(&mut seed) % 25) as u8);
            } else {
                let letters = [2, 3, 26][t % 4];
                b.push(b'a' + (next_random(&mut seed) % letters) as u8);
            }
        }
        b.truncate(20000);
        texts.push(String::from_utf8(b).unwrap());
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for text in texts.iter() {
            check = (check * 31 + max_rep_opt1(text) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 64 texts of 20000 letters: checksum {check}");
}
