// Benchmark mirror for #616: the same workload and algorithm as
// add_bold_tag.kara (mark, then write).

fn add_bold_tag(s: &str, words: &[String]) -> String {
    let n = s.len();
    let mut bold = vec![false; n];
    for i in 0..n {
        for word in words {
            if s[i..n].starts_with(word.as_str()) {
                for k in i..i + word.len() {
                    bold[k] = true;
                }
            }
        }
    }
    let mut out = String::new();
    for i in 0..n {
        if bold[i] && (i == 0 || !bold[i - 1]) {
            out.push_str("<b>");
        }
        out.push_str(&s[i..i + 1]);
        if bold[i] && (i == n - 1 || !bold[i + 1]) {
            out.push_str("</b>");
        }
    }
    out
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(size: i64, seed: &mut i64) -> String {
    (0..size).map(|_| (97 + step(seed) % 4) as u8 as char).collect()
}

fn main() {
    let cases = 20i64;
    let rounds = 1000i64;
    let mut seed: i64 = 616;
    let mut texts: Vec<String> = Vec::new();
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..cases {
        let s = random_text(1000, &mut seed);
        let mut words: Vec<String> = Vec::new();
        while words.len() < 100 {
            let length = 5 + step(&mut seed) % 10;
            let w = if words.len() % 2 == 0 {
                let at = (step(&mut seed) % (1000 - length)) as usize;
                s[at..at + length as usize].to_string()
            } else {
                random_text(length, &mut seed)
            };
            if !words.contains(&w) {
                words.push(w);
            }
        }
        texts.push(s);
        lists.push(words);
    }
    let (mut total, mut checksum) = (0i64, 0i64);
    for r in 0..rounds {
        let c = ((r * 7) % cases) as usize;
        let out = add_bold_tag(&texts[c], &lists[c]);
        total += out.len() as i64;
        for ch in out.chars() {
            checksum = (checksum * 31 + ch as i64) % 1000000007;
        }
    }
    println!("{} cases, {} rounds: {} characters, checksum {}", cases, rounds, total, checksum);
}
