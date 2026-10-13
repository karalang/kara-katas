// Benchmark for #471 -- Rust mirror of the ★ arm (encode_string.kara):
// interval DP over the encodings, with the shortest unit found where t
// first appears again in t + t.

fn encode(s: &str) -> String {
    let n = s.len();
    let mut best: Vec<Vec<String>> = vec![vec![String::new(); n]; n];
    for len in 1..=n {
        for i in 0..=n - len {
            let j = i + len - 1;
            let t = &s[i..=j];
            let doubled = format!("{t}{t}");
            let unit = 1 + doubled[1..].find(t).unwrap();
            let mut shortest = t.to_string();
            if unit < len {
                let packed = format!("{}[{}]", len / unit, best[i][i + unit - 1]);
                if packed.len() < shortest.len() {
                    shortest = packed;
                }
            }
            for k in i..j {
                if best[i][k].len() + best[k + 1][j].len() < shortest.len() {
                    shortest = format!("{}{}", best[i][k], best[k + 1][j]);
                }
            }
            best[i][j] = shortest;
        }
    }
    best[0][n - 1].clone()
}

// ---- bench ------------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_string(seed: &mut i64, letters: i64, depth: i64) -> String {
    let mut s = String::new();
    let pieces = 1 + next_random(seed) % 4;
    for _ in 0..pieces {
        if depth > 0 && next_random(seed) % 2 == 0 {
            let unit = random_string(seed, letters, depth - 1);
            let copies = 2 + next_random(seed) % 11;
            for _ in 0..copies {
                s.push_str(&unit);
            }
        } else {
            s.push((97 + next_random(seed) % letters) as u8 as char);
        }
    }
    s
}

fn main() {
    let count = 400;
    let size = 150;
    let mut seed: i64 = 471;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        let letters = 2 + next_random(&mut seed) % 2;
        let mut s = String::new();
        while s.len() < size {
            s.push_str(&random_string(&mut seed, letters, 2));
        }
        strings.push(s[..size].to_string());
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for i in 0..count {
        let e = encode(&strings[i]);
        total += e.len();
        checksum = (checksum * 31 + e.len() as i64) % 1000000007;
    }
    println!("{count} strings of {size} letters: {total} letters encoded, checksum {checksum}");
}
