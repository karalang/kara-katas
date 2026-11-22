// LeetCode #2861: Maximum Number of Alloys -- the bench: the ★ arm over
// 100 cases of 100 metals and 100 machines, LeetCode's most, amounts
// drawn over LeetCode's full ranges, all drawn first, then each
// answered 20 times.

fn max_number_of_alloys(n: usize, _k: usize, budget: i64, composition: &[Vec<i64>], stock: &[i64], cost: &[i64]) -> i64 {
    let mut best = 0;
    for machine in composition.iter() {
        let price = |x: i64| -> i64 { (0..n).map(|j| (machine[j] * x - stock[j]).max(0) * cost[j]).sum() };
        let mut lo = 0;
        let mut hi = 200000000;
        while lo < hi {
            let mid = (lo + hi + 1) / 2;
            if price(mid) <= budget {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        best = best.max(lo);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

struct Case {
    budget: i64,
    composition: Vec<Vec<i64>>,
    stock: Vec<i64>,
    cost: Vec<i64>,
}

fn main() {
    let count = 100;
    let rounds = 20;
    let n = 100;
    let mut seed = 2861;
    let mut cases: Vec<Case> = Vec::new();
    for _ in 0..count {
        let composition: Vec<Vec<i64>> = (0..n).map(|_| (0..n).map(|_| 1 + wide(&mut seed) % 100).collect()).collect();
        let stock: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 100000001).collect();
        let cost: Vec<i64> = (0..n).map(|_| 1 + wide(&mut seed) % 100).collect();
        let budget = wide(&mut seed) % 100000001;
        cases.push(Case { budget, composition, stock, cost });
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for t in cases.iter() {
            let alloys = max_number_of_alloys(n, n, t.budget, &t.composition, &t.stock, &t.cost);
            total += alloys;
            check = (check * 31 + alloys + r) % 1000000007;
        }
    }
    println!("{count} cases of {n} by {n}, {rounds} rounds: {total} alloys, checksum {check}");
}
