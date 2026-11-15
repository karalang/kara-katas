// benchmark's Rust mirror of pairs.kara (LeetCode #2206, the ★ arm): a
// count per value up to 500, then one pass over the counts.

fn divide_array(nums: &[i64]) -> bool {
    let mut count = vec![0i64; 501];
    for &x in nums {
        count[x as usize] += 1;
    }
    for &c in &count {
        if c % 2 == 1 {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// 1000 numbers up to `top`: 500 pairs shuffled, or 1000 drawn freely
fn random_array(paired: bool, top: i64, seed: &mut i64) -> Vec<i64> {
    let mut nums: Vec<i64> = Vec::new();
    if paired {
        for _ in 0..500 {
            let x = next_random(seed) % top + 1;
            nums.push(x);
            nums.push(x);
        }
        for i in (1..1000usize).rev() {
            let j = (next_random(seed) % (i as i64 + 1)) as usize;
            nums.swap(i, j);
        }
    } else {
        for _ in 0..1000 {
            nums.push(next_random(seed) % top + 1);
        }
    }
    nums
}

fn main() {
    let mut seed = 2206;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..200usize {
        arrays.push(random_array(a % 4 != 3, [2, 5, 500][a % 3], &mut seed));
    }
    // each odd pass punches one number of every array before the count and
    // puts it back after
    let mut check: i64 = 0;
    for p in 0..1500usize {
        for a in 0..200usize {
            let at = (p * 7 + a) % 1000;
            let old = arrays[a][at];
            if p % 2 == 1 {
                arrays[a][at] = ((p + a) % 500 + 1) as i64;
            }
            let paired = divide_array(&arrays[a]);
            arrays[a][at] = old;
            check = (check * 31 + if paired { 2 } else { 1 }) % 1000000007;
        }
    }
    println!("1500 passes over 200 arrays: checksum {}", check);
}
