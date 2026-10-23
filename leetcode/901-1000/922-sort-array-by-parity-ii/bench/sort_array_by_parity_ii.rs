// LeetCode #922: Sort Array By Parity II -- bench: two pointers, in place.
// Mirrors sort_array_by_parity_ii.kara.

fn sort_array_by_parity_ii(nums: &mut Vec<i64>) {
    let mut j = 1;
    let mut i = 0;
    while i < nums.len() {
        if nums[i] % 2 == 1 {
            while nums[j] % 2 == 1 {
                j += 2;
            }
            nums.swap(i, j);
        }
        i += 2;
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 3000;
    let n = 20000;
    let mut seed = 922;
    // n / 2 even and n / 2 odd values up to 1000, shuffled, built once
    let mut original: Vec<i64> = Vec::new();
    for k in 0..n {
        let v = 2 * (next_random(&mut seed) % 500);
        original.push(if k % 2 == 0 { v } else { v + 1 });
    }
    let mut i = n - 1;
    while i > 0 {
        let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
        original.swap(i, j);
        i -= 1;
    }
    let mut check: i64 = 0;
    for r in 0..rounds {
        // a fresh copy each round, rearranged, and one value read back
        let mut nums = original.clone();
        sort_array_by_parity_ii(&mut nums);
        check = (check * 1000003 + nums[(r * 7919) % n]) % 1000000007;
    }
    println!("{rounds} rounds over {n} values: checksum {check}");
}
