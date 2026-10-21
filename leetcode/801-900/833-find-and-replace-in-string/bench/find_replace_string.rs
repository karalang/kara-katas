// Benchmark for #833: Find And Replace in String -- the ★ arm (a table by index).
//
// Mirrors find_replace_string.kara: each operation whose source occurs at
// its index is recorded in a table at that index, and one walk over the
// string writes each recorded operation's target in place of its source
// and copies the other letters.

fn find_replace_string(s: &str, indices: &[i64], sources: &[String], targets: &[String]) -> String {
    let n = s.len();
    let mut at = vec![-1i64; n];
    for k in 0..indices.len() {
        let i = indices[k] as usize;
        if s[i..].starts_with(sources[k].as_str()) {
            at[i] = k as i64;
        }
    }
    let mut out = String::new();
    let mut i = 0;
    while i < n {
        let k = at[i];
        if k >= 0 {
            out.push_str(&targets[k as usize]);
            i += sources[k as usize].len();
        } else {
            out.push_str(&s[i..i + 1]);
            i += 1;
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letter(r: i64) -> char {
    (b'a' + r as u8) as char
}

fn main() {
    let count = 64;
    let rounds: i64 = 300000;
    let n: i64 = 1000;
    let mut seed: i64 = 833;
    let mut cases: Vec<(String, Vec<i64>, Vec<String>, Vec<String>)> = Vec::new();
    for _ in 0..count {
        let mut s = String::new();
        for _ in 0..n {
            s.push(letter(next_random(&mut seed) % 2));
        }
        let mut indices: Vec<i64> = Vec::new();
        let mut sources: Vec<String> = Vec::new();
        let mut targets: Vec<String> = Vec::new();
        let mut pos = next_random(&mut seed) % 4;
        while pos < n && indices.len() < 100 {
            let room = if n - pos < 10 { n - pos } else { 10 };
            let len = 1 + next_random(&mut seed) % room;
            let mut src = s[pos as usize..(pos + len) as usize].to_string();
            if next_random(&mut seed) % 3 == 2 {
                let last = src.as_bytes()[len as usize - 1] as i64 - 97;
                let mut changed = src[0..len as usize - 1].to_string();
                changed.push(letter((last + 1) % 26));
                src = changed;
            }
            let mut target = String::new();
            for _ in 0..1 + next_random(&mut seed) % 7 {
                target.push(letter(next_random(&mut seed) % 26));
            }
            indices.push(pos);
            sources.push(src);
            targets.push(target);
            pos += len + next_random(&mut seed) % 4;
        }
        let mut i = indices.len();
        while i > 1 {
            let j = (next_random(&mut seed) % i as i64) as usize;
            i -= 1;
            indices.swap(i, j);
            sources.swap(i, j);
            targets.swap(i, j);
        }
        cases.push((s, indices, sources, targets));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let c = &cases[(round % count as i64) as usize];
        let out = find_replace_string(&c.0, &c.1, &c.2, &c.3);
        total += out.len() as i64;
        let b = out.as_bytes()[(round / count as i64) as usize % out.len()];
        checksum = (checksum * 131 + b as i64) % 1000000007;
    }
    println!("{} rounds of {} cases: {} letters, checksum {}", rounds, count, total, checksum);
}
