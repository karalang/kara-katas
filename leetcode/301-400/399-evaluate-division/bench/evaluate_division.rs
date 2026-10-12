// Benchmark for #399: mirror of evaluate_division.kara (union-find with weights).
use std::collections::HashMap;

fn find(parent: &mut Vec<usize>, weight: &mut Vec<f64>, i: usize) -> usize {
    let p = parent[i];
    if p == i {
        return i;
    }
    let root = find(parent, weight, p);
    weight[i] = weight[i] * weight[p];
    parent[i] = root;
    root
}

fn intern(index: &mut HashMap<String, usize>, parent: &mut Vec<usize>, weight: &mut Vec<f64>, name: &String) -> usize {
    if let Some(i) = index.get(name) {
        return *i;
    }
    let i = parent.len();
    index.insert(name.clone(), i);
    parent.push(i);
    weight.push(1.0);
    i
}

fn calc_equation(equations: &[(String, String)], values: &[f64], queries: &[(String, String)]) -> Vec<f64> {
    let mut index: HashMap<String, usize> = HashMap::new();
    let mut parent: Vec<usize> = Vec::new();
    let mut weight: Vec<f64> = Vec::new();
    for k in 0..equations.len() {
        let a = intern(&mut index, &mut parent, &mut weight, &equations[k].0);
        let b = intern(&mut index, &mut parent, &mut weight, &equations[k].1);
        let ra = find(&mut parent, &mut weight, a);
        let rb = find(&mut parent, &mut weight, b);
        if ra != rb {
            weight[ra] = values[k] * weight[b] / weight[a];
            parent[ra] = rb;
        }
    }
    let mut answers = Vec::new();
    for (a, b) in queries.iter() {
        let mut answer = -1.0;
        if let Some(&i) = index.get(a) {
            if let Some(&j) = index.get(b) {
                if find(&mut parent, &mut weight, i) == find(&mut parent, &mut weight, j) {
                    answer = weight[i] / weight[j];
                }
            }
        }
        answers.push(answer);
    }
    answers
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn pow2(k: i64) -> f64 {
    let mut x = 1.0;
    for _ in 0..k.abs() {
        x = x * 2.0;
    }
    if k < 0 { 1.0 / x } else { x }
}

fn exponent(x: f64) -> i64 {
    let mut v = x;
    let mut k = 0;
    while v >= 2.0 {
        v = v / 2.0;
        k += 1;
    }
    while v < 1.0 {
        v = v * 2.0;
        k -= 1;
    }
    k
}

fn main() {
    let systems = 100000;
    let mut seed: i64 = 3991;
    let mut answered: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..systems {
        let m = 2 + step(&mut seed) % 39;
        let mut hidden: Vec<i64> = Vec::new();
        for _ in 0..m {
            hidden.push(step(&mut seed) % 9 - 4);
        }
        let mut equations: Vec<(String, String)> = Vec::new();
        let mut values: Vec<f64> = Vec::new();
        for _ in 0..20 {
            let a = step(&mut seed) % m;
            let b = step(&mut seed) % m;
            equations.push((format!("v{}", a), format!("v{}", b)));
            values.push(pow2(hidden[a as usize] - hidden[b as usize]));
        }
        let mut queries: Vec<(String, String)> = Vec::new();
        for _ in 0..20 {
            let a = step(&mut seed) % (m + 2);
            let b = step(&mut seed) % (m + 2);
            queries.push((format!("v{}", a), format!("v{}", b)));
        }
        for x in calc_equation(&equations, &values, &queries) {
            if x < 0.0 {
                checksum = (checksum * 31 + 1) % 1000000007;
            } else {
                answered += 1;
                checksum = (checksum * 31 + exponent(x) + 50) % 1000000007;
            }
        }
    }
    println!("{} systems: {} answered, checksum {}", systems, answered, checksum);
}
