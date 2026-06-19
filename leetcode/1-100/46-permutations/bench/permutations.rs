// LeetCode #46 bench mirror — Rust, the used-array mutable-path backtracker (★).
//
// Mirrors bench/permutations.kara exactly: a DFS that picks any still-unused element (tracked
// by a `used` bool array) alongside a mutable path, snapshotting the path into a Vec<Vec<i64>>
// at each leaf. Workload: TOTAL permutations of a fixed n=7 array with one slot punched per
// iteration (`nums[k%n] = 1 + k%9`), folding a position-weighted per-perm signature plus the
// count into a rolling checksum. Prints the same sink as every other mirror.

fn backtrack(
    nums: &[i64],
    used: &mut [bool],
    path: &mut Vec<i64>,
    out: &mut Vec<Vec<i64>>,
) {
    let n = nums.len();
    if path.len() == n {
        out.push(path.clone());
        return;
    }
    for i in 0..n {
        if !used[i] {
            used[i] = true;
            path.push(nums[i]);
            backtrack(nums, used, path, out);
            path.pop();
            used[i] = false;
        }
    }
}

fn permute(nums: &[i64]) -> Vec<Vec<i64>> {
    let n = nums.len();
    let mut used = vec![false; n];
    let mut path: Vec<i64> = Vec::new();
    let mut out: Vec<Vec<i64>> = Vec::new();
    backtrack(nums, &mut used, &mut path, &mut out);
    out
}

fn main() {
    let total: i64 = 300;
    let modulus: i64 = 1000000007;
    let n: i64 = 7;
    let mut nums: Vec<i64> = (0..n).map(|b| b + 1).collect();

    let mut acc: i64 = 0;
    for k in 0..total {
        nums[(k % n) as usize] = 1 + (k % 9);
        let perms = permute(&nums);

        let mut sig: i64 = 0;
        for perm in &perms {
            let mut s: i64 = 0;
            let mut i: i64 = 0;
            let pl = perm.len() as i64;
            while i < pl {
                s += perm[i as usize] * (i + 1);
                i += 1;
            }
            sig = (sig * 31 + s) % modulus;
        }
        sig = (sig + perms.len() as i64) % modulus;
        acc = (acc * 131 + sig) % modulus;
    }

    println!("{}", acc);
}
