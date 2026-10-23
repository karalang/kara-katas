// LeetCode #930: Binary Subarrays With Sum -- bench: prefix sums counted
// in an array. Mirrors num_subarrays_with_sum.kara.

fn num_subarrays_with_sum(nums: &[i64], goal: i64) -> i64 {
    let n = nums.len();
    let mut seen = vec![0i64; n + 1];
    seen[0] = 1;
    let mut sum: i64 = 0;
    let mut count: i64 = 0;
    for &v in nums {
        sum += v;
        if sum >= goal {
            count += seen[(sum - goal) as usize];
        }
        seen[sum as usize] += 1;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (100, 100, 30000);
    let mut seed = 930;
    // count arrays of n elements, built once, each leaning from 0 to 1 by
    // a random amount, with a goal from 0 to the number of 1s
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut goals: Vec<i64> = Vec::new();
    for _ in 0..count {
        let lean = 1 + next_random(&mut seed) % 99;
        let mut nums: Vec<i64> = Vec::new();
        let mut ones = 0;
        for _ in 0..n {
            let v = if next_random(&mut seed) % 100 < lean {
                1
            } else {
                0
            };
            ones += v;
            nums.push(v);
        }
        goals.push(next_random(&mut seed) % (ones + 1));
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every array, starting from a different one
        for i in 0..count {
            let p = (r + i) % count;
            let a = num_subarrays_with_sum(&arrays[p], goals[p]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds over {count} arrays of {n}: answers summing to {total}, checksum {check}"
    );
}
