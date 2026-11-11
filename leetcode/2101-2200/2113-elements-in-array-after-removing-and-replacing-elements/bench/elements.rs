// LeetCode #2113: Elements in Array After Removing and Replacing Elements
// -- the benchmark, the same algorithm as elements.kara: each query's
// minute modulo the period `2n`, then one value or -1 for its phase.

fn element_in_nums(nums: &[i64], queries: &[(i64, i64)]) -> Vec<i64> {
    let n = nums.len() as i64;
    let mut ans: Vec<i64> = Vec::new();
    for &(time, index) in queries {
        let t = time % (2 * n);
        if t < n {
            if index < n - t {
                ans.push(nums[(t + index) as usize]);
            } else {
                ans.push(-1);
            }
        } else if index < t - n {
            ans.push(nums[index as usize]);
        } else {
            ans.push(-1);
        }
    }
    ans
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2113i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let nums: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 101).collect();
        arrays.push(nums);
    }
    let mut queries: Vec<(i64, i64)> = Vec::new();
    for _ in 0..100000 {
        let time = next_random(&mut seed) % 100001;
        queries.push((time, next_random(&mut seed) % 100));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for s in 0..50usize {
        let j = s * 1999 % 100000;
        queries[j] = (queries[j].0 + 1, queries[j].1);
        let mut sum = 0i64;
        for x in element_in_nums(&arrays[s % 20], &queries) {
            sum += x;
        }
        total += sum;
        check = (check * 31 + sum) % 1000000007;
    }
    println!("50 solves: {} summed, checksum {}", total, check);
}
