// LeetCode #2161: Partition Array According to Given Pivot -- the
// benchmark's Rust mirror of pivot.kara.

fn pivot_array(nums: &[i64], pivot: i64) -> Vec<i64> {
    let mut out: Vec<i64> = nums.iter().filter(|&&x| x < pivot).cloned().collect();
    out.extend(nums.iter().filter(|&&x| x == pivot));
    out.extend(nums.iter().filter(|&&x| x > pivot));
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2161i64;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let nums: Vec<i64> = (0..100000).map(|_| wide_random(&mut seed) % 2000001 - 1000000).collect();
        lists.push(nums);
    }
    let mut check = 0i64;
    for round in 0..25i64 {
        for l in 0..4 {
            let at = (wide_random(&mut seed) % 100000) as usize;
            lists[l][at] = wide_random(&mut seed) % 2000001 - 1000000;
            let pivot = lists[l][(wide_random(&mut seed) % 100000) as usize];
            let out = pivot_array(&lists[l], pivot);
            for k in 0..10 {
                check = (check * 31 + out[k * 9999] + 1000001 + round) % 1000000007;
            }
        }
    }
    println!("100 solves: checksum {}", check);
}
