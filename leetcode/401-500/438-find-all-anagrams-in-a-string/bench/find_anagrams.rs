// Benchmark for #438: mirror of find_anagrams.kara (a sliding window of
// letter counts) on 40 patterns searched in one random text of
// 1,000,000 letters.

fn find_anagrams(s: &str, p: &str) -> Vec<i64> {
    let sb = s.as_bytes();
    let pb = p.as_bytes();
    let n = sb.len();
    let m = pb.len();
    let mut starts: Vec<i64> = Vec::new();
    if m > n {
        return starts;
    }
    // need[c] is p's count of c minus the window's.
    let mut need = vec![0i64; 26];
    for i in 0..m {
        need[(pb[i] - b'a') as usize] += 1;
    }
    let mut differ = 0;
    for c in 0..26 {
        if need[c] != 0 {
            differ += 1;
        }
    }
    for i in 0..n {
        let enter = (sb[i] - b'a') as usize;
        if need[enter] == 0 {
            differ += 1;
        }
        need[enter] -= 1;
        if need[enter] == 0 {
            differ -= 1;
        }
        if i >= m {
            let leave = (sb[i - m] - b'a') as usize;
            if need[leave] == 0 {
                differ += 1;
            }
            need[leave] += 1;
            if need[leave] == 0 {
                differ -= 1;
            }
        }
        if i + 1 >= m && differ == 0 {
            starts.push((i + 1 - m) as i64);
        }
    }
    starts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size = 1000000;
    let patterns = 40;
    let mut seed: i64 = 438;
    // Letters from 'a' to 'd', so that short patterns have many
    // anagrams in the text.
    let mut text = String::new();
    for _ in 0..size {
        text.push((b'a' + (next_random(&mut seed) % 4) as u8) as char);
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..patterns {
        let length = 1 + next_random(&mut seed) % 12;
        let mut p = String::new();
        for _ in 0..length {
            p.push((b'a' + (next_random(&mut seed) % 4) as u8) as char);
        }
        let starts = find_anagrams(&text, &p);
        found += starts.len();
        for i in starts {
            checksum = (checksum * 31 + i) % 1000000007;
        }
    }
    println!("{} patterns in a text of {}: {} anagrams, checksum {}", patterns, size, found, checksum);
}
