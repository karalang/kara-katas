// LeetCode #1569: Number of Ways to Reorder Array to Get Same BST -- bench:
// the ★ arm (the interleavings, by recursion and Pascal's triangle) over 20
// permutations of 1 to 1000, built once; 15 passes, each first swapping two
// values of every permutation.

const MOD: i64 = 1000000007;

fn ways(nums: &[i64], choose: &[Vec<i64>]) -> i64 {
    if nums.len() <= 2 {
        return 1;
    }
    let root = nums[0];
    let left: Vec<i64> = nums.iter().skip(1).filter(|&&x| x < root).cloned().collect();
    let right: Vec<i64> = nums.iter().skip(1).filter(|&&x| x > root).cloned().collect();
    choose[nums.len() - 1][left.len()] * ways(&left, choose) % MOD * ways(&right, choose) % MOD
}

fn num_of_ways(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut choose: Vec<Vec<i64>> = vec![vec![0; n + 1]; n + 1];
    for i in 0..=n {
        choose[i][0] = 1;
        for j in 1..=i {
            choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % MOD;
        }
    }
    (ways(nums, &choose) - 1 + MOD) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n: i64 = 1000;
    let mut seed = 1569;
    let mut perms: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums: Vec<i64> = (1..=n).collect();
        for i in (1..n).rev() {
            let a = next_random(&mut seed);
            let j = (a * 32768 + next_random(&mut seed)) % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        perms.push(nums);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for pass in 0..15i64 {
        for p in 0..perms.len() {
            let i = (pass * 7919 + p as i64 * 104729) % n;
            let j = (pass * 104729 + p as i64 * 7919 + 1) % n;
            perms[p].swap(i as usize, j as usize);
            let w = num_of_ways(&perms[p]);
            total = (total + w) % MOD;
            check = mix(check, w);
        }
    }
    println!("15 passes over 20 permutations of 1000 values: ways sum {}, checksum {}", total, check);
}
