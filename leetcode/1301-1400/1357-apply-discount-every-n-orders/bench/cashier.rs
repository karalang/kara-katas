// LeetCode #1357 bench -- Rust: the prices in a HashMap from product to
// price, and a count of the customers so far.
use std::collections::HashMap;

struct Cashier {
    n: i32,
    discount: i32,
    served: i32,
    price: HashMap<i32, i32>,
}

impl Cashier {
    fn new(n: i32, discount: i32, products: &[i32], prices: &[i32]) -> Self {
        let mut price = HashMap::new();
        for i in 0..products.len() {
            price.insert(products[i], prices[i]);
        }
        Cashier { n, discount, served: 0, price }
    }

    fn get_bill(&mut self, product: &[i32], amount: &[i32]) -> f64 {
        self.served += 1;
        let mut bill = 0.0;
        for i in 0..product.len() {
            bill += (self.price[&product[i]] * amount[i]) as f64;
        }
        if self.served % self.n == 0 {
            bill * (100 - self.discount) as f64 / 100.0
        } else {
            bill
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn cents(bill: f64) -> i64 {
    (bill * 100.0).round() as i64
}

fn main() {
    // 20 cashiers, each selling the products 1 to 200 at prices from 1 to
    // 1000, with n from 1 to 10 and a discount from 0 to 100, built once;
    // then 10^6 bills, each of 1 to 20 products bought 1 to 1000 times,
    // all drawn from the checksum so far, every bill folded into it in cents
    let mut seed = 1357;
    let mut cashiers: Vec<Cashier> = Vec::new();
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..20 {
        let mut products: Vec<i32> = (1..201).collect();
        for i in 0..200 {
            let j = i + (next_random(&mut seed) % (200 - i as i64)) as usize;
            products.swap(i, j);
        }
        let prices: Vec<i32> = (0..200).map(|_| (1 + next_random(&mut seed) % 1000) as i32).collect();
        let n = (1 + next_random(&mut seed) % 10) as i32;
        let discount = (next_random(&mut seed) % 101) as i32;
        cashiers.push(Cashier::new(n, discount, &products, &prices));
        lists.push(products);
    }
    let mut check: i64 = 0;
    let mut product: Vec<i32> = Vec::new();
    let mut amount: Vec<i32> = Vec::new();
    for r in 0..1000000 {
        let k = (check % 20) as usize;
        let m = 1 + (check / 20) % 20;
        product.clear();
        amount.clear();
        for j in 0..m {
            product.push(lists[k][((check / 7 + j * 37) % 200) as usize]);
            amount.push((1 + (check + j) % 1000) as i32);
        }
        check = (check * 31 + cents(cashiers[k].get_bill(&product, &amount)) + r) % 1000000007;
    }
    println!("1000000 bills over 20 cashiers: checksum {}", check);
}
