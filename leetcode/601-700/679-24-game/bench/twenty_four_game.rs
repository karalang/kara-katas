// Benchmark for #679: the ★ arm, pairs combined in floating point.

fn reach(values: &[f64]) -> bool {
    let n = values.len();
    if n == 1 {
        return (values[0] - 24.0).abs() < 0.000001;
    }
    for i in 0..n {
        for j in i + 1..n {
            let a = values[i];
            let b = values[j];
            let mut rest: Vec<f64> = Vec::new();
            for k in 0..n {
                if k != i && k != j {
                    rest.push(values[k]);
                }
            }
            let mut results = vec![a + b, a - b, b - a, a * b];
            if b != 0.0 {
                results.push(a / b);
            }
            if a != 0.0 {
                results.push(b / a);
            }
            for r in results {
                let mut next = rest.clone();
                next.push(r);
                if reach(&next) {
                    return true;
                }
            }
        }
    }
    false
}

fn judge_point24(cards: &[i64]) -> bool {
    let values: Vec<f64> = cards.iter().map(|&c| c as f64).collect();
    reach(&values)
}

fn main() {
    let mut solvable: i64 = 0;
    let mut sum: i64 = 0;
    for a in 1..14i64 {
        for b in 1..14i64 {
            for c in 1..14i64 {
                for d in 1..14i64 {
                    let code = a * 1000 + b * 100 + c * 10 + d;
                    if judge_point24(&[a, b, c, d]) {
                        solvable += 1;
                        sum = (sum * 31 + code) % 1000000007;
                    } else {
                        sum = (sum * 31 + 7) % 1000000007;
                    }
                }
            }
        }
    }
    println!("28561 hands: {} solvable, checksum {}", solvable, sum);
}
