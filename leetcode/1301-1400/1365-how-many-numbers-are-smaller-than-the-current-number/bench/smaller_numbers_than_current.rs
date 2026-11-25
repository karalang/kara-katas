// LeetCode #1365 bench -- Rust: the values counted and the counts summed,
// so below[v] holds how many values are less than v.

fn smaller_numbers_than_current(nums: &[i32]) -> Vec<i32> {
    let mut below = vec![0i32; 102];
    for &x in nums {
        below[x as usize + 1] += 1;
    }
    for v in 1..102 {
        below[v] += below[v - 1];
    }
    nums.iter().map(|&x| below[x as usize]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 arrays of 500 values from 0 to 100, the constraints' most, built
    // once; then 2 * 10^5 rounds, each setting one value of one array, both
    // drawn from the checksum so far, and folding three of the answers
    // into the checksum
    let mut seed = 1365;
    let mut arrays: Vec<Vec<i32>> = (0..20)
        .map(|_| (0..500).map(|_| (next_random(&mut seed) % 101) as i32).collect())
        .collect();
    let mut check: i64 = 0;
    for r in 0..200000 {
        let k = (check % 20) as usize;
        arrays[k][((check / 20) % 500) as usize] = ((check / 10000) % 101) as i32;
        let got = smaller_numbers_than_current(&arrays[k]);
        check = (check * 31
            + got[0] as i64
            + got[(check % 500) as usize] as i64 * 7
            + got[499] as i64 * 13
            + r)
            % 1000000007;
    }
    println!("200000 rounds over 20 arrays of 500 values: checksum {}", check);
}
