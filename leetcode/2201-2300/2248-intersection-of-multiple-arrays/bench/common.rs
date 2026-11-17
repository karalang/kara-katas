// LeetCode #2248: Intersection of Multiple Arrays -- the benchmark's Rust
// mirror of common.kara: a count for every value from 1 to 1000, kept
// where it reaches the number of arrays.

fn intersection(nums: &[Vec<i64>]) -> Vec<i64> {
    let mut count = vec![0i64; 1001];
    for row in nums {
        for &v in row {
            count[v as usize] += 1;
        }
    }
    (1..1001i64).filter(|&v| count[v as usize] == nums.len() as i64).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2248i64;
    let mut check = 0i64;
    let mut pool: Vec<i64> = (1..151).collect();
    for _ in 0..20000 {
        let mut nums: Vec<Vec<i64>> = Vec::new();
        for _ in 0..10 {
            for i in 0..100usize {
                let j = i + (next_random(&mut seed) % (150 - i as i64)) as usize;
                pool.swap(i, j);
            }
            nums.push(pool[0..100].to_vec());
        }
        let common = intersection(&nums);
        let folded = common.iter().fold(common.len() as i64, |acc, &v| (acc * 1009 + v) % 1000000007);
        check = (check * 31 + folded) % 1000000007;
    }
    println!("20000 cases: checksum {}", check);
}
