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
    let mut save_vec = vec.clone();

    while let Some(x) = vec.pop() {
        for y in vec.iter() {
            if x + y == 2020 {
                println!("({} * {}) = {}", x, y, x*y);
                break;
            }
        }
    }

    while let Some(x) = save_vec.pop() {
        let mut vec_copy = save_vec.clone();
        while let Some(y) = vec_copy.pop() {
            for z in vec_copy.iter() {
                if x + y + z == 2020 {
                    println!("({} * {} * {}) = {}", x, y, z, x*y*z);
                    break;
                }
            }
        }
    }
}
