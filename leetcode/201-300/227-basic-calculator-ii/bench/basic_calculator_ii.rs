// ASCII: '+'=43 '-'=45 '*'=42 '/'=47 '0'=48 '9'=57
fn calculate(bytes: &[i64], n: i64) -> i64 {
    let mut stack: Vec<i64> = Vec::new();
    let mut num = 0i64;
    let mut op = 43i64; // '+'
    let mut i = 0i64;
    while i < n {
        let b = bytes[i as usize];
        if b >= 48 && b <= 57 {
            num = num * 10 + (b - 48);
        }
        let is_op = b == 43 || b == 45 || b == 42 || b == 47;
        if is_op || i == n - 1 {
            if op == 43 {
                stack.push(num);
            } else if op == 45 {
                stack.push(-num);
            } else if op == 42 {
                let t = stack.pop().unwrap_or(0);
                stack.push(t * num);
            } else {
                let t = stack.pop().unwrap_or(0);
                stack.push(t / num); // truncates toward zero
            }
            op = b;
            num = 0;
        }
        i += 1;
    }
    let mut total = 0i64;
    for &v in &stack {
        total += v;
    }
    total
}

fn push_number(buf: &mut Vec<i64>, num: i64) {
    if num >= 10 {
        buf.push(48 + num / 10);
        buf.push(48 + num % 10);
    } else {
        buf.push(48 + num);
    }
}

fn main() {
    let tokens: i64 = 200000;
    let passes: i64 = 250;
    let modulus: i64 = 1000000007;

    let mut buf: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;

    state = (state * 1103515245 + 12345) & 2147483647;
    push_number(&mut buf, (state % 99) + 1);

    let mut prev_high = false;
    let mut t = 1i64;
    while t < tokens {
        state = (state * 1103515245 + 12345) & 2147483647;
        let opsel = if prev_high { state % 2 } else { state % 4 };
        if opsel == 0 {
            buf.push(43);
            prev_high = false;
        } else if opsel == 1 {
            buf.push(45);
            prev_high = false;
        } else if opsel == 2 {
            buf.push(42);
            prev_high = true;
        } else {
            buf.push(47);
            prev_high = true;
        }
        state = (state * 1103515245 + 12345) & 2147483647;
        push_number(&mut buf, (state % 99) + 1);
        t += 1;
    }

    let n = buf.len() as i64;
    let mut sink = 0i64;
    for p in 0..passes {
        buf[0] = 49 + (p % 9);
        let r = calculate(&buf, n);
        sink = ((sink + r) % modulus + modulus) % modulus;
    }
    println!("{}", sink);
}
