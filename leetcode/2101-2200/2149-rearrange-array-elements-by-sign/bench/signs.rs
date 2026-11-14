// LeetCode #2149: Rearrange Array Elements by Sign -- the benchmark's
// Rust mirror of signs.kara.

fn rearrange_array(nums: &[i64]) -> Vec<i64> {
    let mut out = vec![0i64; nums.len()];
    let mut positive = 0;
    let mut negative = 1;
    for &x in nums {
        if x > 0 {
            out[positive] = x;
            positive += 2;
        } else {
            out[negative] = x;
            negative += 2;
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2149;
    let n: i64 = 200000;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let mut nums: Vec<i64> = Vec::new();
        for i in 0..n {
            let size = next_random(&mut seed) % 100000 + 1;
            nums.push(if i < n / 2 { size } else { -size });
        }
        for i in (1..n).rev() {
            let j = wide(&mut seed) % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        lists.push(nums);
    }
    let mut check = 0;
    for round in 0..25 {
        for l in 0..4 {
            let a = wide(&mut seed) % n;
            let b = wide(&mut seed) % n;
            lists[l].swap(a as usize, b as usize);
            let out = rearrange_array(&lists[l]);
            let at = wide(&mut seed) % n;
            check = (check * 31 + out[0] + out[(n - 1) as usize] + out[at as usize] + 300000 + round) % 1000000007;
        }
    }
    println!("100 answers: checksum {}", check);
}
