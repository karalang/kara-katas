// LeetCode #1838: Frequency of the Most Frequent Element -- the bench in Rust: the ★ arm over
// 200 calls on the first 50000 to 99999 of one list of 10^5 numbers from 1
// to 10^5, built once, with `k` from 1 to 10^5, each run's length and `k`
// drawn from the checksum so far. Each call copies its run, and the arm
// sorts a copy of its own.

fn max_frequency(nums: &[i64], k: i64) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut best = 0;
    let mut first = 0;
    let mut sum = 0;
    for last in 0..sorted.len() {
        sum += sorted[last];
        while sorted[last] * (last - first + 1) as i64 - sum > k {
            sum -= sorted[first];
            first += 1;
        }
        best = best.max(last - first + 1);
    }
    best as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1838;
    let mut base: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        base.push(1 + (hi * 32768 + next_random(&mut seed)) % 100000);
    }
    let mut check: i64 = 0;
    for call in 0..200 {
        let n = (50000 + (check + call) % 50000) as usize;
        let k = 1 + (check * 7 + call) % 100000;
        let run = base[..n].to_vec();
        check = (check * 31 + max_frequency(&run, k)) % 1000000007;
    }
    println!("200 calls: checksum {}", check);
}
