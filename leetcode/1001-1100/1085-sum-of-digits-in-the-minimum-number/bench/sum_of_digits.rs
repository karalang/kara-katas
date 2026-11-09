// Benchmark: LeetCode #1085 Sum of Digits in the Minimum Number -- the ★
// arm. Mirrors sum_of_digits.kara, .c, .py and go-seq/.

fn sum_of_digits(nums: &[i64]) -> i64 {
    let mut least = nums[0];
    for &v in nums.iter() {
        if v < least {
            least = v;
        }
    }
    let mut sum = 0;
    while least > 0 {
        sum += least % 10;
        least /= 10;
    }
    if sum % 2 == 0 { 1 } else { 0 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 5000;
    let mut seed = 1085;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let low = next_random(&mut seed) % 100 + 1;
        let nums: Vec<i64> = (0..100).map(|_| low + next_random(&mut seed) % (101 - low)).collect();
        arrays.push(nums);
    }
    let mut ones: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..2000i64 {
            let a = sum_of_digits(&arrays[((r * 7 + i) % 2000) as usize]);
            ones += a;
            check = (check * 31 + a + i) % 1000000007;
        }
    }
    println!("{rounds} rounds over 2000 arrays of 100 values: {ones} answer 1, checksum {check}");
}
