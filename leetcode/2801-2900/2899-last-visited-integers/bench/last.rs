// LeetCode #2899: Last Visited Integers -- the bench's Rust mirror (last.kara).

fn last_visited_integers(nums: &[i64]) -> Vec<i64> {
    let mut seen: Vec<i64> = Vec::new();
    let mut ans: Vec<i64> = Vec::new();
    let mut k = 0usize;
    for &v in nums {
        if v == -1 {
            k += 1;
            ans.push(if k <= seen.len() {
                seen[seen.len() - k]
            } else {
                -1
            });
        } else {
            seen.push(v);
            k = 0;
        }
    }
    ans
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (count, rounds, n) = (10000, 20i64, 100);
    let mut seed = 2899i64;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums = Vec::new();
        for _ in 0..n {
            if next_random(&mut seed) % 3 == 0 {
                nums.push(-1);
            } else {
                nums.push(next_random(&mut seed) % 100 + 1);
            }
        }
        cases.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &cases {
            let ans = last_visited_integers(nums);
            check = (check * 31 + ans.len() as i64 + r) % 1000000007;
            for &v in &ans {
                total += v;
                check = (check * 31 + v + 2) % 1000000007;
            }
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: answers total {total}, checksum {check}");
}
