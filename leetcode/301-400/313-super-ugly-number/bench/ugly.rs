// LeetCode 313 - Super Ugly Number.
//
// Mirror of ugly.kara: the same k-way merge with one pointer per prime and a
// two-pass step (find the minimum, then advance every stream that offered it).
// Same build-once + punch shape, same per-pass prime swap, same masked sink.
// Kept algorithm-for-algorithm so the benchmark lane is honest.

const TERMS: usize = 100000;
const PASSES: i64 = 30;
const MASK: i64 = 1073741823;

fn main() {
    let mut primes: Vec<i64> = vec![
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
        59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    ];
    let k = primes.len();
    let pool: Vec<i64> = vec![179, 181, 191, 193, 197, 199, 211, 223];

    let mut ugly: Vec<i64> = vec![0; TERMS];
    let mut idx: Vec<usize> = vec![0; k];

    let mut checksum: i64 = 0;
    for _pass in 0..PASSES {
        let slot = (checksum as usize) % k;
        let keep = primes[slot];
        primes[slot] = pool[(checksum as usize) % pool.len()];

        for i in 0..k {
            idx[i] = 0;
        }
        ugly[0] = 1;
        for m in 1..TERMS {
            let mut best = primes[0] * ugly[idx[0]];
            for i in 1..k {
                let c = primes[i] * ugly[idx[i]];
                if c < best {
                    best = c;
                }
            }
            for i in 0..k {
                if primes[i] * ugly[idx[i]] == best {
                    idx[i] += 1;
                }
            }
            ugly[m] = best;
        }

        checksum = (checksum + ugly[TERMS - 1]) & MASK;
        primes[slot] = keep;
    }

    println!("checksum {}", checksum);
}
