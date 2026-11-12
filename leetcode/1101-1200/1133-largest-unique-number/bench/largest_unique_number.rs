// LeetCode #1133: Largest Unique Number -- the bench in Rust, the same
// algorithm and workload as largest_unique_number.kara: each array its own
// `Vec<i64>`, a fixed array of 1001 counts per call, the same 256 arrays of
// 2000 values and 1000 rounds.

fn largest_unique_number(nums: &[i64]) -> i64 {
    let mut count = [0i64; 1001];
    for &x in nums {
        count[x as usize] += 1;
    }
    for v in (0..1001).rev() {
        if count[v] == 1 {
            return v as i64;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1133;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..256 {
        let nums: Vec<i64> = (0..2000).map(|_| next_random(&mut seed) % 1001).collect();
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..1000i64 {
        for j in 0..256usize {
            let at = ((round * 7919 + j as i64 * 104729) % 2000) as usize;
            arrays[j][at] = (arrays[j][at] * 7 + 13) % 1001;
            let r = largest_unique_number(&arrays[j]);
            total += r;
            check = (check * 31 + r + 1) % 1000000007;
        }
    }
    println!("1000 rounds over 256 arrays of 2000 values: answers total {}, checksum {}", total, check);
}
