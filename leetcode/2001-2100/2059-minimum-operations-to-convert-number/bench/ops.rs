// LeetCode #2059: Minimum Operations to Convert Number -- Rust mirror of
// the ★ arm's benchmark (ops.kara): the same 16000 problems, each answered
// by one breadth-first search over the values 0 to 1000.
use std::collections::VecDeque;

fn minimum_operations(nums: &[i64], start: i64, goal: i64) -> i64 {
    let mut seen = vec![false; 1001];
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    seen[start as usize] = true;
    queue.push_back((start, 0));
    while let Some((x, steps)) = queue.pop_front() {
        for &n in nums {
            for y in [x + n, x - n, x ^ n] {
                if y == goal {
                    return steps + 1;
                }
                if (0..=1000).contains(&y) && !seen[y as usize] {
                    seen[y as usize] = true;
                    queue.push_back((y, steps + 1));
                }
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(n: i64, spread: i64, seed: &mut i64) -> Vec<i64> {
    let mut nums: Vec<i64> = Vec::new();
    while (nums.len() as i64) < n {
        let x = if next_random(seed) % 8 == 0 {
            let hi = next_random(seed);
            (hi * 32768 + next_random(seed)) % 2000000001 - 1000000000
        } else {
            next_random(seed) % (2 * spread + 1) - spread
        };
        if !nums.contains(&x) {
            nums.push(x);
        }
    }
    nums
}

fn main() {
    let mut seed: i64 = 2059;
    let (mut unreachable, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..16000 {
        let n = next_random(&mut seed) % 16 + 1;
        let spread = [5, 50, 300, 1500][(next_random(&mut seed) % 4) as usize];
        let nums = draw(n, spread, &mut seed);
        let start = next_random(&mut seed) % 1001;
        let mut goal = next_random(&mut seed) % 1401 - 200;
        if goal == start {
            goal += 1;
        }
        let ops = minimum_operations(&nums, start, goal);
        if ops < 0 {
            unreachable += 1;
        }
        total += ops;
        check = (check * 31 + ops + 2) % 1000000007;
    }
    println!("16000 problems: {unreachable} unreachable, sum {total}, checksum {check}");
}
