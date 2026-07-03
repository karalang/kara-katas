// LeetCode #55 bench harness — Rust mirror of jump_game.kara (greedy forward max-reach, ★).
// See ../README.md § Benchmarks. Built with `rustc -O`; the bench.sh also builds a
// `-C overflow-checks=on` variant as the equal-safety comparator to Kāra's checked-by-default
// integer semantics.

fn can_jump_work(nums: &[i64], n: i64) -> i64 {
    let mut farthest: i64 = 0;
    let mut i: i64 = 0;
    while i < n {
        if i > farthest {
            return i;
        }
        if i + nums[i as usize] > farthest {
            farthest = i + nums[i as usize];
        }
        if farthest >= n - 1 {
            return i;
        }
        i += 1;
    }
    i
}

fn main() {
    let total: i64 = 200000;
    let modulus: i64 = 1000000007;
    let n: i64 = 1000;

    let mut nums: Vec<i64> = Vec::new();
    let mut a: i64 = 0;
    while a < n {
        nums.push(1 + (a % 4));
        a += 1;
    }

    let mut acc: i64 = 0;
    let mut k: i64 = 0;
    while k < total {
        nums[(k % n) as usize] = 1 + (k % 9);
        let ans = can_jump_work(&nums, n);
        acc = (acc * 131 + ans) % modulus;
        k += 1;
    }

    println!("{}", acc);
}
