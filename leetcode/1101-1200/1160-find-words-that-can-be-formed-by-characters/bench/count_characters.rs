// LeetCode #1160 bench: the ★ arm's counts of each letter, the same
// workload as count_characters.kara.

fn count_characters(words: &[String], chars: &str) -> i64 {
    let mut have = [0i64; 26];
    for &c in chars.as_bytes() {
        have[(c - b'a') as usize] += 1;
    }
    let mut total = 0i64;
    for w in words {
        let mut need = [0i64; 26];
        let mut good = true;
        for &c in w.as_bytes() {
            let i = (c - b'a') as usize;
            need[i] += 1;
            if need[i] > have[i] {
                good = false;
                break;
            }
        }
        if good {
            total += w.len() as i64;
        }
    }
    total
}

fn main() {
    let passes = 1500i64;
    let mut seed: i64 = 1160;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut problems: Vec<(Vec<String>, String)> = Vec::new();
    for p in 0..12 {
        let kind = p % 3;
        let k = if kind == 1 { 4 } else { 26 };
        let chars: String = (0..100).map(|_| (b'a' + (next_random() % k) as u8) as char).collect();
        let mut words = Vec::with_capacity(1000);
        for i in 0..1000 {
            let w: String = if kind == 0 {
                let len = 1 + next_random() % 100;
                (0..len).map(|_| (b'a' + (next_random() % 26) as u8) as char).collect()
            } else if kind == 1 {
                let len = 1 + next_random() % 30;
                (0..len).map(|_| (b'a' + (next_random() % 4) as u8) as char).collect()
            } else {
                let mut b: Vec<u8> = chars.bytes().filter(|_| next_random() % 2 == 0).collect();
                if i % 2 == 1 {
                    let x = b[(next_random() % b.len() as i64) as usize];
                    b.push(x);
                }
                String::from_utf8(b).unwrap()
            };
            words.push(w);
        }
        problems.push((words, chars));
    }
    let mut check = 0i64;
    for p in 0..passes {
        for (words, chars) in &problems {
            check = (check * 31 + count_characters(words, chars) + p) % 1000000007;
        }
    }
    println!("{} passes over 12 problems of 1000 words: checksum {}", passes, check);
}
