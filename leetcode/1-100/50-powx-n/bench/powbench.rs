// Bench mirror of powbench.kara — recursive fast-power, f64-bits sum sink.
// rustc -O. See ../README.md § Benchmarks.

fn fast_pow(x: f64, n: i64) -> f64 {
    if n == 0 {
        return 1.0;
    }
    let half = fast_pow(x, n / 2);
    if n % 2 == 0 {
        half * half
    } else {
        half * half * x
    }
}

fn my_pow(x: f64, n: i64) -> f64 {
    if n < 0 {
        1.0 / fast_pow(x, -n)
    } else {
        fast_pow(x, n)
    }
}

fn main() {
    let n_iters: i64 = 400_000;
    let k_reps: i64 = 20;
    let inv2048 = 0.00048828125_f64; // 2^-11, exact
    let mut acc: u64 = 0;
    for rep in 0..k_reps {
        for i in 0..n_iters {
            let h = ((i + rep * 7919) * 2654435761) & 2047;
            let x = 1.0 + (h as f64) * inv2048;
            let n = ((i + rep) % 129) - 64;
            acc = acc.wrapping_add(my_pow(x, n).to_bits());
        }
    }
    println!("{}", acc & 0x7FFF_FFFF_FFFF_FFFF);
}
