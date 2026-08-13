// Benchmark workload for LeetCode #265 — Paint House II (Rust mirror).
// Mirrors paint_ii.kara algorithm-for-algorithm.

fn main() {
    let n: i64 = 4000;
    let k: i64 = 32;
    let rounds: i64 = 1300;
    let inf: i64 = 1000000000000;

    let mut cost: Vec<i64> = Vec::with_capacity((n * k) as usize);
    let mut state: i64 = 265265;
    for _ in 0..(n * k) {
        state = (state * 1103515245 + 12345) & 2147483647;
        cost.push((state / 65536) % 40 + 1);
    }

    let mut prev: Vec<i64> = vec![0; k as usize];
    let mut cur: Vec<i64> = vec![0; k as usize];

    let mut sink: i64 = 0;
    for r in 0..rounds {
        let start = (r * 7919) % n;

        for c in 0..k {
            prev[c as usize] = cost[(start * k + c) as usize];
        }

        for i in 1..n {
            let mut min1 = inf;
            let mut idx1: i64 = -1;
            let mut min2 = inf;
            for j in 0..k {
                let v = prev[j as usize];
                if v < min1 {
                    min2 = min1;
                    min1 = v;
                    idx1 = j;
                } else if v < min2 {
                    min2 = v;
                }
            }

            let row = ((start + i) % n) * k;
            for t in 0..k {
                let best = if t == idx1 { min2 } else { min1 };
                cur[t as usize] = cost[(row + t) as usize] + best;
            }

            std::mem::swap(&mut prev, &mut cur);
        }

        let mut answer = inf;
        let mut fold: i64 = 0;
        for p in 0..k {
            let v = prev[p as usize];
            if v < answer {
                answer = v;
            }
            fold = (fold * 31 + v) % 1000000007;
        }
        sink = (sink * 131 + answer + fold) % 1000000007;
    }

    println!("{}", sink);
}
