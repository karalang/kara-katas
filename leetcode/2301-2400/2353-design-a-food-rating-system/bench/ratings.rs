// LeetCode #2353: Design a Food Rating System -- the bench, the ★ arm: lazy
// heaps, a HashMap from each food to its rating and its cuisine, and for
// each cuisine a min-first BinaryHeap of Reverse((-rating, food)) holding
// every key a food was ever given; a query pops the tops that are no
// longer true.

use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

struct FoodRatings {
    rating: HashMap<String, i64>,
    cuisine_of: HashMap<String, String>,
    heaps: HashMap<String, BinaryHeap<Reverse<(i64, String)>>>,
}

impl FoodRatings {
    fn new(foods: &[String], cuisines: &[String], ratings: &[i64]) -> FoodRatings {
        let mut table = FoodRatings { rating: HashMap::new(), cuisine_of: HashMap::new(), heaps: HashMap::new() };
        for i in 0..foods.len() {
            table.rating.insert(foods[i].clone(), ratings[i]);
            table.cuisine_of.insert(foods[i].clone(), cuisines[i].clone());
            table.heaps.entry(cuisines[i].clone()).or_default().push(Reverse((-ratings[i], foods[i].clone())));
        }
        table
    }

    fn change_rating(&mut self, food: &str, new_rating: i64) {
        *self.rating.get_mut(food).unwrap() = new_rating;
        let cuisine = self.cuisine_of[food].clone();
        self.heaps.get_mut(&cuisine).unwrap().push(Reverse((-new_rating, food.to_string())));
    }

    fn highest_rated(&mut self, cuisine: &str) -> String {
        let heap = self.heaps.get_mut(cuisine).unwrap();
        loop {
            let Reverse((negated, food)) = heap.peek().unwrap();
            if self.rating[food] == -negated {
                return food.clone();
            }
            heap.pop();
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn four_letters(v: i64) -> String {
    [v / 17576, v / 676 % 26, v / 26 % 26, v % 26].iter().map(|&x| (97 + x) as u8 as char).collect()
}

fn main() {
    let mut seed = 2353;
    let n = 10000;
    let foods: Vec<String> = (0..n).map(|i| four_letters(i * 7919 % 456976)).collect();
    let cuisines: Vec<String> = (0..n).map(|_| format!("c{}", next_random(&mut seed) % 100)).collect();
    let ratings: Vec<i64> = (0..n).map(|_| 1 + next_random(&mut seed) % 100000000).collect();
    let mut calls: Vec<(i64, String, i64)> = Vec::new();
    for i in 0..100000 {
        let f = (next_random(&mut seed) % n) as usize;
        if i % 3 == 2 {
            calls.push((1, cuisines[f].clone(), 0));
        } else {
            calls.push((0, foods[f].clone(), 1 + next_random(&mut seed) % 100000000));
        }
    }
    let mut check: i64 = 0;
    for p in 0..100 {
        let mut table = FoodRatings::new(&foods, &cuisines, &ratings);
        for (kind, name, rating) in calls.iter() {
            if *kind == 0 {
                table.change_rating(name, *rating);
            } else {
                for b in table.highest_rated(name).bytes() {
                    check = (check * 31 + b as i64) % 1000000007;
                }
                check = (check * 31 + p) % 1000000007;
            }
        }
    }
    println!("100 passes over 10^4 foods and 10^5 calls: checksum {}", check);
}
