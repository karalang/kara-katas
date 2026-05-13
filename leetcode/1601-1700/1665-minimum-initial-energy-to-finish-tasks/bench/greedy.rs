//! Benchmark workload — greedy O(n log n) Minimum Initial Energy to Finish Tasks.
//!
//! Algorithmic mirror of bench/greedy.kara and bench/greedy.py. See
//! ../README.md § Benchmarks for the choice of N / K and the
//! deterministic generator.

fn minimum_effort(tasks: &[(i64, i64)]) -> i64 {
    let mut ordered: Vec<(i64, i64)> = tasks.to_vec();
    ordered.sort_by(|a, b| (b.1 - b.0).cmp(&(a.1 - a.0)));
    let mut energy: i64 = 0;
    let mut spent: i64 = 0;
    for &(actual, minimum) in &ordered {
        let need = spent + minimum;
        if need > energy {
            energy = need;
        }
        spent += actual;
    }
    energy
}

fn main() {
    const N: i64 = 50_000;
    let data: Vec<(i64, i64)> = (0..N)
        .map(|i| {
            let actual = (i * 7) % 100 + 1;
            let minimum = actual + (i * 13) % 50;
            (actual, minimum)
        })
        .collect();

    let mut sum: i64 = 0;
    for _ in 0..5 {
        sum += minimum_effort(&data);
    }
    println!("{}", sum);
}
