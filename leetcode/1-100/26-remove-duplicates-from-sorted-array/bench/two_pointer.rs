//! Benchmark workload — two-pointer in-place O(n) Remove Duplicates.
//!
//! Algorithmic mirror of bench/two_pointer.kara and bench/two_pointer.py. See
//! ../README.md § Benchmarks for the choice of N, K and the LCG-random-gap
//! input.

fn remove_duplicates(nums: &mut [i64], len: i64) -> i64 {
    if len == 0 {
        return 0;
    }
    let mut k = 1i64;
    for i in 1..len {
        if nums[i as usize] != nums[(k - 1) as usize] {
            nums[k as usize] = nums[i as usize];
            k += 1;
        }
    }
    k
}

fn main() {
    const N: usize = 2_000_000;

    let mut original: Vec<i64> = vec![0; N];
    let mut state: i64 = 1;
    for i in 1..N {
        state = (state * 1103515245 + 12345) % 2147483648;
        original[i] = original[i - 1] + (state / 65536) % 2;
    }

    let mut workspace: Vec<i64> = vec![0; N];

    let mut sum: i64 = 0;
    for _ in 0..10 {
        for p in 0..N {
            workspace[p] = original[p];
        }
        let k = remove_duplicates(&mut workspace, N as i64);
        sum += k + workspace[(k - 1) as usize];
    }
    println!("{}", sum);
}
