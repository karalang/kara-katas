// LeetCode #2499: Minimum Total Cost to Make Arrays Unequal -- Rust mirror
// of the benchmark (unequal.kara): the same pairs, passes and checksum.

fn minimum_total_cost(nums1: &[i64], nums2: &[i64]) -> i64 {
    let n = nums1.len();
    let mut count = vec![0i64; n + 1];
    let mut equal = 0;
    let mut cost = 0i64;
    for i in 0..n {
        if nums1[i] == nums2[i] {
            count[nums1[i] as usize] += 1;
            equal += 1;
            cost += i as i64;
        }
    }
    let mut mode = 0usize;
    for v in 1..=n {
        if count[v] > count[mode] {
            mode = v;
        }
    }
    let mode_value = mode as i64;
    let mut short = 2 * count[mode] - equal;
    for j in 0..n {
        if short <= 0 {
            break;
        }
        if nums1[j] != nums2[j] && nums1[j] != mode_value && nums2[j] != mode_value {
            cost += j as i64;
            short -= 1;
        }
    }
    if short > 0 { -1 } else { cost }
}

fn main() {
    let n: i64 = 100000;
    let passes: i64 = 33;
    let mut seed: i64 = 2499;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums1 = Vec::new();
        let mut nums2 = Vec::new();
        for _ in 0..n {
            let a = next_random() % 4 + 1;
            nums1.push(a);
            if next_random() % 2 == 0 {
                nums2.push(a);
            } else {
                nums2.push(next_random() % 4 + 1);
            }
        }
        firsts.push(nums1);
        seconds.push(nums2);
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for q in 0..20 {
            let at = (check % n) as usize;
            let was = seconds[q][at];
            seconds[q][at] = if (check / n + p) % 2 == 0 { firsts[q][at] } else { check % 4 + 1 };
            check = (check * 31 + minimum_total_cost(&firsts[q], &seconds[q]) + 1 + p) % 1000000007;
            seconds[q][at] = was;
        }
    }
    println!("{passes} passes over 20 pairs of 10^5: checksum {check}");
}
