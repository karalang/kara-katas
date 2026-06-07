//! Benchmark workload — two-pointer in-place O(n) Remove Element.
//!
//! Algorithmic mirror of bench/two_pointer.kara and bench/two_pointer.py. See
//! ../README.md § Benchmarks for the choice of N, K and the LCG ~50%-match
//! input.

fn remove_element(nums: &mut [i64], len: i64, val: i64) -> i64 {
    let mut k = 0i64;
    for i in 0..len {
        if nums[i as usize] != val {
            nums[k as usize] = nums[i as usize];
            k += 1;
        }
    }
    k
}

fn main() {
    const N: usize = 2_000_000;
    let val: i64 = 0;

    let mut original: Vec<i64> = vec![0; N];
    let mut state: i64 = 1;
    for i in 0..N {
        state = (state * 1103515245 + 12345) % 2147483648;
        if (state / 65536) % 2 == 1 {
            original[i] = i as i64 + 1;
        } else {
            original[i] = 0;
        }
    }

    let mut workspace: Vec<i64> = vec![0; N];

    let mut sum: i64 = 0;
    for _ in 0..10 {
        for p in 0..N {
            workspace[p] = original[p];
        }
        let k = remove_element(&mut workspace, N as i64, val);
        sum += k + workspace[(k - 1) as usize];
    }
    println!("{}", sum);
}
