#[macro_use] extern crate rocket;
use std::fs;
use std::borrow::Cow;


fn basename<'a>(path: &'a str, sep: char) -> Cow<'a, str> {
    let pieces = path.rsplit(sep);
    match pieces.next() {
        Some(p) => p.into(),
        None => path.into(),
    }
}

#[get("/<name>/<age>")]
fn hello(name: &str, age: u8) -> String {
    format!("Hello, {} year old named {}!", age, name)
}

#[get("/")]
fn root() -> String {

    let paths = fs::read_dir("/home/drew/Documents/daily_mirror/data/captures").unwrap();

    for path in paths {
        let pathBasename = basename(path.unwrap().path(), '/');
        println!("Name: {}", pathBasename)
    }

    "Hello world!".to_string()
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![hello, root])
   
}

