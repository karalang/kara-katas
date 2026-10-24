// Benchmark: LeetCode #940 Distinct Subsequences II -- the ★ arm,
// doubling less the repeats, on 100 words of 2000 letters, LeetCode's
// longest, in 200 rounds. Mirrors distinct_subseq_ii.kara, .c, .py and
// go-seq/.

fn distinct_subseq_ii(s: &str) -> i64 {
    let m = 1000000007;
    let b = s.as_bytes();
    let n = b.len();
    let mut count: Vec<i64> = vec![1];
    let mut last = vec![0usize; 26];
    for i in 0..n {
        let c = (b[i] - b'a') as usize;
        let mut next = 2 * count[i] % m;
        if last[c] > 0 {
            next = (next - count[last[c] - 1] + m) % m;
        }
        count.push(next);
        last[c] = i + 1;
    }
    (count[n] - 1 + m) % m
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 200;
    let count = 100;
    let mut seed = 940;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..count {
        let k = 1 + next_random(&mut seed) % 26;
        let mut s = String::new();
        for _ in 0..2000 {
            s.push((next_random(&mut seed) % k + 97) as u8 as char);
        }
        words.push(s);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let a = distinct_subseq_ii(&words[(r + i) % count]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!(
        "{} rounds over {} words of 2000 letters: counts adding to {}, checksum {}",
        rounds, count, total, check
    );
}
