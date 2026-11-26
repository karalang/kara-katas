// LeetCode #1781: Sum of Beauty of All Substrings -- the bench in Rust,
// mirroring beauty_sum.kara: the letters' counts grown from each start.

fn beauty_sum(s: &str) -> i32 {
    let letters: Vec<char> = s.chars().collect();
    let n = letters.len();
    let mut total: i32 = 0;
    for i in 0..n {
        let mut counts = [0i32; 26];
        for j in i..n {
            counts[(letters[j] as u32 - 'a' as u32) as usize] += 1;
            let mut most: i32 = 0;
            let mut fewest = n as i64;
            for &c in counts.iter() {
                if c > 0 {
                    most = most.max(c);
                    fewest = fewest.min(c as i64);
                }
            }
            total += (most as i64 - fewest) as i32;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1781;
    let mut words: Vec<String> = Vec::new();
    for w in 0..48i64 {
        let letters = 2 + w % 12 * 2;
        let mut s = String::new();
        for _ in 0..500 {
            s.push(char::from_u32((97 + next_random(&mut seed) % letters) as u32).unwrap());
        }
        words.push(s);
    }
    let mut check: i64 = 0;
    for w in 0..48 {
        check = (check * 31 + beauty_sum(&words[w]) as i64) % 1000000007;
    }
    println!("48 strings of 500 letters: checksum {}", check);
}
