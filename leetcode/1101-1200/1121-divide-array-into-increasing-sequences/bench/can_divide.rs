// LeetCode #1121: Divide Array Into Increasing Sequences -- the bench in
// Rust: the ★ arm over 4 sorted arrays of 100000 values, each round
// copying one value over its neighbour and answering for a new `k`.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn can_divide_into_subsequences(nums: &[i32], k: i32) -> bool {
    let mut longest = 0i64;
    let mut run = 0i64;
    for i in 0..nums.len() {
        if i > 0 && nums[i] == nums[i - 1] {
            run += 1;
        } else {
            run = 1;
        }
        longest = longest.max(run);
    }
    longest * k as i64 <= nums.len() as i64
}

fn main() {
    let n = 100000usize;
    let tops = [2000i64, 1000, 500, 200];
    let mut seed = 1121i64;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for &top in tops.iter() {
        let mut nums: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % top + 1) as i32).collect();
        nums.sort();
        arrays.push(nums);
    }
    let mut yes = 0i64;
    let mut check = 0i64;
    for round in 0..250usize {
        for j in 0..arrays.len() {
            let at = (round * 7919 + j * 104729) % (n - 2) + 1;
            arrays[j][at] = if round % 2 == 0 { arrays[j][at + 1] } else { arrays[j][at - 1] };
            let k = ((round * 13 + j * 7) % 2000 + 1) as i32;
            let r = can_divide_into_subsequences(&arrays[j], k);
            if r {
                yes += 1;
            }
            check = (check * 31 + if r { 1 } else { 2 } + k as i64) % 1000000007;
        }
    }
    println!("250 rounds over 4 arrays of 100000 values: {yes} can be divided, checksum {check}");
}
