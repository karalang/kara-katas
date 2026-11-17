// LeetCode #1187: Make Array Strictly Increasing -- the ★ arm in Rust: for
// each count k of replacements so far, the least value the prefix can end
// on, over the same pairs as the Kāra bench.

fn make_array_increasing(arr1: &[i64], arr2: &[i64]) -> i64 {
    let mut spare = arr2.to_vec();
    spare.sort();
    spare.dedup();
    let n = arr1.len();
    let none = i64::MAX;
    let mut end = vec![none; n + 1];
    end[0] = i64::MIN;
    for &a in arr1.iter() {
        let mut next = vec![none; n + 1];
        for k in 0..=n {
            if end[k] != none && a > end[k] {
                next[k] = a;
            }
            if k > 0 && end[k - 1] != none {
                let p = spare.partition_point(|&b| b <= end[k - 1]);
                if p < spare.len() && spare[p] < next[k] {
                    next[k] = spare[p];
                }
            }
        }
        end = next;
    }
    match (0..=n).find(|&k| end[k] != none) {
        Some(k) => k as i64,
        None => -1,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn values(seed: &mut i64, n: i64, span: i64) -> Vec<i64> {
    (0..n)
        .map(|_| {
            let hi = next_random(seed);
            (hi * 32768 + next_random(seed)) % span
        })
        .collect()
}

fn main() {
    let mut seed: i64 = 1187;
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    firsts.push(values(&mut seed, 2000, 1000000001));
    seconds.push(values(&mut seed, 2000, 1000000001));
    firsts.push((0..2000).map(|i| if i % 40 == 39 { 0 } else { i * 500000 }).collect());
    seconds.push(values(&mut seed, 2000, 1000000001));
    firsts.push(values(&mut seed, 2000, 4000));
    seconds.push(values(&mut seed, 2000, 4000));
    firsts.push((0..2000).map(|i| (2000 - i) * 1000).collect());
    seconds.push(values(&mut seed, 2000, 1000000001));
    let rounds = 6;
    let mut check: i64 = 0;
    for round in 0..rounds {
        for p in 0..4 {
            let ops = make_array_increasing(&firsts[p], &seconds[p]);
            check = (check * 131 + ops + 2 + round) % 1000000007;
        }
    }
    println!("{} rounds of 4 pairs of 2000 values: checksum {}", rounds, check);
}
