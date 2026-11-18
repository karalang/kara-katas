// LeetCode #2294: Partition Array Such That Maximum Difference Is K --
// the bench, the ★ arm in Rust. Sort a copy (stable, as Kāra's `sort`),
// then open a group at each number more than k above the one that opened
// the last.

fn partition_array(nums: &[i64], k: i64) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut groups = 0;
    let mut low = -1;
    for &x in &sorted {
        if groups == 0 || x - low > k {
            groups += 1;
            low = x;
        }
    }
    groups
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2294;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % 100001);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for pass in 0..5 {
        for a in 0..20 {
            check = (check * 31 + partition_array(&arrays[a], 7 * a as i64 + pass)) % 1000000007;
        }
    }
    println!("5 passes over 20 arrays of 10^5: checksum {}", check);
}
