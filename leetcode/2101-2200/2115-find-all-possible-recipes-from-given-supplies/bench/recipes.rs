// LeetCode #2115: Find All Possible Recipes from Given Supplies -- the
// benchmark, the same algorithm as recipes.kara: Kahn's order over names,
// a `HashMap` from each ingredient to the recipes needing it and a
// `VecDeque` starting with the supplies.

use std::collections::{HashMap, VecDeque};

fn find_all_recipes(recipes: &[String], ingredients: &[Vec<String>], supplies: &[String]) -> Vec<String> {
    let mut needed_by: HashMap<String, Vec<usize>> = HashMap::new();
    let mut lacking: Vec<usize> = Vec::new();
    for i in 0..recipes.len() {
        lacking.push(ingredients[i].len());
        for item in &ingredients[i] {
            needed_by.entry(item.clone()).or_default().push(i);
        }
    }
    let mut queue: VecDeque<String> = VecDeque::new();
    for s in supplies {
        queue.push_back(s.clone());
    }
    let mut made: Vec<String> = Vec::new();
    while let Some(item) = queue.pop_front() {
        if let Some(users) = needed_by.get(&item) {
            for &i in users {
                lacking[i] -= 1;
                if lacking[i] == 0 {
                    made.push(recipes[i].clone());
                    queue.push_back(recipes[i].clone());
                }
            }
        }
    }
    made
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2115i64;
    let recipes: Vec<String> = (0..100).map(|i| format!("r{}", i)).collect();
    let supplies: Vec<String> = (0..56).map(|i| format!("s{}", i)).collect();
    let mut kitchens: Vec<Vec<Vec<String>>> = Vec::new();
    for _ in 0..40 {
        let mut ingredients: Vec<Vec<String>> = Vec::new();
        for i in 0..100i64 {
            let mut need: Vec<String> = Vec::new();
            for _ in 0..next_random(&mut seed) % 8 + 1 {
                let pick = next_random(&mut seed) % (60 + i);
                let item = if pick < 60 { format!("s{}", pick) } else { format!("r{}", pick - 60) };
                if !need.contains(&item) {
                    need.push(item);
                }
            }
            if need.is_empty() {
                need.push("s0".to_string());
            }
            ingredients.push(need);
        }
        kitchens.push(ingredients);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10usize {
        for k in 0..40usize {
            let i = (round * 37 + k) % 100;
            kitchens[k][i][0] = format!("s{}", (round + k) % 50);
            let got = find_all_recipes(&recipes, &kitchens[k], &supplies);
            total += got.len() as i64;
            check = (check * 31 + got.len() as i64) % 1000000007;
        }
    }
    println!("400 solves: {} recipes made, checksum {}", total, check);
}
