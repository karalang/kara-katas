// LeetCode #2179: Count Good Triplets in an Array -- the benchmark's
// Rust mirror of triplets.kara, over slices.

fn good_triplets(nums1: &[i64], nums2: &[i64]) -> i64 {
    let n = nums1.len() as i64;
    let mut place = vec![0i64; n as usize];
    for i in 0..n {
        place[nums2[i as usize] as usize] = i;
    }
    let mut tree = vec![0i64; (n + 1) as usize];
    let mut total = 0i64;
    for i in 0..n {
        let p = place[nums1[i as usize] as usize];
        let mut smaller = 0i64;
        let mut j = p;
        while j > 0 {
            smaller += tree[j as usize];
            j -= j & -j;
        }
        let larger = (n - 1 - p) - (i - smaller);
        total += smaller * larger;
        j = p + 1;
        while j <= n {
            tree[j as usize] += 1;
            j += j & -j;
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn shuffled(n: i64, seed: &mut i64) -> Vec<i64> {
    let mut perm: Vec<i64> = (0..n).collect();
    let mut i = n - 1;
    while i > 0 {
        let a = next_random(seed);
        let b = next_random(seed);
        let j = (a * 32768 + b) % (i + 1);
        perm.swap(i as usize, j as usize);
        i -= 1;
    }
    perm
}

fn main() {
    let n = 100000i64;
    let mut seed = 2179i64;
    let first = shuffled(n, &mut seed);
    let second = shuffled(n, &mut seed);
    let mut check = 0i64;
    for _ in 0..40 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let offset = (a * 32768 + b) % n;
        let rotated: Vec<i64> = (0..n).map(|i| second[((i + offset) % n) as usize]).collect();
        let found = good_triplets(&first, &rotated);
        check = (check * 31 + found % 1000000007) % 1000000007;
    }
    println!("40 solves: checksum {}", check);
}
