// LeetCode #2190: Most Frequent Number Following Key In an Array -- the
// benchmark's Rust mirror of follow.kara, over a slice of the row:
// counts in a list, the leader kept as met.

fn most_frequent(nums: &[i64], key: i64) -> i64 {
    let mut counts = vec![0i64; 1001];
    let mut best = 0;
    let mut target = -1;
    for i in 1..nums.len() {
        if nums[i - 1] == key {
            let x = nums[i] as usize;
            counts[x] += 1;
            if counts[x] > best {
                best = counts[x];
                target = x as i64;
            }
        }
    }
    target
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    a * 32768 + b
}

fn main() {
    let mut seed = 2190;
    let row: Vec<i64> = (0..1000000).map(|_| next_random(&mut seed) % 100 + 1).collect();
    let mut check: i64 = 0;
    for _ in 0..200000 {
        let start = (big_random(&mut seed) % 999001) as usize;
        let key = row[start];
        check = (check * 31 + most_frequent(&row[start..start + 1000], key)) % 1000000007;
    }
    println!("200000 solves: checksum {}", check);
}
