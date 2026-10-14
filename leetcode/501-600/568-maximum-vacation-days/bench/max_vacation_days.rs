// Benchmark for #568: Rust mirror of the ★ arm (dynamic programming over
// the weeks); see max_vacation_days.kara.

fn max_vacation_days(flights: &[Vec<i64>], days: &[Vec<i64>]) -> i64 {
    let n = flights.len();
    let k = days[0].len();
    let mut best = vec![-1i64; n];
    best[0] = 0;
    for w in 0..k {
        let mut next = vec![-1i64; n];
        for j in 0..n {
            for i in 0..n {
                if best[i] >= 0 && (i == j || flights[i][j] == 1) {
                    next[j] = next[j].max(best[i] + days[j][w]);
                }
            }
        }
        best = next;
    }
    *best.iter().max().unwrap()
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 20;
    let rounds: i64 = 30;
    let densities = [1i64, 2, 5, 10, 25, 50, 100];
    let mut seed: i64 = 568;
    let mut cases: Vec<(Vec<Vec<i64>>, Vec<Vec<i64>>)> = Vec::new();
    for g in 0..count {
        let density = densities[(g % 7) as usize];
        let mut flights: Vec<Vec<i64>> = Vec::new();
        for i in 0..100 {
            let mut row = vec![0i64; 100];
            for j in 0..100 {
                if i != j && step(&mut seed) % 100 < density {
                    row[j] = 1;
                }
            }
            flights.push(row);
        }
        let mut days: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            let mut row = vec![0i64; 100];
            for w in 0..100 {
                row[w] = step(&mut seed) % 8;
            }
            days.push(row);
        }
        cases.push((flights, days));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let (flights, days) = &cases[((round * 7 + g) % count) as usize];
            let got = max_vacation_days(flights, days);
            total += got;
            checksum = (checksum * 31 + got + 1) % 1000000007;
        }
    }
    println!(
        "{} cases of 100 cities and 100 weeks, {} rounds: {} days, checksum {}",
        count, rounds, total, checksum
    );
}
