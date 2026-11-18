// LeetCode #2303: Calculate Amount Paid in Taxes -- the bench, the ★ arm
// in Rust. Walk the brackets in order, taxing the part of the income
// inside each at its percent, summed in hundredths and divided once at
// the end.

fn calculate_tax(brackets: &[(i64, i64)], income: i64) -> f64 {
    let mut hundredths = 0i64;
    let mut below = 0i64;
    for &(upper, percent) in brackets {
        if below >= income {
            break;
        }
        hundredths += (upper.min(income) - below) * percent;
        below = upper;
    }
    hundredths as f64 / 100.0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2303;
    let mut lists: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..20 {
        let mut brackets = Vec::new();
        for i in 0..100i64 {
            let less = if i == 99 { 0 } else { next_random(&mut seed) % 5 };
            brackets.push((10 * (i + 1) - less, next_random(&mut seed) % 101));
        }
        lists.push(brackets);
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        for brackets in &lists {
            for income in 0..=1000i64 {
                let tax = (calculate_tax(brackets, income) * 100.0).round() as i64;
                check = (check * 31 + tax) % 1000000007;
            }
        }
    }
    println!("100 passes over 20 lists of 100 brackets and 1001 incomes: checksum {}", check);
}
