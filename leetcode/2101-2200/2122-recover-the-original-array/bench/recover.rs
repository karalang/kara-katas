// LeetCode #2122: Recover the Original Array -- the benchmark, the same
// algorithm as recover.kara: each positive even distance from the
// smallest number tried as 2k, smallest first, the sorted numbers paired
// by two pointers.

fn recover_array(nums: &[i64]) -> Vec<i64> {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let m = sorted.len();
    for i in 1..m {
        let gap = sorted[i] - sorted[0];
        if gap == 0 || gap % 2 != 0 || (i > 1 && gap == sorted[i - 1] - sorted[0]) {
            continue;
        }
        let k = gap / 2;
        let mut used = vec![false; m];
        let mut original = Vec::new();
        let mut high = 0;
        for low in 0..m {
            if used[low] {
                continue;
            }
            while high < m && (used[high] || high <= low || sorted[high] < sorted[low] + 2 * k) {
                high += 1;
            }
            if high == m || sorted[high] != sorted[low] + 2 * k {
                break;
            }
            used[high] = true;
            original.push(sorted[low] + k);
        }
        if original.len() * 2 == m {
            return original;
        }
    }
    Vec::new()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2122;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for g in 0..40 {
        let top = [1000, 10000, 100000][g % 3];
        let k = next_random(&mut seed) % 500 + 1;
        let mut nums = Vec::new();
        for _ in 0..1000 {
            let x = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % top + 1 + k;
            nums.push(x - k);
            nums.push(x + k);
        }
        for i in (1..nums.len()).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            nums.swap(i, j);
        }
        arrays.push(nums);
    }
    let mut sizes = 0;
    let mut check: i64 = 0;
    for _ in 0..200 {
        for g in 0..40 {
            for v in arrays[g].iter_mut() {
                *v += 1;
            }
            let original = recover_array(&arrays[g]);
            sizes += original.len();
            for v in original {
                check = (check * 31 + v) % 1000000007;
            }
        }
    }
    println!("8000 solves: {} values recovered, checksum {}", sizes, check);
}
