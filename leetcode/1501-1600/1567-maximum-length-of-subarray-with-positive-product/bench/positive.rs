// LeetCode #1567: Maximum Length of Subarray With Positive Product --
// bench: the ★ arm over 20 arrays of 200000 values, built once, each
// value 0 one time in 5000 and otherwise of 1 to 1000, negative one time in
// three; 20 passes, each first flipping the sign of one value of every
// array.

fn get_max_len(nums: &[i64]) -> i64 {
    let (mut positive, mut negative, mut best) = (0i64, 0i64, 0i64);
    for &x in nums {
        if x > 0 {
            positive += 1;
            negative = if negative > 0 { negative + 1 } else { 0 };
        } else if x < 0 {
            let was_positive = positive;
            positive = if negative > 0 { negative + 1 } else { 0 };
            negative = was_positive + 1;
        } else {
            positive = 0;
            negative = 0;
        }
        best = best.max(positive);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n: i64 = 200000;
    let mut seed = 1567;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..n {
            let size = next_random(&mut seed) % 1000 + 1;
            let kind = next_random(&mut seed);
            nums.push(if kind % 5000 == 0 { 0 } else if kind % 3 == 0 { -size } else { size });
        }
        arrays.push(nums);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for pass in 0..20i64 {
        for a in 0..arrays.len() {
            let at = ((pass * 7919 + a as i64 * 104729) % n) as usize;
            arrays[a][at] = -arrays[a][at];
            let length = get_max_len(&arrays[a]);
            total += length;
            check = mix(check, length);
        }
    }
    println!("20 passes over 20 arrays of 200000 values: lengths sum {}, checksum {}", total, check);
}
