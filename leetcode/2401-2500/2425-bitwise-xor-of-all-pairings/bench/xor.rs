// LeetCode #2425: Bitwise XOR of All Pairings -- the bench, the ★ arm: the
// XOR of `nums1` when `nums2` has odd length, XORed with that of `nums2`
// when `nums1` has odd length.

fn xor_all_nums(nums1: &[i64], nums2: &[i64]) -> i64 {
    let mut answer = 0;
    if nums2.len() % 2 == 1 {
        for &x in nums1 {
            answer ^= x;
        }
    }
    if nums1.len() % 2 == 1 {
        for &y in nums2 {
            answer ^= y;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2425;
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    for i in 0..10i64 {
        for (list, n) in [(0, 100000 - i), (1, 100000 - i / 2 - 1)] {
            let mut nums: Vec<i64> = Vec::new();
            for _ in 0..n {
                let a = next_random(&mut seed);
                nums.push((a * 32768 + next_random(&mut seed)) % 1000000001);
            }
            if list == 0 {
                firsts.push(nums);
            } else {
                seconds.push(nums);
            }
        }
    }
    let mut check: i64 = 0;
    for p in 0..500i64 {
        for i in 0..10 {
            let at = ((p * 7919) % firsts[i].len() as i64) as usize;
            firsts[i][at] ^= p % 1024;
            check = (check * 31 + xor_all_nums(&firsts[i], &seconds[i]) + p) % 1000000007;
        }
    }
    println!("500 passes over 10 pairs of 10^5 values: checksum {}", check);
}
