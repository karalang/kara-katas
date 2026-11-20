// LeetCode #1272 bench, in Rust: the ★ arm (one pass; an interval the cut
// misses kept whole, one it meets keeping its parts before and after) on 20
// random lists of 10,000 intervals drawn once, each cut three ways, 40
// rounds; every interval kept folded into a checksum. Each interval is its
// own two-element array, as LeetCode's `int[][]` is.

fn remove_interval(intervals: &[Vec<i64>], to_be_removed: &[i64]) -> Vec<Vec<i64>> {
    let (lo, hi) = (to_be_removed[0], to_be_removed[1]);
    let mut out: Vec<Vec<i64>> = Vec::new();
    for iv in intervals.iter() {
        let (a, b) = (iv[0], iv[1]);
        if b <= lo || a >= hi {
            out.push(vec![a, b]);
            continue;
        }
        if a < lo {
            out.push(vec![a, lo]);
        }
        if b > hi {
            out.push(vec![hi, b]);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1272;
    let mut lists: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut list: Vec<Vec<i64>> = Vec::new();
        let mut at = -1000000;
        for _ in 0..10000 {
            let a = at + next_random(&mut seed) % 50;
            let b = a + 1 + next_random(&mut seed) % 50;
            list.push(vec![a, b]);
            at = b;
        }
        lists.push(list);
    }
    let mut check: i64 = 0;
    for round in 0..40 {
        for list in &lists {
            for cut in [[-990000i64, -800000], [-700000, -699990], [-1000000, 1000000]] {
                let kept = remove_interval(list, &cut);
                check = (check * 131 + kept.len() as i64 + round) % 1000000007;
                for iv in &kept {
                    check = (check * 131 + iv[0] + iv[1] + 2000000) % 1000000007;
                }
            }
        }
    }
    println!("40 rounds of 20 lists cut 3 ways: checksum {}", check);
}
