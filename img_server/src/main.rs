#[macro_use]
extern crate rocket;
use rocket::fs::FileServer;
use serde::{Deserialize, Serialize};
use std::fs::{self};
use rocket::http::Header;
use rocket::{Request, Response};
use rocket::fairing::{Fairing, Info, Kind};

#[derive(Serialize, Deserialize)]
struct GetAllResponse {
    files: Vec<String>,
}

static CAPTURES_DIR:&'static str = "/home/drew/Documents/daily_mirror/data/captures";
// let captures_dir = "C:\\Users\\andre\\workspace\\daily_mirror\\data\\captures"

pub struct CORS;

#[rocket::async_trait]
impl Fairing for CORS {
    fn info(&self) -> Info {
        Info {
            name: "Add CORS headers to responses",
            kind: Kind::Response
        }
    }

    async fn on_response<'r>(&self, _request: &'r Request<'_>, response: &mut Response<'r>) {
        response.set_header(Header::new("Access-Control-Allow-Origin", "*"));
        response.set_header(Header::new("Access-Control-Allow-Methods", "POST, GET, PATCH, OPTIONS"));
        response.set_header(Header::new("Access-Control-Allow-Headers", "*"));
        response.set_header(Header::new("Access-Control-Allow-Credentials", "true"));
    }
}


#[get("/all")]
fn root() -> String {
//    
    let paths = fs::read_dir(CAPTURES_DIR)
        .unwrap()
        .map(|res| res.unwrap().path().file_name().unwrap().to_str().unwrap().to_string())
        .collect();

    let res = GetAllResponse { files: paths };
    serde_json::to_string(&res).unwrap()
}

#[launch]
fn rocket() -> _ {
    rocket::build()
    .attach(CORS)
    .mount("/", FileServer::from("dist").rank(2))
    .mount("/api/images", FileServer::from(CAPTURES_DIR).rank(1))
    .mount("/api", routes![root])

}
