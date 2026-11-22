// LeetCode #2863: Maximum Length of Semi-Decreasing Subarrays -- the
// bench: the ★ arm over 100 arrays of 10^5 values, LeetCode's most,
// every other one random over LeetCode's range and the rest rising with
// five values moved, all drawn first, then each answered 10 times.

fn max_subarray_length(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut starts: Vec<usize> = Vec::new();
    for i in 0..n {
        if starts.is_empty() || nums[i] > nums[starts[starts.len() - 1]] {
            starts.push(i);
        }
    }
    let mut best = 0;
    for j in (0..n).rev() {
        while let Some(&i) = starts.last() {
            if nums[i] <= nums[j] {
                break;
            }
            best = best.max((j - i + 1) as i64);
            starts.pop();
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 100;
    let rounds = 10;
    let n = 100000i64;
    let mut seed = 2863;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let mut nums: Vec<i64> = if c % 2 == 0 {
            (0..n).map(|_| wide(&mut seed) % 2000000001 - 1000000000).collect()
        } else {
            (0..n).map(|i| 20000 * i - 1000000000).collect()
        };
        if c % 2 == 1 {
            for _ in 0..5 {
                let i = (wide(&mut seed) % n) as usize;
                nums[i] = wide(&mut seed) % 2000000001 - 1000000000;
            }
        }
        arrays.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let longest = max_subarray_length(nums);
            total += longest;
            check = (check * 31 + longest + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}");
}
