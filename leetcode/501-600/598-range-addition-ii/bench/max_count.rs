// Benchmark for #598: Rust mirror of the ★ arm (the smallest corner); see
// max_count.kara. Each operation is its own `Vec`, as LeetCode gives
// them and as the Kāra arm reads them.

fn max_count(m: i64, n: i64, ops: &[Vec<i64>]) -> i64 {
    let mut rows = m;
    let mut cols = n;
    for op in ops {
        rows = rows.min(op[0]);
        cols = cols.min(op[1]);
    }
    rows * cols
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = step(seed);
    let lo = step(seed);
    hi * 32768 + lo
}

fn main() {
    let count = 100;
    let rounds = 300;
    let mut seed: i64 = 598;
    let mut sizes: Vec<(i64, i64)> = Vec::new();
    let mut lists: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let m = 1 + wide(&mut seed) % 40000;
        let n = 1 + wide(&mut seed) % 40000;
        let mut ops: Vec<Vec<i64>> = Vec::new();
        for _ in 0..10000 {
            let a = m - step(&mut seed) % (1 + m / 8);
            let b = n - step(&mut seed) % (1 + n / 8);
            ops.push(vec![a, b]);
        }
        sizes.push((m, n));
        lists.push(ops);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let c = (round * 7 + g) % count;
            let (m, n) = sizes[c];
            let got = max_count(m, n, &lists[c]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} lists, {} rounds: total {}, checksum {}", count, rounds, total, checksum);
}
