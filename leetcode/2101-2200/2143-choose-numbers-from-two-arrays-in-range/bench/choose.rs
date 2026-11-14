// LeetCode #2143: Choose Numbers From Two Arrays in Range -- the
// benchmark, the same algorithm as choose.kara.

fn count_subranges(nums1: &[i64], nums2: &[i64]) -> i64 {
    let modulus = 1000000007;
    let low: i64 = nums2.iter().sum();
    let high: i64 = nums1.iter().sum();
    let width = (low + high + 1) as usize;
    let low = low as usize;
    let mut ways = vec![0i64; width];
    let mut balanced = 0;
    for i in 0..nums1.len() {
        ways[low] += 1;
        let mut next = vec![0i64; width];
        let a = nums1[i] as usize;
        let b = nums2[i] as usize;
        for d in 0..width {
            if ways[d] > 0 {
                next[d + a] = (next[d + a] + ways[d]) % modulus;
                next[d - b] = (next[d - b] + ways[d]) % modulus;
            }
        }
        ways = next;
        balanced = (balanced + ways[low]) % modulus;
    }
    balanced
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2143;
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let nums1: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 101).collect();
        let nums2: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 101).collect();
        firsts.push(nums1);
        seconds.push(nums2);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..50 {
        for p in 0..4 {
            let at = (next_random(&mut seed) % 100) as usize;
            firsts[p][at] = next_random(&mut seed) % 101;
            seconds[p][at] = next_random(&mut seed) % 101;
            let ways = count_subranges(&firsts[p], &seconds[p]);
            total += ways;
            check = (check * 31 + ways + round) % 1000000007;
        }
    }
    println!("200 solves: {} ranges in all, checksum {}", total, check);
}
