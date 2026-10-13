// Benchmark for #500: Rust mirror of the ★ arm (a row number for every
// letter); see keyboard_row.kara. Each list is handed over by value, as
// the Kāra list is, and each word lower-cased into a fresh String.

fn find_words(words: Vec<String>) -> Vec<String> {
    let rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
    let mut row_of = [0i64; 26];
    for r in 0..3 {
        for ch in rows[r].chars() {
            row_of[ch as usize - 'a' as usize] = r as i64;
        }
    }
    let mut out: Vec<String> = Vec::new();
    for word in words {
        let mut first = -1;
        let mut one_row = true;
        for ch in word.to_lowercase().chars() {
            let r = row_of[ch as usize - 'a' as usize];
            if first < 0 {
                first = r;
            } else if r != first {
                one_row = false;
                break;
            }
        }
        if one_row {
            out.push(word.clone());
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20,000 lists of 20 words of 1 to 100 letters, each word from one
    // row (2 in 3) or the whole alphabet, a letter upper case with odds
    // 1 in 4, built once. Then each list is solved once.
    let rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "abcdefghijklmnopqrstuvwxyz"];
    let pools: Vec<Vec<char>> = rows.iter().map(|r| r.chars().collect()).collect();
    let lists = 20000;
    let mut seed: i64 = 500;
    let mut all: Vec<Vec<String>> = Vec::new();
    for _ in 0..lists {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..20 {
            let pool = if next_random(&mut seed) % 3 == 0 { 3 } else { (next_random(&mut seed) % 3) as usize };
            let length = 1 + next_random(&mut seed) % 100;
            let mut word = String::new();
            for _ in 0..length {
                let ch = pools[pool][(next_random(&mut seed) % pools[pool].len() as i64) as usize];
                if next_random(&mut seed) % 4 == 0 {
                    word.push(ch.to_ascii_uppercase());
                } else {
                    word.push(ch);
                }
            }
            words.push(word);
        }
        all.push(words);
    }
    let mut kept = 0i64;
    let mut letters = 0i64;
    let mut checksum: i64 = 0;
    for words in all {
        for word in find_words(words) {
            kept += 1;
            letters += word.len() as i64;
            checksum = (checksum * 31 + word.len() as i64 + word.as_bytes()[0] as i64) % 1000000007;
        }
    }
    println!("{} lists of 20 words: {} words kept, {} letters, checksum {}", lists, kept, letters, checksum);
}
