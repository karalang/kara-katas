// LeetCode #1464 bench in Rust: the ★ arm (one pass keeping the two
// largest values) on the same 1000 arrays of 500 values and 100 passes.

fn max_product(nums: &[i32]) -> i32 {
    let mut first = 0;
    let mut second = 0;
    for &x in nums {
        if x > first {
            second = first;
            first = x;
        } else if x > second {
            second = x;
        }
    }
    (first - 1) * (second - 1)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1464i64;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..1000 {
        let nums: Vec<i32> = (0..500).map(|_| (1 + next_random(&mut seed) % 1000) as i32).collect();
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for pass in 0..100 {
        for p in 0..1000 {
            let k = (check % 500) as usize;
            arrays[p][k] = (1 + (check / 7) % 1000) as i32;
            let got = max_product(&arrays[p]);
            check = (check * 31 + got as i64 + pass) % 1000000007;
        }
    }
    println!("100 passes over 1000 arrays of 500 values: checksum {check}");
}
