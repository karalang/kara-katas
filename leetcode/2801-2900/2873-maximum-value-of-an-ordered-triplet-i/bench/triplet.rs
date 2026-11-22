// LeetCode #2873: Maximum Value of an Ordered Triplet I -- the bench, as
// triplet.kara: 100000 arrays of 100 values, each answered 30 times by
// the one-pass arm.

fn maximum_triplet_value(nums: &[i64]) -> i64 {
    let mut best = 0;
    let mut top = 0;
    let mut gap = 0;
    for &v in nums {
        best = best.max(gap * v);
        gap = gap.max(top - v);
        top = top.max(v);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (100000, 30i64, 100);
    let mut seed = 2873;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000 + 1).collect();
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let best = maximum_triplet_value(nums);
            total += best;
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: values total {total}, checksum {check}");
}
