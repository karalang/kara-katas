// benchmark's Rust mirror of moves.kara (LeetCode #2193, the ★ arm): the
// twin swapped out to the end, over a copy of the word's bytes.

fn min_moves_to_make_palindrome(s: &str) -> i64 {
    let mut b: Vec<u8> = s.bytes().collect();
    let mut left = 0;
    let mut right = b.len() - 1;
    let mut moves = 0;
    while left < right {
        let mut k = right;
        while k > left && b[k] != b[left] {
            k -= 1;
        }
        if k == left {
            b.swap(left, left + 1);
            moves += 1;
            continue;
        }
        while k < right {
            b.swap(k, k + 1);
            k += 1;
            moves += 1;
        }
        left += 1;
        right -= 1;
    }
    moves
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64) -> String {
    let mut chars: Vec<char> = Vec::new();
    for _ in 0..1000 {
        let c = (97 + next_random(seed) % 26) as u8 as char;
        chars.push(c);
        chars.push(c);
    }
    for i in (1..2000).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        chars.swap(i, j);
    }
    chars.into_iter().collect()
}

fn main() {
    let mut seed = 2193;
    let words: Vec<String> = (0..20).map(|_| random_word(&mut seed)).collect();
    let mut check: i64 = 0;
    for r in 0..3000 {
        check = (check * 31 + min_moves_to_make_palindrome(&words[r % 20])) % 1000000007;
    }
    println!("3000 solves: checksum {}", check);
}
