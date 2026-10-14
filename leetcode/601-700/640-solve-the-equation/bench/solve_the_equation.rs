// Benchmark for #640: mirror of solve_the_equation.kara (the ★ arm: each
// side read once into a count of x and a constant) on the same workload.

const ROUNDS: usize = 200000;

fn side(text: &[u8]) -> (i64, i64) {
    let mut xs = 0;
    let mut constant = 0;
    let mut i = 0;
    let n = text.len();
    while i < n {
        let mut sign = 1;
        if text[i] == b'+' || text[i] == b'-' {
            if text[i] == b'-' {
                sign = -1;
            }
            i += 1;
        }
        let mut value = 0;
        let mut digits = 0;
        while i < n && text[i].is_ascii_digit() {
            value = value * 10 + (text[i] - b'0') as i64;
            digits += 1;
            i += 1;
        }
        if i < n && text[i] == b'x' {
            xs += sign * if digits == 0 { 1 } else { value };
            i += 1;
        } else {
            constant += sign * value;
        }
    }
    (xs, constant)
}

fn solve_equation(equation: &str) -> String {
    let bytes = equation.as_bytes();
    let mut eq = 0;
    while bytes[eq] != b'=' {
        eq += 1;
    }
    let (a, b) = side(&bytes[0..eq]);
    let (c, d) = side(&bytes[eq + 1..]);
    if a == c {
        if b == d {
            String::from("Infinite solutions")
        } else {
            String::from("No solution")
        }
    } else {
        format!("x={}", (d - b) / (a - c))
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_side(terms: usize, seed: &mut i64) -> (String, i64, i64) {
    let mut text = String::new();
    let mut xs = 0;
    let mut constant = 0;
    for t in 0..terms {
        let minus = next_random(seed) % 2 == 0;
        if minus {
            text.push('-');
        } else if t > 0 {
            text.push('+');
        }
        let sign = if minus { -1 } else { 1 };
        let value = next_random(seed) % 100;
        if next_random(seed) % 2 == 0 {
            text.push_str(&format!("{}x", value));
            xs += sign * value;
        } else {
            text.push_str(&format!("{}", value));
            constant += sign * value;
        }
    }
    (text, xs, constant)
}

fn main() {
    let mut seed: i64 = 640;
    let mut equations: Vec<String> = Vec::new();
    for _ in 0..20 {
        let (left, a, b) = random_side(125, &mut seed);
        let (right, c, d) = random_side(125, &mut seed);
        let mut text = format!("{}={}", left, right);
        if a != c {
            let rem = (d - b) % (a - c);
            if rem > 0 {
                text = format!("{}-{}", text, rem);
            } else if rem < 0 {
                text = format!("{}+{}", text, -rem);
            }
        }
        equations.push(text);
    }
    let mut solved = 0;
    let mut sum = 0i64;
    for round in 0..ROUNDS {
        let answer = solve_equation(&equations[round % 20]);
        if answer.starts_with("x=") {
            solved += 1;
            sum += answer[2..].parse::<i64>().unwrap();
        }
    }
    println!("20 equations, {} rounds: {} solved, x adding to {}", ROUNDS, solved, sum);
}
