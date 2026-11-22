// LeetCode #2709: Greatest Common Divisor Traversal -- the bench
// (traversal.kara in Rust): a smallest-prime-factor sieve, and each index
// joined in a union-find to the first index seen with each of its
// primes.

fn find(parent: &mut Vec<i64>, a: i64) -> i64 {
    let mut a = a;
    while parent[a as usize] != a {
        parent[a as usize] = parent[parent[a as usize] as usize];
        a = parent[a as usize];
    }
    a
}

fn can_traverse_all_pairs(nums: &[i64]) -> bool {
    let n = nums.len() as i64;
    if n == 1 {
        return true;
    }
    let top = *nums.iter().max().unwrap();
    let mut spf: Vec<i64> = (0..top + 1).collect();
    let mut p: i64 = 2;
    while p * p <= top {
        if spf[p as usize] == p {
            let mut m = p * p;
            while m <= top {
                if spf[m as usize] == m {
                    spf[m as usize] = p;
                }
                m += p;
            }
        }
        p += 1;
    }
    let mut parent: Vec<i64> = (0..n).collect();
    let mut first: Vec<i64> = vec![-1; (top + 1) as usize];
    let mut sets = n;
    for (i, &v) in nums.iter().enumerate() {
        if v == 1 {
            return false;
        }
        let mut rest = v;
        while rest > 1 {
            let q = spf[rest as usize];
            while rest % q == 0 {
                rest /= q;
            }
            if first[q as usize] < 0 {
                first[q as usize] = i as i64;
            } else {
                let a = find(&mut parent, i as i64);
                let b = find(&mut parent, first[q as usize]);
                if a != b {
                    parent[a as usize] = b;
                    sets -= 1;
                }
            }
        }
    }
    sets == 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let arrays = 20;
    let n = 100000;
    let rounds = 5;
    let mut seed: i64 = 2709;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for a in 0..arrays {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            if a % 2 == 0 {
                let p = [2, 3, 5, 7][(next_random(&mut seed) % 4) as usize];
                nums.push(p * (wide(&mut seed) % 14285 + 1));
            } else {
                nums.push(wide(&mut seed) % 99999 + 2);
            }
        }
        all.push(nums);
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in all.iter() {
            let can = can_traverse_all_pairs(nums);
            if can {
                yes += 1;
            }
            check = (check * 31 + if can { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{} arrays of {} numbers up to 100000, {} rounds: {} traversable, checksum {}", arrays, n, rounds, yes, check);
}
