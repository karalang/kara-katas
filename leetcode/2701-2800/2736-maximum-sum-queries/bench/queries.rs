// LeetCode #2736: Maximum Sum Queries -- the bench (queries.kara in Rust):
// pairs and queries by nums1 and x falling, a stack of (nums2, sum) with
// nums2 rising and sums falling, and a binary search per query.

fn maximum_sum_queries(nums1: &[i64], nums2: &[i64], queries: &[Vec<i64>]) -> Vec<i64> {
    let n = nums1.len();
    let mut pairs: Vec<(i64, i64)> = (0..n).map(|i| (nums1[i], nums2[i])).collect();
    pairs.sort_by(|a, b| b.0.cmp(&a.0));
    let mut order: Vec<usize> = (0..queries.len()).collect();
    order.sort_by(|&a, &b| queries[b][0].cmp(&queries[a][0]));
    let mut answer: Vec<i64> = vec![-1; queries.len()];
    let mut stack: Vec<(i64, i64)> = Vec::new();
    let mut j = 0;
    for &q in order.iter() {
        let x = queries[q][0];
        let y = queries[q][1];
        while j < n && pairs[j].0 >= x {
            let (a, b) = pairs[j];
            j += 1;
            if !stack.is_empty() && stack[stack.len() - 1].0 >= b {
                continue;
            }
            while !stack.is_empty() && stack[stack.len() - 1].1 <= a + b {
                stack.pop();
            }
            stack.push((b, a + b));
        }
        let mut low = 0;
        let mut high = stack.len();
        while low < high {
            let middle = (low + high) / 2;
            if stack[middle].0 >= y {
                high = middle;
            } else {
                low = middle + 1;
            }
        }
        if low < stack.len() {
            answer[q] = stack[low].1;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_up_to(seed: &mut i64, most: i64) -> i64 {
    let hi = next_random(seed);
    (hi * 32768 + next_random(seed)) % most + 1
}

fn main() {
    let cases = 10;
    let n = 100000;
    let rounds = 3;
    let mut seed: i64 = 2736;
    let mut problems: Vec<(Vec<i64>, Vec<i64>, Vec<Vec<i64>>)> = Vec::new();
    for _ in 0..cases {
        let nums1: Vec<i64> = (0..n).map(|_| random_up_to(&mut seed, 1000000000)).collect();
        let nums2: Vec<i64> = (0..n).map(|_| random_up_to(&mut seed, 1000000000)).collect();
        let queries: Vec<Vec<i64>> = (0..n)
            .map(|_| {
                let x = random_up_to(&mut seed, 1000000000);
                vec![x, random_up_to(&mut seed, 1000000000)]
            })
            .collect();
        problems.push((nums1, nums2, queries));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums1, nums2, queries) in problems.iter() {
            for &best in maximum_sum_queries(nums1, nums2, queries).iter() {
                sum += best;
                check = (check * 31 + best + 1 + r) % 1000000007;
            }
        }
    }
    println!("{} cases of {} pairs and queries, {} rounds: answers sum to {}, checksum {}", cases, n, rounds, sum, check);
}
