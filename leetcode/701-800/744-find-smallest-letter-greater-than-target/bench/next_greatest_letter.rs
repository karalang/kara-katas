// LeetCode 744 — Find Smallest Letter Greater Than Target, bench: the ★
// arm (binary search) on lists of 10000 sorted letters, many random
// targets each. Mirrors next_greatest_letter.kara.

fn next_greatest_letter(letters: &[char], target: char) -> char {
    let mut lo = 0;
    let mut hi = letters.len();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if letters[mid] <= target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    if lo == letters.len() { letters[0] } else { letters[lo] }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 60;
    let n = 10000;
    let queries = 100000;
    let a = 'a' as i64;
    let z = 'z' as i64;
    let mut seed = 744;
    let mut total: i64 = 0;
    for _ in 0..rounds {
        let mut letters: Vec<char> = Vec::new();
        let mut c = a + next_random(&mut seed) % 6;
        for _ in 0..n {
            if next_random(&mut seed) % 500 == 0 && c < z {
                c += 1;
            }
            letters.push(c as u8 as char);
        }
        if letters[0] == letters[n - 1] {
            letters[n - 1] = (letters[0] as u8 + 1) as char;
        }
        for _ in 0..queries {
            let target = (a + next_random(&mut seed) % 26) as u8 as char;
            total += next_greatest_letter(&letters, target) as i64;
        }
    }
    println!("{} rounds of 100000 queries on 10000 letters: answers sum to {}", rounds, total);
}
