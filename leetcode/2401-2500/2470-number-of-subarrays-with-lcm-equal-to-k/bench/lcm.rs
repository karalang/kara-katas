// LeetCode #2470: Number of Subarrays With LCM Equal to K -- the bench,
// the ★ arm in Rust: from each start the running LCM, the walk stopped
// once it no longer divides `k`, the gcd recursive as in Kāra.

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn subarray_lcm(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let mut count = 0;
    for start in 0..n {
        let mut lcm = 1;
        for end in start..n {
            lcm = lcm / gcd(lcm, nums[end]) * nums[end];
            if k % lcm != 0 {
                break;
            }
            if lcm == k {
                count += 1;
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10 lists of 1000 numbers built once, each a random divisor of 720
    // but one in 50 any number from 1 to 1000; then 90 passes, each
    // setting one number of every list from the checksum so far, then
    // answering it with `k` 720 and folding the count plus the pass into
    // the checksum
    let mut seed = 2470;
    let divisors: Vec<i64> = (1..721).filter(|d| 720 % d == 0).collect();
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums = Vec::new();
        for _ in 0..1000 {
            if next_random(&mut seed) % 50 == 0 {
                nums.push(1 + next_random(&mut seed) % 1000);
            } else {
                nums.push(divisors[(next_random(&mut seed) % divisors.len() as i64) as usize]);
            }
        }
        lists.push(nums);
    }
    let mut check = 0i64;
    for p in 0..90i64 {
        for a in 0..lists.len() {
            lists[a][((check + a as i64) % 1000) as usize] = divisors[(check % divisors.len() as i64) as usize];
            check = (check * 31 + subarray_lcm(&lists[a], 720) + p) % 1000000007;
        }
    }
    println!("90 passes over 10 lists of 1000: checksum {}", check);
}
