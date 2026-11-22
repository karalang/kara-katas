// LeetCode #2866: Beautiful Towers II -- the bench, as towers.kara: 50
// arrays of 10^5 towers, each answered 10 times by the stack arm.

fn maximum_sum_of_heights(max_heights: &[i64]) -> i64 {
    let n = max_heights.len();
    let mut left = vec![0i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        while !stack.is_empty() && max_heights[stack[stack.len() - 1]] > max_heights[i] {
            stack.pop();
        }
        left[i] = match stack.last() {
            Some(&j) => left[j] + (i - j) as i64 * max_heights[i],
            None => (i + 1) as i64 * max_heights[i],
        };
        stack.push(i);
    }
    stack.clear();
    let mut best = 0;
    let mut right = vec![0i64; n];
    for i in (0..n).rev() {
        while !stack.is_empty() && max_heights[stack[stack.len() - 1]] > max_heights[i] {
            stack.pop();
        }
        right[i] = match stack.last() {
            Some(&j) => right[j] + (j - i) as i64 * max_heights[i],
            None => (n - i) as i64 * max_heights[i],
        };
        stack.push(i);
        best = best.max(left[i] + right[i] - max_heights[i]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (50, 10, 100000);
    let mut seed = 2866;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let top = if c % 2 == 0 { 1000000000 } else { 50 };
        arrays.push((0..n).map(|_| wide(&mut seed) % top + 1).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for heights in arrays.iter() {
            let best = maximum_sum_of_heights(heights);
            total += best;
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: sums total {total}, checksum {check}");
}
