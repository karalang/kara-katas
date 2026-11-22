// LeetCode #2832: Maximal Range That Each Element Is Maximum in It --
// the bench, mirrored from ranges.kara: two passes of a falling stack.

fn maximum_length_of_ranges(nums: &[i64]) -> Vec<i64> {
    let n = nums.len();
    let mut left: Vec<i64> = vec![-1; n];
    let mut right: Vec<i64> = vec![n as i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        while let Some(&top) = stack.last() {
            if nums[top] > nums[i] {
                break;
            }
            stack.pop();
        }
        if let Some(&top) = stack.last() {
            left[i] = top as i64;
        }
        stack.push(i);
    }
    stack.clear();
    for i in (0..n).rev() {
        while let Some(&top) = stack.last() {
            if nums[top] > nums[i] {
                break;
            }
            stack.pop();
        }
        if let Some(&top) = stack.last() {
            right[i] = top as i64;
        }
        stack.push(i);
    }
    (0..n).map(|i| right[i] - left[i] - 1).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds = 20;
    let n: i64 = 100000;
    let mut seed = 2832;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = (1..=n).collect();
        for i in (1..n).rev() {
            let j = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let ans = maximum_length_of_ranges(nums);
            for &x in ans.iter() {
                total += x;
                check = (check * 31 + x + r) % 1000000007;
            }
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: ranges total {total}, checksum {check}");
}
