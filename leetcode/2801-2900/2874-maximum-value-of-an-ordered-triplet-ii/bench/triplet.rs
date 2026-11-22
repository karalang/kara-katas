// LeetCode #2874: Maximum Value of an Ordered Triplet II -- the bench, as
// triplet.kara: 50 arrays of 10^5 values, each answered 20 times by the
// one-pass arm.

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
    let (count, rounds, n) = (50, 20i64, 100000);
    let mut seed = 2874;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let nums: Vec<i64> = (0..n)
            .map(|i| {
                if c % 2 == 1 {
                    (1000000 - i * 9 - wide(&mut seed) % 100000).max(1)
                } else {
                    wide(&mut seed) % 1000000 + 1
                }
            })
            .collect();
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
