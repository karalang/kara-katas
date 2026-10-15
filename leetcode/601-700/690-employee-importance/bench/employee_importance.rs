// LeetCode #690: Employee Importance -- breadth first, by id. Bench.
//
// 30 companies of 2,000 people, ids 1 to 2000 in random order, each
// person under a random earlier one, are built once, with 100 random
// people to ask about in each; then 80 rounds ask about all of them.

use std::collections::VecDeque;

struct Employee {
    id: i64,
    importance: i64,
    subordinates: Vec<i64>,
}

fn get_importance(employees: &[Employee], id: i64) -> i64 {
    let mut at = vec![-1i64; 2001];
    for i in 0..employees.len() {
        at[employees[i].id as usize] = i as i64;
    }
    let mut queue: VecDeque<i64> = VecDeque::new();
    queue.push_back(id);
    let mut sum = 0;
    while let Some(next) = queue.pop_front() {
        let e = &employees[at[next as usize] as usize];
        sum += e.importance;
        for s in e.subordinates.iter() {
            queue.push_back(*s);
        }
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 30;
    let rounds: i64 = 80;
    let size: i64 = 2000;
    let mut seed: i64 = 690;
    let mut companies: Vec<Vec<Employee>> = Vec::new();
    let mut questions: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut ids: Vec<i64> = (1..size + 1).collect();
        for i in 0..size {
            let j = i + next_random(&mut seed) % (size - i);
            ids.swap(i as usize, j as usize);
        }
        let mut subs: Vec<Vec<i64>> = (0..size).map(|_| Vec::new()).collect();
        for i in 1..size {
            let boss = next_random(&mut seed) % i;
            subs[boss as usize].push(ids[i as usize]);
        }
        let mut company: Vec<Employee> = Vec::new();
        for i in 0..size as usize {
            let importance = next_random(&mut seed) % 201 - 100;
            company.push(Employee { id: ids[i], importance, subordinates: subs[i].clone() });
        }
        companies.push(company);
        let ask: Vec<i64> = (0..100).map(|_| 1 + next_random(&mut seed) % size).collect();
        questions.push(ask);
    }
    let mut sum: i64 = 0;
    for r in 0..rounds {
        for c in 0..count as usize {
            for q in 0..100 {
                let got = get_importance(&companies[c], questions[c][q]);
                sum = (sum * 31 + got + 1000000 + r) % 1000000007;
            }
        }
    }
    println!("{} questions answered, checksum {}", count * rounds * 100, sum);
}
