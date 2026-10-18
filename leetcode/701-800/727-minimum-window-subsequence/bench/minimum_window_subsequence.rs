// LeetCode #727: Minimum Window Subsequence -- forward, then back.
// Benchmark mirror of the Kara star arm: walk s1 forward matching s2 in
// order, walk back from where the last letter matched to find the
// latest start, keep the window if shorter, and begin again one place
// after its start.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: i64, kinds: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push((b'a' + (next_random(seed) % kinds) as u8) as char);
    }
    s
}

fn min_window(s1: &str, s2: &str) -> String {
    let a = s1.as_bytes();
    let b = s2.as_bytes();
    let n = a.len() as i64;
    let m = b.len() as i64;
    let mut best_start: i64 = -1;
    let mut best_len = n + 1;
    let mut i: i64 = 0;
    while i < n {
        let mut j: i64 = 0;
        while i < n {
            if a[i as usize] == b[j as usize] {
                j += 1;
                if j == m {
                    break;
                }
            }
            i += 1;
        }
        if j < m {
            break;
        }
        let end = i;
        let mut k = m - 1;
        let mut p = end;
        while k >= 0 {
            if a[p as usize] == b[k as usize] {
                k -= 1;
            }
            p -= 1;
        }
        let start = p + 1;
        if end - start + 1 < best_len {
            best_len = end - start + 1;
            best_start = start;
        }
        i = start + 1;
    }
    if best_start < 0 {
        return String::new();
    }
    s1[best_start as usize..(best_start + best_len) as usize].to_string()
}

fn main() {
    let mut seed: i64 = 727;
    let mut texts: Vec<String> = Vec::new();
    for _ in 0..10 {
        texts.push(random_word(20000, 8, &mut seed));
    }
    let mut sum = 0;
    for _ in 0..300 {
        for d in 0..10 {
            let word = random_word(20, 8, &mut seed);
            sum += min_window(&texts[d], &word).len();
        }
    }
    println!("300 rounds of 10 texts of 20000 letters: sum {}", sum);
}
