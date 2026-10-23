// LeetCode #873 bench: Rust mirror of len_longest_fib_subseq.kara (the ★
// arm, a HashMap from value to index) on the same 100 arrays.

use std::collections::HashMap;

fn len_longest_fib_subseq(arr: &[i64]) -> i64 {
    let n = arr.len();
    let mut index: HashMap<i64, usize> = HashMap::new();
    for (i, &x) in arr.iter().enumerate() {
        index.insert(x, i);
    }
    let mut longest = vec![vec![2i64; n]; n];
    let mut best = 0;
    for k in 0..n {
        for j in 0..k {
            let before = arr[k] - arr[j];
            if before < arr[j] {
                if let Some(&i) = index.get(&before) {
                    longest[j][k] = longest[i][j] + 1;
                    best = best.max(longest[j][k]);
                }
            }
        }
    }
    best
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn increasing(rng: &mut Rng, n: usize, gap: i64) -> Vec<i64> {
    let mut arr = Vec::new();
    let mut x = 0;
    for _ in 0..n {
        x += 1 + rng.next() % gap;
        arr.push(x);
    }
    arr
}

fn big(rng: &mut Rng) -> i64 {
    let hi = rng.next();
    (hi * 32768 + rng.next()) % 1000000000 + 1
}

fn scattered(rng: &mut Rng, n: usize, run: usize) -> Vec<i64> {
    let mut a = rng.next() % 1000 + 1;
    let mut b = a + rng.next() % 1000 + 1;
    let mut vals = vec![a, b];
    while vals.len() < run && a + b <= 1000000000 {
        let next = a + b;
        a = b;
        b = next;
        vals.push(b);
    }
    while vals.len() < n {
        vals.push(big(rng));
    }
    vals.sort();
    vals.dedup();
    vals
}

fn main() {
    let mut rng = Rng(873);
    let mut arrays = Vec::new();
    for k in 0..100 {
        arrays.push(if k % 2 == 0 { increasing(&mut rng, 1000, k % 5 + 2) } else { scattered(&mut rng, 1000, 10 + (k % 30) as usize) });
    }
    let mut total = 0;
    let mut check = 0i64;
    for arr in &arrays {
        let answer = len_longest_fib_subseq(arr);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    println!("100 arrays of 1000 values: lengths sum to {}, checksum {}", total, check);
}
