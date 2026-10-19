// Benchmark for #775: Global and Local Inversions -- the ★ arm (every
// value at most one place from its index), as the Kāra program does it.

fn is_ideal_permutation(nums: &[i64]) -> bool {
    for i in 0..nums.len() {
        if (nums[i] - i as i64).abs() > 1 {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: usize = 64;
    let n: usize = 100000;
    let mut seed: i64 = 775;
    let mut perms: Vec<Vec<i64>> = Vec::new();
    for g in 0..count {
        let mut nums: Vec<i64> = (0..n as i64).collect();
        let mut i = 0;
        while i + 1 < n {
            if next_random(&mut seed) % 2 == 0 {
                nums.swap(i, i + 1);
                i += 2;
            } else {
                i += 1;
            }
        }
        if g % 4 == 1 {
            let at = n - 4 - (next_random(&mut seed) % 1000) as usize;
            nums.swap(at, at + 3);
        } else if g % 4 == 2 {
            let at = (next_random(&mut seed) % (n as i64 - 3)) as usize;
            nums.swap(at, at + 3);
        }
        perms.push(nums);
    }
    let mut ideals = 0;
    let mut checksum: i64 = 0;
    for round in 0..12000 {
        let g = (round * 7) % count;
        if is_ideal_permutation(&perms[g]) {
            ideals += 1;
            checksum = (checksum * 31 + g as i64 + 1) % 1000000007;
        } else {
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    println!("12000 rounds of {} values: {} ideal, checksum {}", n, ideals, checksum);
}
