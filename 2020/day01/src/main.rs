use std::fs::File;
use std::io::{self, BufRead};
use std::vec::Vec;

fn main() {

    let mut vec: Vec<i32> = Vec::new();

    let file = match File::open("input") {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
    };

    for line in io::BufReader::new(file).lines() {
        if let Ok(v) = line {
            vec.push(v.parse::<i32>().unwrap());
        }
    }

    while let Some(x) = vec.pop() {
        for y in vec.iter() {
            if x + y == 2020 {
                println!("({} * {}) = {}", x, y, x*y);
                break;
            }
        }
    }
}
