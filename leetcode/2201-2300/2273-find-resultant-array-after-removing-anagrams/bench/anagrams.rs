// LeetCode #2273: Find Resultant Array After Removing Anagrams -- the
// bench, the ★ arm.

fn sorted_letters(word: &str) -> String {
    let mut letters: Vec<char> = word.chars().collect();
    letters.sort();
    letters.iter().collect()
}

fn remove_anagrams(words: &[String]) -> Vec<String> {
    let mut kept: Vec<String> = Vec::new();
    let mut last = String::new();
    for w in words {
        let key = sorted_letters(w);
        if kept.is_empty() || key != last {
            kept.push(w.clone());
        }
        last = key;
    }
    kept
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2273;
    let mut check: i64 = 0;
    for _ in 0..20000 {
        let mut words: Vec<String> = Vec::new();
        for i in 0..100 {
            if i > 0 && next_random(&mut seed) % 2 == 0 {
                let mut letters: Vec<char> = words[i - 1].chars().collect();
                for j in (1..10usize).rev() {
                    let r = (next_random(&mut seed) % (j as i64 + 1)) as usize;
                    letters.swap(j, r);
                }
                words.push(letters.iter().collect());
            } else {
                let mut w = String::new();
                for _ in 0..10 {
                    w.push((b'a' + (next_random(&mut seed) % 4) as u8) as char);
                }
                words.push(w);
            }
        }
        let kept = remove_anagrams(&words);
        check = (check * 31 + kept.len() as i64 * 1000 + kept[kept.len() - 1].as_bytes()[0] as i64) % 1000000007;
    }
    println!("20000 lists of 100: checksum {check}");
}
