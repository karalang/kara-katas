// LeetCode #45 bench mirror — Rust, the greedy range-expansion matcher (★).
//
// Mirrors bench/jump_game_ii.kara exactly: one cursor with farthest/current_end/jumps scalars,
// collapsing the layered BFS into a single scan. Build a reachable array once, punch one slot
// per iteration, fold the jump count into a rolling checksum. Same workload + sink as every
// other mirror.

fn jump(nums: &[i64], n: i64) -> i64 {
    let mut jumps = 0i64;
    let mut current_end = 0i64;
    let mut farthest = 0i64;
    let mut i = 0i64;
    while i < n - 1 {
        if i + nums[i as usize] > farthest {
            farthest = i + nums[i as usize];
        }
        if i == current_end {
            jumps += 1;
            current_end = farthest;
        }
        i += 1;
    }
    jumps
}

fn main() {
    let total: i64 = 200000;
    let modulus: i64 = 1000000007;
    let n: i64 = 1000;

    let mut nums: Vec<i64> = (0..n).map(|a| 1 + (a % 4)).collect();

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        nums[(k % n) as usize] = 1 + (k % 9);
        let ans = jump(&nums, n);
        acc = (acc * 131 + ans) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
