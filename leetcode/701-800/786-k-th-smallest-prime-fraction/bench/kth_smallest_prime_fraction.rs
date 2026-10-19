// LeetCode 786 — K-th Smallest Prime Fraction: the bench, in Rust.
// Mirrors kth_smallest_prime_fraction.kara: a heap of the next fraction
// for each denominator, over the same 64 arrays.
use std::cmp::{Ordering, Reverse};
use std::collections::BinaryHeap;

struct Fraction {
    i: usize,
    j: usize,
    num: i64,
    den: i64,
}

impl PartialEq for Fraction {
    fn eq(&self, other: &Self) -> bool {
        self.num * other.den == other.num * self.den
    }
}

impl Eq for Fraction {}

impl PartialOrd for Fraction {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Fraction {
    fn cmp(&self, other: &Self) -> Ordering {
        (self.num * other.den).cmp(&(other.num * self.den))
    }
}

fn kth_smallest_prime_fraction(arr: &[i64], k: i64) -> Vec<i64> {
    let n = arr.len();
    let mut heap = BinaryHeap::new();
    for j in 1..n {
        heap.push(Reverse(Fraction { i: 0, j, num: arr[0], den: arr[j] }));
    }
    for _ in 0..k - 1 {
        let Some(Reverse(f)) = heap.pop() else {
            break;
        };
        if f.i + 1 < f.j {
            heap.push(Reverse(Fraction { i: f.i + 1, j: f.j, num: arr[f.i + 1], den: f.den }));
        }
    }
    let Reverse(f) = heap.pop().unwrap();
    vec![f.num, f.den]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut composite = vec![false; 30000];
    let mut primes: Vec<i64> = Vec::new();
    for p in 2..30000usize {
        if !composite[p] {
            primes.push(p as i64);
            let mut m = p * p;
            while m < 30000 {
                composite[m] = true;
                m += p;
            }
        }
    }
    let mut seed = 786;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..64 {
        let mut taken = vec![false; primes.len()];
        let mut count = 0;
        while count < 999 {
            let at = (next_random(&mut seed) % primes.len() as i64) as usize;
            if !taken[at] {
                taken[at] = true;
                count += 1;
            }
        }
        let mut arr = vec![1];
        for at in 0..primes.len() {
            if taken[at] {
                arr.push(primes[at]);
            }
        }
        arrays.push(arr);
    }
    let rounds = 64;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let k = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 499500;
        let answer = kth_smallest_prime_fraction(&arrays[r % 64], k);
        sum += answer[0] + answer[1];
        check = (check * 31 + answer[0] * 7 + answer[1]) % 1000000007;
    }
    println!("{rounds} rounds of 1000-number arrays: terms sum to {sum}, checksum {check}");
}
