// Benchmark harness for LeetCode #135 — Candy.
// Mirrors candy.kara algorithm-for-algorithm, including the explicit
// descending index loop for the right-to-left pass (not `.rev()`), so the
// generated loop shape matches.

fn candy(ratings: &[i64]) -> i64 {
    let n = ratings.len() as i64;
    if n == 0 {
        return 0;
    }
    let mut c: Vec<i64> = vec![1; n as usize];

    let mut i: i64 = 1;
    while i < n {
        if ratings[i as usize] > ratings[(i - 1) as usize] {
            c[i as usize] = c[(i - 1) as usize] + 1;
        }
        i += 1;
    }

    i = n - 2;
    while i >= 0 {
        if ratings[i as usize] > ratings[(i + 1) as usize]
            && c[i as usize] <= c[(i + 1) as usize]
        {
            c[i as usize] = c[(i + 1) as usize] + 1;
        }
        i -= 1;
    }

    let mut total: i64 = 0;
    for i in 0..n {
        total += c[i as usize];
    }
    total
}

fn lcg(seed: i64, n: i64, cap: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        let wd0 = x / 65536;
        x = (x * 1103515245 + 12345) % 2147483648;
        out.push((wd0 * 32768 + x / 65536) % cap);
    }
    out
}

fn main() {
    let np: i64 = 8;
    let n: i64 = 200000;
    let iters: i64 = 150;

    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for j in 0..np {
        if j % 2 == 0 {
            arrays.push(lcg(j + 1, n, 4));
        } else {
            arrays.push(lcg(j + 1, n, 100000));
        }
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink + candy(&arrays[idx])) % 1000000007;
    }
    println!("{}", sink);
}
