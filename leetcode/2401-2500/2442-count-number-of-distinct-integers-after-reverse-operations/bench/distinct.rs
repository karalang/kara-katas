// LeetCode #2442: Count Number of Distinct Integers After Reverse
// Operations -- the bench, the ★ arm: the digits reversed by `% 10` and
// `/ 10`, and a table of flags up to the largest value.

fn reversed(x: i64) -> i64 {
    let mut r = 0;
    let mut y = x;
    while y > 0 {
        r = r * 10 + y % 10;
        y /= 10;
    }
    r
}

fn count_distinct_integers(nums: &[i64]) -> i64 {
    let mut values = nums.to_vec();
    for &x in nums {
        values.push(reversed(x));
    }
    let mut largest = 0;
    for &v in &values {
        largest = largest.max(v);
    }
    let mut seen = vec![false; largest as usize + 1];
    let mut count = 0;
    for &v in &values {
        if !seen[v as usize] {
            seen[v as usize] = true;
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    1 + (a * 32768 + next_random(seed)) % 1000000
}

fn main() {
    let mut seed = 2442i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            nums.push(wide(&mut seed));
        }
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..40i64 {
        for c in 0..arrays.len() {
            let at = ((p * 7919 + c as i64 * 104729) % 100000) as usize;
            arrays[c][at] = wide(&mut seed);
            check = (check * 31 + count_distinct_integers(&arrays[c]) + p) % 1000000007;
        }
    }
    println!("40 passes over 4 arrays of 10^5 values: checksum {}", check);
}
