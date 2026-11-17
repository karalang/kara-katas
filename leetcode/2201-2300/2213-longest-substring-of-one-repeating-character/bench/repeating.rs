// LeetCode #2213: Longest Substring of One Repeating Character -- bench
// mirror of repeating.kara: a segment tree over the letters, each node
// keeping the longest run from its start, from its end and inside.

fn pull(node: usize, lo: usize, hi: usize, letters: &[u8], prefix: &mut [i64], suffix: &mut [i64], best: &mut [i64]) {
    let mid = (lo + hi) / 2;
    let left = 2 * node;
    let right = 2 * node + 1;
    let joined = letters[mid] == letters[mid + 1];
    prefix[node] = if joined && prefix[left] == (mid - lo + 1) as i64 { prefix[left] + prefix[right] } else { prefix[left] };
    suffix[node] = if joined && suffix[right] == (hi - mid) as i64 { suffix[right] + suffix[left] } else { suffix[right] };
    best[node] = best[left].max(best[right]);
    if joined {
        best[node] = best[node].max(suffix[left] + prefix[right]);
    }
}

fn build(node: usize, lo: usize, hi: usize, letters: &[u8], prefix: &mut [i64], suffix: &mut [i64], best: &mut [i64]) {
    if lo == hi {
        prefix[node] = 1;
        suffix[node] = 1;
        best[node] = 1;
        return;
    }
    let mid = (lo + hi) / 2;
    build(2 * node, lo, mid, letters, prefix, suffix, best);
    build(2 * node + 1, mid + 1, hi, letters, prefix, suffix, best);
    pull(node, lo, hi, letters, prefix, suffix, best);
}

fn update(node: usize, lo: usize, hi: usize, at: usize, letters: &[u8], prefix: &mut [i64], suffix: &mut [i64], best: &mut [i64]) {
    if lo == hi {
        return;
    }
    let mid = (lo + hi) / 2;
    if at <= mid {
        update(2 * node, lo, mid, at, letters, prefix, suffix, best);
    } else {
        update(2 * node + 1, mid + 1, hi, at, letters, prefix, suffix, best);
    }
    pull(node, lo, hi, letters, prefix, suffix, best);
}

fn longest_repeating(s: &[u8], query_characters: &[u8], query_indices: &[usize]) -> Vec<i64> {
    let mut letters = s.to_vec();
    let n = letters.len();
    let mut prefix = vec![0i64; 4 * n];
    let mut suffix = vec![0i64; 4 * n];
    let mut best = vec![0i64; 4 * n];
    build(1, 0, n - 1, &letters, &mut prefix, &mut suffix, &mut best);
    let mut lengths = Vec::new();
    for (&letter, &at) in query_characters.iter().zip(query_indices.iter()) {
        letters[at] = letter;
        update(1, 0, n - 1, at, &letters, &mut prefix, &mut suffix, &mut best);
        lengths.push(best[1]);
    }
    lengths
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: usize, letters: i64, seed: &mut i64) -> Vec<u8> {
    (0..n).map(|_| b'a' + (next_random(seed) % letters) as u8).collect()
}

fn main() {
    let mut seed = 2213;
    let mut words = Vec::new();
    for w in 0..6 {
        // 10^5 letters from 2, 3 and 26 in turn, with 10^5 queries
        let letters = [2, 3, 26][w % 3];
        let s = random_word(100000, letters, &mut seed);
        let query_characters = random_word(100000, letters, &mut seed);
        let query_indices: Vec<usize> = (0..100000).map(|_| (next_random(&mut seed) % 100000) as usize).collect();
        words.push((s, query_characters, query_indices));
    }
    let mut check: i64 = 0;
    for (s, query_characters, query_indices) in &words {
        for length in longest_repeating(s, query_characters, query_indices) {
            check = (check * 31 + length) % 1000000007;
        }
    }
    println!("6 words of 10^5: checksum {check}");
}
