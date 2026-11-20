// LeetCode #2369: Check if There is a Valid Partition For The Array -- the
// bench, the ★ arm in Rust: good[i] says whether the first i values split
// into valid blocks, from the last block before i and the values before
// it.

fn valid_partition(nums: &[i64]) -> bool {
    let n = nums.len();
    let mut good = vec![false; n + 1];
    good[0] = true;
    for i in 2..n + 1 {
        let a = nums[i - 1];
        let b = nums[i - 2];
        if a == b && good[i - 2] {
            good[i] = true;
        }
        if i >= 3 && good[i - 3] {
            let c = nums[i - 3];
            if (a == b && b == c) || (b == c + 1 && a == b + 1) {
                good[i] = true;
            }
        }
    }
    good[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // array a: about 10^5 values in random blocks of two or three equal
    // values or three rising, the values up to 4^(a + 1); when a is odd, one
    // value near the end then raised by one
    let mut seed = 2369i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut top = 4i64;
    for a in 0..10 {
        let mut nums: Vec<i64> = Vec::new();
        while nums.len() < 100000 {
            let kind = next_random(&mut seed) % 3;
            let hi = next_random(&mut seed);
            let v = 1 + (hi * 32768 + next_random(&mut seed)) % top;
            if kind == 0 {
                nums.extend([v, v]);
            } else if kind == 1 {
                nums.extend([v, v, v]);
            } else {
                nums.extend([v, v + 1, v + 2]);
            }
        }
        if a % 2 == 1 {
            let at = nums.len() - 1 - (next_random(&mut seed) % 100) as usize;
            nums[at] += 1;
        }
        arrays.push(nums);
        top *= 4;
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        for a in 0..10 {
            let valid = if valid_partition(&arrays[a]) { a as i64 + 1 } else { 0 };
            check = (check * 31 + valid + p) % 1000000007;
        }
    }
    println!("20 passes over 10 arrays of about 10^5 values: checksum {}", check);
}
