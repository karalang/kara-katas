// LeetCode #2870: Minimum Number of Operations to Make Array Empty --
// the bench, as empty.kara: 50 arrays of 10^5 values, each answered 10
// times by the sorted-runs arm.

fn min_operations(nums: &[i64]) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut ops = 0;
    let mut i = 0;
    while i < sorted.len() {
        let mut j = i;
        while j < sorted.len() && sorted[j] == sorted[i] {
            j += 1;
        }
        let f = (j - i) as i64;
        if f == 1 {
            return -1;
        }
        ops += (f + 2) / 3;
        i = j;
    }
    ops
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (50, 10, 100000usize);
    let mut seed = 2870;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        while nums.len() < n {
            let v = wide(&mut seed) % 1000000 + 1;
            let copies = ((next_random(&mut seed) % 7 + 2) as usize).min(n - nums.len());
            for _ in 0..copies {
                nums.push(v);
            }
        }
        for i in (1..n).rev() {
            let j = (wide(&mut seed) % (i as i64 + 1)) as usize;
            nums.swap(i, j);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let ops = min_operations(nums);
            total += ops;
            check = (check * 31 + ops + 1 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: {total} operations, checksum {check}");
}
