// LeetCode #2129: Capitalize the Title -- the benchmark, the same
// algorithm as title.kara.

fn capitalize_title(title: &str) -> String {
    let words: Vec<String> = title
        .split(' ')
        .map(|w| {
            let lower = w.to_lowercase();
            if lower.len() <= 2 {
                lower
            } else {
                format!("{}{}", lower[..1].to_uppercase(), &lower[1..])
            }
        })
        .collect();
    words.join(" ")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2129;
    let mut titles: Vec<Vec<u8>> = Vec::new();
    for _ in 0..1000 {
        let mut t: Vec<u8> = Vec::new();
        loop {
            let len = (next_random(&mut seed) % 6 + 1) as usize;
            if t.len() + 1 + len > 100 {
                break;
            }
            if !t.is_empty() {
                t.push(32);
            }
            for _ in 0..len {
                let k = next_random(&mut seed) % 52;
                t.push(if k < 26 { 97 + k } else { 39 + k } as u8);
            }
        }
        titles.push(t);
    }
    let mut capitals: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..200i64 {
        for k in 0..1000 {
            let n = titles[k].len() as i64;
            let mut p = (next_random(&mut seed) % n) as usize;
            if titles[k][p] == 32 {
                p -= 1;
            }
            titles[k][p] ^= 32;
            let title = String::from_utf8(titles[k].clone()).unwrap();
            let answer = capitalize_title(&title);
            for b in answer.bytes() {
                if (65..=90).contains(&b) {
                    capitals += 1;
                }
                check = (check * 31 + b as i64 + round) % 1000000007;
            }
        }
    }
    println!("200000 titles: {} capitals, checksum {}", capitals, check);
}
