// LeetCode #686: Repeated String Match -- Knuth-Morris-Pratt. Bench.
//
// 100 pairs are built once: `a` of 1,000 to 10,000 letters over two
// letters, and `b` of 10,000 cut from the repetition of `a`, half of
// them with the last letter changed. Then 30 rounds answer every pair.

fn repeated_string_match(a: &str, b: &str) -> i64 {
    let x = a.as_bytes();
    let y = b.as_bytes();
    let n = x.len();
    let m = y.len();
    let mut fail: Vec<usize> = vec![0; m];
    let mut k = 0;
    for i in 1..m {
        while k > 0 && y[i] != y[k] {
            k = fail[k - 1];
        }
        if y[i] == y[k] {
            k += 1;
        }
        fail[i] = k;
    }
    let mut j = 0;
    for i in 0..n + m {
        let c = x[i % n];
        while j > 0 && c != y[j] {
            j = fail[j - 1];
        }
        if c == y[j] {
            j += 1;
        }
        if j == m {
            return ((i + 1 + n - 1) / n) as i64;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 100;
    let rounds: i64 = 30;
    let m: usize = 10000;
    let mut seed: i64 = 686;
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    for c in 0..count {
        let n = (1000 + next_random(&mut seed) % 9001) as usize;
        let mut a: Vec<u8> = Vec::new();
        for _ in 0..n {
            a.push((97 + next_random(&mut seed) % 2) as u8);
        }
        let start = next_random(&mut seed) as usize % n;
        let mut b: Vec<u8> = (0..m).map(|i| a[(start + i) % n]).collect();
        if c % 2 == 1 {
            b[m - 1] = 196 - b[m - 1];
        }
        firsts.push(String::from_utf8(a).unwrap());
        seconds.push(String::from_utf8(b).unwrap());
    }
    let mut sum: i64 = 0;
    let mut none = 0;
    for r in 0..rounds {
        for c in 0..count as usize {
            let k = repeated_string_match(&firsts[c], &seconds[c]);
            if k == -1 {
                none += 1;
            }
            sum = (sum * 31 + k + r + 2) % 1000000007;
        }
    }
    println!("{} pairs answered: {} with no answer, checksum {}", count * rounds, none, sum);
}
