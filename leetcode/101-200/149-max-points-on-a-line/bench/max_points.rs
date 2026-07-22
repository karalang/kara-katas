//! Benchmark workload — Max Points on a Line, O(n^2 log n) sort-based variant.
//! Algorithmic mirror of bench/max_points.kara / .c / .py / go-seq. See
//! ../README.md § Benchmarks for N / K and the deterministic LCG generator.

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

fn max_points(xs: &[i64], ys: &[i64]) -> i64 {
    let n = xs.len();
    if n <= 2 {
        return n as i64;
    }
    let mut best: i64 = 1;
    let mut slopes: Vec<i64> = Vec::with_capacity(n);
    for i in 0..n {
        slopes.clear();
        let mut dup: i64 = 0;
        for j in (i + 1)..n {
            let mut dx = xs[j] - xs[i];
            let mut dy = ys[j] - ys[i];
            if dx == 0 && dy == 0 {
                dup += 1;
            } else {
                let g = gcd(dx.abs(), dy.abs());
                dx /= g;
                dy /= g;
                if dx < 0 || (dx == 0 && dy < 0) {
                    dx = -dx;
                    dy = -dy;
                }
                slopes.push(dx * 4096 + dy);
            }
        }
        slopes.sort_unstable();
        let mut local: i64 = 0;
        let mut run: i64 = 0;
        for k in 0..slopes.len() {
            if k == 0 || slopes[k] != slopes[k - 1] {
                run = 1;
            } else {
                run += 1;
            }
            if run > local {
                local = run;
            }
        }
        let cand = local + dup + 1;
        if cand > best {
            best = cand;
        }
    }
    best
}

fn main() {
    const N: usize = 1200;
    let mut xs = vec![0i64; N];
    let mut ys = vec![0i64; N];
    let mut state: i64 = 12345;
    for i in 0..N {
        state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 2_147_483_647;
        xs[i] = state & 1023;
        state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 2_147_483_647;
        ys[i] = state & 1023;
    }
    let mut sum: i64 = 0;
    for _ in 0..8 {
        sum += max_points(&xs, &ys);
    }
    println!("{}", sum);
}
