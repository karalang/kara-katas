// LeetCode 801 — Minimum Swaps To Make Sequences Increasing: the bench,
// in Rust. Mirrors min_swap.kara: two states, left alone and swapped.

fn min_swap(nums1: &[i64], nums2: &[i64]) -> i64 {
    let n = nums1.len();
    let (mut keep, mut swap) = (0i64, 1i64);
    for i in 1..n {
        let same = nums1[i - 1] < nums1[i] && nums2[i - 1] < nums2[i];
        let cross = nums1[i - 1] < nums2[i] && nums2[i - 1] < nums1[i];
        let mut next_keep = n as i64 + 1;
        let mut next_swap = n as i64 + 1;
        if same {
            next_keep = keep;
            next_swap = swap + 1;
        }
        if cross {
            next_keep = next_keep.min(swap);
            next_swap = next_swap.min(keep + 1);
        }
        keep = next_keep;
        swap = next_swap;
    }
    keep.min(swap)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 100000;
    let mut seed = 801;
    let mut pairs: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..16 {
        let (mut a, mut b) = (Vec::new(), Vec::new());
        let (mut x, mut y) = (0i64, 0i64);
        for _ in 0..n {
            x += 1 + next_random(&mut seed) % 2;
            y += 1 + next_random(&mut seed) % 2;
            if next_random(&mut seed) % 2 == 0 {
                a.push(x);
                b.push(y);
            } else {
                a.push(y);
                b.push(x);
            }
        }
        pairs.push((a, b));
    }
    let rounds: i64 = 2000;
    let (mut total, mut check) = (0i64, 0i64);
    for r in 0..rounds {
        let (a, b) = &pairs[(r % 16) as usize];
        let k = min_swap(a, b);
        total += k;
        check = (check * 131 + k) % 1000000007;
    }
    println!("{rounds} rounds of {n} places: {total} swaps in all, checksum {check}");
}
