// Benchmark: LeetCode #1005 Maximize Sum Of Array After K Negations -- the
// ★ arm, counting, on arrays of 10000 numbers, LeetCode's longest.
// Mirrors largest_sum.kara, .c, .py and go-seq/.

fn largest_sum_after_k_negations(nums: &[i64], k: i64) -> i64 {
    let mut count = vec![0i64; 201];
    for &x in nums {
        count[(x + 100) as usize] += 1;
    }
    let mut left = k;
    let mut v: i64 = -100;
    while v < 0 && left > 0 {
        let flip = count[(v + 100) as usize].min(left);
        count[(v + 100) as usize] -= flip;
        count[(100 - v) as usize] += flip;
        left -= flip;
        v += 1;
    }
    let mut sum = 0;
    for v in -100..101i64 {
        sum += v * count[(v + 100) as usize];
    }
    if left % 2 == 1 {
        let mut smallest: i64 = 0;
        while count[(smallest + 100) as usize] == 0 {
            smallest += 1;
        }
        sum -= 2 * smallest;
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 2500;
    let n: i64 = 10000;
    let mut seed: i64 = 1005;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for t in 0..20i64 {
        let mut nums = Vec::new();
        for _ in 0..n {
            let size = next_random(&mut seed) % 101;
            nums.push(if next_random(&mut seed) % 8 < t % 7 + 1 { -size } else { size });
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20i64 {
            let t = (r + i) % 20;
            let k = 1 + (r * 37 + t * 101) % 10000;
            let got = largest_sum_after_k_negations(&arrays[t as usize], k);
            total += got;
            check = (check * 31 + got % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 arrays of {n} numbers: answers sum to {total}, checksum {check}");
}
