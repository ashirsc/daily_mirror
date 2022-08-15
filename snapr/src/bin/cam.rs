use anyhow::Result; // Automatically handle the error types
                    // use dlib_face_recognition::*;
                    // use dlib_face_recognition_cv::matrix_to_opencv_mat;
use opencv::{
    core::{self, Point, Rect, Scalar, Size, ToInputOutputArray, ToOutputArray, Vector},
    highgui, imgcodecs, imgproc,
    objdetect,
    prelude::*,
    types, videoio,
};

use std::time::SystemTime;

fn draw_fps<'a>(frame: &mut Mat, prev_time: &SystemTime) -> SystemTime {
    let new_frame_time = SystemTime::now();

    let fps = 1.0
        / (new_frame_time
            .duration_since(*prev_time)
            .unwrap()
            .as_secs_f32());

    let _ = imgproc::put_text(
        &mut frame.input_output_array().unwrap(),
        fps.to_string().as_str(),
        Point::new(7, 70),
        0,
        2.0,
        Scalar::new(100.0, 255.0, 0.0, 0.0),
        3,
        imgproc::LINE_AA,
        false,
    );

    new_frame_time
}

fn main() -> Result<()> {
    // Note, this is anyhow::Result
    // Open a GUI window
    highgui::named_window("window", highgui::WINDOW_FULLSCREEN)?;
    // Open the web-camera (assuming you have one)
    let mut cam = videoio::VideoCapture::new(0, videoio::CAP_ANY)?;
    let mut frame = Mat::default();

    let mut prev_frame_time = SystemTime::now();

    let mut face_cascade = objdetect::CascadeClassifier::new("haarcascade_frontalface_alt.xml").unwrap();

    loop {
        cam.read(&mut frame)?;
        if frame.empty() {
            continue;
        }

        let mut gray = Mat::default();
        imgproc::cvt_color(
            &frame,
            &mut gray.output_array().unwrap(),
            imgproc::COLOR_BGR2GRAY,
            0,
        )
        .unwrap();
        let mut faces = Vector::<Rect>::new();
        let _ = face_cascade.detect_multi_scale(
            &gray,
            &mut faces,
            2.0,
            4,
            0,
            Size::new(240, 240),
            Size::new(3680, 3680),
        )?;
        for face in faces.iter() {
            let _ = imgproc::rectangle(
                &mut frame.input_output_array().unwrap(),
                face,
                Scalar::new(0.0, 255.0, 0.0, 0.0),
                3,
                imgproc::LINE_AA,
                0,
            );
        }

        prev_frame_time = draw_fps(&mut frame, &prev_frame_time);

        highgui::imshow("window", &gray)?;
        let key = highgui::wait_key(1)?;
        if key == 32 {
            //save image with space
            imgcodecs::imwrite(
                "../data/output/image.png",
                &frame,
                &opencv::types::VectorOfi32::new(),
            )?;
        } else if key == 27 {
            break;
        }
    }
    Ok(())
}
