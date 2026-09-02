// Benchmark mirror — LeetCode 304, Range Sum Query 2D (Immutable).
// Same algorithm, same flat prefix layout, same LCG, same masked sink as
// rangesum2d.kara. See ../README.md § Benchmarks.

fn main() {
    let n: i64 = 256;
    let stride: i64 = n + 1;
    let queries: i64 = 100000;
    let passes: i64 = 1800;
    let mut state: i64 = 20304;

    let mut m: Vec<i64> = Vec::with_capacity((n * n) as usize);
    for _ in 0..n * n {
        state = (state * 1103515245 + 12345) % 2147483648;
        m.push(state % 21 - 10);
    }

    let table = ((n + 1) * stride) as usize;
    let mut pre: Vec<i64> = vec![0; table];
    for r in 0..n {
        for c in 0..n {
            pre[((r + 1) * stride + (c + 1)) as usize] = pre[(r * stride + (c + 1)) as usize]
                + pre[((r + 1) * stride + c) as usize]
                - pre[(r * stride + c) as usize]
                + m[(r * n + c) as usize];
        }
    }

    let mut qr1: Vec<i64> = Vec::with_capacity(queries as usize);
    let mut qc1: Vec<i64> = Vec::with_capacity(queries as usize);
    let mut qr2: Vec<i64> = Vec::with_capacity(queries as usize);
    let mut qc2: Vec<i64> = Vec::with_capacity(queries as usize);
    for _ in 0..queries {
        state = (state * 1103515245 + 12345) % 2147483648;
        let a = state % n;
        state = (state * 1103515245 + 12345) % 2147483648;
        let b = state % n;
        state = (state * 1103515245 + 12345) % 2147483648;
        let c = state % n;
        state = (state * 1103515245 + 12345) % 2147483648;
        let d = state % n;
        if a <= b { qr1.push(a); qr2.push(b); } else { qr1.push(b); qr2.push(a); }
        if c <= d { qc1.push(c); qc2.push(d); } else { qc1.push(d); qc2.push(c); }
    }

    let mut checksum: i64 = 0;
    for _ in 0..passes {
        for k in 0..queries as usize {
            let r1 = qr1[k];
            let c1 = qc1[k];
            let r2 = qr2[k];
            let c2 = qc2[k];
            let v = pre[((r2 + 1) * stride + (c2 + 1)) as usize]
                - pre[(r1 * stride + (c2 + 1)) as usize]
                - pre[((r2 + 1) * stride + c1) as usize]
                + pre[(r1 * stride + c1) as usize];
            checksum = (checksum + v) & 0x3FFFFFFF;
        }
    }

    println!("checksum {}", checksum);
}
