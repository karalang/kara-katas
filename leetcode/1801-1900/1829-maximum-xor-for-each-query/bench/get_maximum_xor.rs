// LeetCode #1829: Maximum XOR for Each Query -- the bench in Rust: the ★ arm
// over 200 calls on the first 50000 to 99999 of one sorted list of 10^5
// numbers below 2^20, built once, each run's length drawn from the checksum so
// far, and maximumBit 20. Each call copies its run, as the arm takes its list
// by value.

fn get_maximum_xor(nums: Vec<i64>, maximum_bit: i64) -> Vec<i64> {
    let mask = (1 << maximum_bit) - 1;
    let mut all = 0;
    for &x in nums.iter() {
        all ^= x;
    }
    let mut answer: Vec<i64> = Vec::new();
    for i in (0..nums.len()).rev() {
        answer.push(all ^ mask);
        all ^= nums[i];
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1829;
    let mut base: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        base.push((hi * 32768 + next_random(&mut seed)) % 1048576);
    }
    base.sort();
    let mut check: i64 = 0;
    for call in 0..200 {
        let n = (50000 + (check + call) % 50000) as usize;
        let answer = get_maximum_xor(base[..n].to_vec(), 20);
        let total: i64 = answer.iter().sum();
        check = (check * 31 + total % 1000000007) % 1000000007;
    }
    println!("200 calls: checksum {}", check);
}
