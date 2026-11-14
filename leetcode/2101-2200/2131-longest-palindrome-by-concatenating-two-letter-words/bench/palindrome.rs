// LeetCode #2131: Longest Palindrome by Concatenating Two Letter Words --
// the benchmark, the same algorithm as palindrome.kara.

fn longest_palindrome(words: &[String]) -> i64 {
    let mut count = vec![0i64; 26 * 26];
    for w in words.iter() {
        let b = w.as_bytes();
        count[(b[0] - 97) as usize * 26 + (b[1] - 97) as usize] += 1;
    }
    let mut length = 0;
    let mut middle = false;
    for x in 0..26 {
        length += count[x * 26 + x] / 2 * 4;
        if count[x * 26 + x] % 2 == 1 {
            middle = true;
        }
        for y in x + 1..26 {
            length += count[x * 26 + y].min(count[y * 26 + x]) * 4;
        }
    }
    if middle {
        length += 2;
    }
    length
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(seed: &mut i64) -> String {
    let letters = b"abcdefgh";
    let a = (next_random(seed) % 8) as usize;
    let b = (next_random(seed) % 8) as usize;
    String::from_utf8(vec![letters[a], letters[b]]).unwrap()
}

fn main() {
    let mut seed = 2131;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..20 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..100000 {
            words.push(word(&mut seed));
        }
        lists.push(words);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..10i64 {
        for k in 0..20usize {
            let at = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000) as usize;
            lists[k][at] = word(&mut seed);
            let length = longest_palindrome(&lists[k]);
            total += length;
            check = (check * 31 + length + round) % 1000000007;
        }
    }
    println!("200 solves: {} letters in all, checksum {}", total, check);
}
