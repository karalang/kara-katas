// LeetCode #1714: Sum Of Special Evenly-Spaced Elements In Array -- the
// Rust mirror of the bench (special.kara): the queries taken in order of
// their step, a small step's sums built from the back and a large step's
// walked, on 5 random problems of 50000 values and 150000 queries, each
// answered 4 times.

fn solve(nums: &[i32], queries: &[Vec<i32>]) -> Vec<i32> {
    let modulus: i64 = 1000000007;
    let n = nums.len();
    let small = n.isqrt();
    let mut answer: Vec<i32> = vec![0; queries.len()];
    let mut order: Vec<usize> = (0..queries.len()).collect();
    order.sort_by_key(|&q| queries[q][1]);
    let mut sums: Vec<i64> = vec![0; n];
    let mut built = 0;
    for &q in order.iter() {
        let (x, y) = (queries[q][0] as usize, queries[q][1] as usize);
        if y <= small {
            if y != built {
                for j in (0..n).rev() {
                    let after = if j + y < n { sums[j + y] } else { 0 };
                    sums[j] = (nums[j] as i64 + after) % modulus;
                }
                built = y;
            }
            answer[q] = sums[x] as i32;
        } else {
            let mut total: i64 = 0;
            let mut j = x;
            while j < n {
                total += nums[j] as i64;
                j += y;
            }
            answer[q] = (total % modulus) as i32;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 5;
    let rounds: i64 = 4;
    let n: i64 = 50000;
    let q = 150000;
    let mut seed: i64 = 1714;
    let mut problems: Vec<(Vec<i32>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i32> = (0..n).map(|_| (wide(&mut seed) % 1000000000) as i32).collect();
        let mut queries: Vec<Vec<i32>> = Vec::new();
        for _ in 0..q {
            let x = wide(&mut seed) % n;
            let y = if next_random(&mut seed) % 2 == 0 {
                next_random(&mut seed) % 223 + 1
            } else {
                wide(&mut seed) % n + 1
            };
            queries.push(vec![x as i32, y as i32]);
        }
        problems.push((nums, queries));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, queries) in problems.iter() {
            for &a in solve(nums, queries).iter() {
                sum += a as i64;
                check = (check * 31 + a as i64 + r) % 1000000007;
            }
        }
    }
    println!("{count} problems of {n} values and {q} queries, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
