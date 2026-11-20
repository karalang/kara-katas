// LeetCode #1224 bench, Rust mirror of the Kāra ★ arm: each number's count
// and how many numbers have each count, over 10 random arrays of 10^5
// numbers drawn once, 5 passes; checksum of the answers.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn max_equal_freq(nums: &[i64]) -> i64 {
    let top = *nums.iter().max().unwrap();
    let mut count = vec![0i64; top as usize + 1];
    let mut with_count = vec![0i64; nums.len() + 1];
    let mut most = 0i64;
    let mut best = 0i64;
    for (k, &x) in nums.iter().enumerate() {
        let x = x as usize;
        with_count[count[x] as usize] -= 1;
        count[x] += 1;
        with_count[count[x] as usize] += 1;
        most = most.max(count[x]);
        let len = k as i64 + 1;
        if most == 1
            || with_count[most as usize] * most + 1 == len
            || (with_count[(most - 1) as usize] + 1) * (most - 1) + 1 == len
        {
            best = len;
        }
    }
    best
}

fn main() {
    let mut seed: i64 = 1224;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..10 {
        let values: i64 = 2 << a;
        arrays.push((0..100000).map(|_| next_random(&mut seed) % values + 1).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..5 {
        for nums in arrays.iter() {
            let answer = max_equal_freq(nums);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("10 arrays of 10^5 numbers, 5 passes: lengths total {}, checksum {}", total, check);
}
