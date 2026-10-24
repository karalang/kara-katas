// Benchmark: LeetCode #960 Delete Columns to Make Sorted III -- the ★
// arm, longest chain, on 100 strings of 100 letters, LeetCode's largest.
// Mirrors min_deletion_size.kara, .c, .py and go-seq/.

fn min_deletion_size(strs: &[String]) -> i64 {
    let n = strs.len();
    let m = strs[0].len();
    let mut longest = vec![1i64; m];
    let mut best = 0;
    for j in 0..m {
        for k in 0..j {
            let mut before = true;
            for s in strs.iter().take(n) {
                if s.as_bytes()[k] > s.as_bytes()[j] {
                    before = false;
                    break;
                }
            }
            if before {
                longest[j] = longest[j].max(longest[k] + 1);
            }
        }
        best = best.max(longest[j]);
    }
    m as i64 - best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn nearly_sorted(seed: &mut i64, n: usize, m: usize, letters: i64, swaps: usize) -> Vec<String> {
    let mut out = Vec::new();
    for _ in 0..n {
        let mut b: Vec<u8> = (0..m)
            .map(|_| b'a' + (next_random(seed) % letters) as u8)
            .collect();
        b.sort();
        for _ in 0..swaps {
            let p = (next_random(seed) % (m as i64 - 1)) as usize;
            b.swap(p, p + 1);
        }
        out.push(String::from_utf8(b).unwrap());
    }
    out
}

fn main() {
    let rounds = 40;
    let mut seed = 960;
    let cases: Vec<Vec<String>> = (0..50)
        .map(|i| nearly_sorted(&mut seed, 100, 100, 2 + i % 25, (i % 10) as usize))
        .collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..50 {
            let d = min_deletion_size(&cases[(r + i) % 50]);
            total += d;
            check = (check * 31 + d + i as i64) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over 50 cases of 100 strings of 100 letters: {total} columns deleted, checksum {check}"
    );
}
