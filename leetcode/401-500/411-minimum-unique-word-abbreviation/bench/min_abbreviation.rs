// Benchmark for #411: mirror of min_abbreviation.kara (masks over the
// letters).

fn abbreviate(t: &[u8], mask: i64) -> String {
    let mut out = String::new();
    let mut run = 0;
    for i in 0..t.len() {
        if (mask >> i) & 1 == 1 {
            if run > 0 {
                out.push_str(&run.to_string());
                run = 0;
            }
            out.push(t[i] as char);
        } else {
            run += 1;
        }
    }
    if run > 0 {
        out.push_str(&run.to_string());
    }
    out
}

fn mask_length(m: i64, mask: i64) -> i64 {
    let mut length = 0;
    let mut in_run = false;
    for i in 0..m {
        if (mask >> i) & 1 == 1 {
            length += 1;
            in_run = false;
        } else if !in_run {
            length += 1;
            in_run = true;
        }
    }
    length
}

fn min_abbreviation(target: &str, dictionary: &[String]) -> String {
    let t = target.as_bytes();
    let m = t.len() as i64;
    let mut diffs: Vec<i64> = Vec::new();
    for word in dictionary {
        let w = word.as_bytes();
        if w.len() as i64 == m {
            let mut diff = 0;
            for i in 0..m as usize {
                if w[i] != t[i] {
                    diff |= 1 << i;
                }
            }
            diffs.push(diff);
        }
    }
    let mut best_mask = (1i64 << m) - 1;
    let mut best_length = m;
    for mask in 0..(1i64 << m) {
        let length = mask_length(m, mask);
        if length < best_length {
            let mut unique = true;
            for d in 0..diffs.len() {
                if mask & diffs[d] == 0 {
                    unique = false;
                    break;
                }
            }
            if unique {
                best_length = length;
                best_mask = mask;
            }
        }
    }
    abbreviate(t, best_mask)
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let targets: i64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(30);
    let m = 20;
    let words = 2;
    let mut seed: i64 = 411;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..targets {
        let mut target = String::new();
        for _ in 0..m {
            target.push((97 + step(&mut seed) % 2) as u8 as char);
        }
        let mut dictionary: Vec<String> = Vec::new();
        while dictionary.len() < words {
            let mut word = String::new();
            for _ in 0..m {
                word.push((97 + step(&mut seed) % 2) as u8 as char);
            }
            if word != target {
                dictionary.push(word);
            }
        }
        let abbr = min_abbreviation(&target, &dictionary);
        total += abbr.len() as i64;
        for b in abbr.bytes() {
            checksum = (checksum * 31 + b as i64) % 1000000007;
        }
    }
    println!("{} targets of {} letters, {} words each: total {}, checksum {}", targets, m, words, total, checksum);
}
