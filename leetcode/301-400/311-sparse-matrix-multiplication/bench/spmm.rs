// Benchmark mirror — LeetCode 311, Sparse Matrix Multiplication.
// Same flat row-major layout, same LCG, same zero-skipping multiply, same
// per-pass perturbation and masked sink as spmm.kara. See ../README.md.

fn main() {
    let n: i64 = 320;
    let passes: i64 = 620;
    let cells = (n * n) as usize;
    let mut a: Vec<i64> = Vec::with_capacity(cells);
    let mut b: Vec<i64> = Vec::with_capacity(cells);
    let mut c: Vec<i64> = vec![0; cells];
    let mut state: i64 = 20311;
    for _ in 0..n * n {
        state = (state * 1103515245 + 12345) % 2147483648;
        if state % 100 < 4 { state = (state * 1103515245 + 12345) % 2147483648; a.push(state % 9 - 4); }
        else { a.push(0); }
        state = (state * 1103515245 + 12345) % 2147483648;
        if state % 100 < 4 { state = (state * 1103515245 + 12345) % 2147483648; b.push(state % 9 - 4); }
        else { b.push(0); }
    }

    let mut checksum: i64 = 0;
    for p in 0..passes {
        let slot = ((p * 7919) % (n * n)) as usize;
        a[slot] = a[slot] + (checksum & 1);
        for i in 0..cells { c[i] = 0; }
        for r in 0..n {
            let arow = (r * n) as usize;
            for k in 0..n {
                let av = a[arow + k as usize];
                if av != 0 {
                    let brow = (k * n) as usize;
                    for j in 0..n as usize { c[arow + j] += av * b[brow + j]; }
                }
            }
        }
        let mut acc: i64 = 0;
        for t in 0..cells { acc = (acc + c[t]) & 0x3FFFFFFF; }
        checksum = (checksum + acc) & 0x3FFFFFFF;
    }
    println!("checksum {}", checksum);
}
