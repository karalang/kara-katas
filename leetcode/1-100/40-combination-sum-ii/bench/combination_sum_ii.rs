// LeetCode #40 bench mirror — Rust, the sorted same-level-dedup backtracker (★).
//
// Mirrors bench/combination_sum_ii.kara exactly: sort once, then an index-bounded DFS
// recursing at i+1 (each element used once) with the same-level duplicate skip and the
// suffix break, snapshotting the path into a Vec<Vec<i64>> at each leaf. Workload: TOTAL
// enumerations over a fixed duplicate-heavy multiset with a per-iteration target =
// 10 + k%13, folding a position-weighted per-combo signature plus the count into a rolling
// checksum. Prints the same sink as every other mirror.

fn backtrack(
    candidates: &[i64],
    start: usize,
    remaining: i64,
    path: &mut Vec<i64>,
    out: &mut Vec<Vec<i64>>,
) {
    if remaining == 0 {
        out.push(path.clone());
        return;
    }
    let n = candidates.len();
    let mut i = start;
    while i < n {
        let c = candidates[i];
        if c > remaining {
            break;
        }
        if i > start && c == candidates[i - 1] {
            i += 1;
            continue;
        }
        path.push(c);
        backtrack(candidates, i + 1, remaining - c, path, out);
        path.pop();
        i += 1;
    }
}

fn combination_sum2(candidates: &[i64], target: i64) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut path: Vec<i64> = Vec::new();
    backtrack(candidates, 0, target, &mut path, &mut out);
    out
}

fn main() {
    let total: i64 = 30000;
    let modulus: i64 = 1000000007;
    let mut candidates: Vec<i64> = vec![1, 1, 2, 2, 3, 3, 4, 5, 6, 7];
    candidates.sort();

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        let target = 10 + (k % 13);
        let combos = combination_sum2(&candidates, target);

        let mut sig: i64 = 0;
        for combo in &combos {
            let mut s: i64 = 0;
            let mut i: i64 = 0;
            let cl = combo.len() as i64;
            while i < cl {
                s += combo[i as usize] * (i + 1);
                i += 1;
            }
            sig = (sig * 31 + s) % modulus;
        }
        sig = (sig + combos.len() as i64) % modulus;
        acc = (acc * 131 + sig) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
