// LeetCode #1331 bench, Rust mirror of the Kāra bench: the ★ arm (the
// values sorted, their repeats removed, and each value's rank found by
// binary search) on 20 arrays of 10^5 values, the constraints' longest,
// each from 1 to 10^9 or from a narrower spread with many repeats, built
// once. Then 15 passes, each setting one value of every array from the
// checksum so far, answering it and folding two of its ranks plus the pass
// into the checksum.

fn array_rank_transform(arr: &[i32]) -> Vec<i32> {
    let mut distinct = arr.to_vec();
    distinct.sort();
    distinct.dedup();
    arr.iter().map(|x| (distinct.binary_search(x).unwrap() + 1) as i32).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 100000;
    let mut seed: i64 = 1331;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for t in 0..20 {
        let spread = if t % 2 == 0 { 1000000000 } else { 1000 };
        let mut arr: Vec<i32> = Vec::new();
        for _ in 0..n {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            arr.push(((a * 61036 + b) % spread + 1) as i32);
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for pass in 0..15 {
        for t in 0..20 {
            let at = (check % n as i64) as usize;
            arrays[t][at] = (check / 7 % 1000000000 + 1) as i32;
            let ranks = array_rank_transform(&arrays[t]);
            check = (check * 31 + ranks[at] as i64 + ranks[n - 1] as i64 + pass) % 1000000007;
        }
    }
    println!("15 passes over 20 arrays of 10^5: checksum {check}");
}
