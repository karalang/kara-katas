// Benchmark twin for LeetCode #288 — same algorithm as uniqueabbr.kara.
use std::collections::HashMap;

// Sole(word) | Conflicted, mirroring the Kara enum.
enum Bucket {
    Sole(String),
    Conflicted,
}

fn abbrev(w: &str) -> String {
    let n = w.len();
    if n <= 2 {
        return w.to_string();
    }
    let b = w.as_bytes();
    format!("{}{}{}", b[0] as char, n - 2, b[n - 1] as char)
}

fn next_rand(state: i64) -> i64 {
    (state * 1103515245 + 12345) & 2147483647
}

fn main() {
    const LETTERS: &[u8] = b"abcdefghijklmnopqrstuvwxyz";
    let dict_n: i64 = 3000;
    let pool_n: i64 = 20000;
    let punches: i64 = 1000000;
    let mut seed: i64 = 12345;

    let mut dict: Vec<String> = Vec::new();
    for _ in 0..dict_n {
        seed = next_rand(seed);
        let n = 3 + ((seed / 65536) % 8);
        let mut w = String::new();
        for _ in 0..n {
            seed = next_rand(seed);
            w.push(LETTERS[((seed / 65536) % 26) as usize] as char);
        }
        dict.push(w);
    }

    let mut idx: HashMap<String, Bucket> = HashMap::new();
    for w in &dict {
        let a = abbrev(w);
        match idx.get(&a) {
            None => {
                idx.insert(a, Bucket::Sole(w.clone()));
            }
            Some(Bucket::Sole(prev)) => {
                if prev != w {
                    idx.insert(a, Bucket::Conflicted);
                }
            }
            Some(Bucket::Conflicted) => {}
        }
    }

    let mut pool: Vec<String> = Vec::new();
    for i in 0..pool_n {
        if i % 2 == 0 {
            pool.push(dict[((i * 7) % dict_n) as usize].clone());
        } else {
            seed = next_rand(seed);
            let n = 3 + ((seed / 65536) % 8);
            let mut w = String::new();
            for _ in 0..n {
                seed = next_rand(seed);
                w.push(LETTERS[((seed / 65536) % 26) as usize] as char);
            }
            pool.push(w);
        }
    }

    let mut unique_count: i64 = 0;
    for i in 0..punches {
        let word = &pool[(i % pool_n) as usize];
        let a = abbrev(word);
        let u = match idx.get(&a) {
            None => true,
            Some(Bucket::Sole(w)) => w == word,
            Some(Bucket::Conflicted) => false,
        };
        if u {
            unique_count += 1;
        }
    }
    println!("unique {}", unique_count);
}
