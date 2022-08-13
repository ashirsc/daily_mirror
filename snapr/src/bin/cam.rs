use anyhow::Result; // Automatically handle the error types
use dlib_face_recognition::*;
// use dlib_face_recognition_cv::matrix_to_opencv_mat;
use opencv::{highgui, imgcodecs, prelude::*, types, videoio, imgproc};





// fps logic
        // new_frame_time = time.time()
        // fps = 1/(new_frame_time-prev_frame_time)
        // prev_frame_time = new_frame_time
        // fps = int(fps)
        // fps = str(fps)
        // cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

fn main() -> Result<()> {
    // Note, this is anyhow::Result
    // Open a GUI window
    highgui::named_window("window", highgui::WINDOW_FULLSCREEN)?;
    // Open the web-camera (assuming you have one)
    let mut cam = videoio::VideoCapture::new(0, videoio::CAP_ANY)?;
    let mut frame = Mat::default(); // This array will store the web-cam data
                                    // Read the camera
                                    // and display in the window

    // let cnn_detector = FaceDetectorCnn::default();
    // let landmarks = LandmarkPredictor::default();

    loop {
        cam.read(&mut frame)?;


        
        // let matrix = matrix_to_opencv_mat(&frame);
        // let face_locations = cnn_detector.face_locations(&matrix);

        // for r in face_locations.iter() {
        //     let green = Rgb([0, 255, 0]);
            
        //     imgproc::rectangle(&mut frame, r.to_opencv(), green, 2, imgproc::LINE_8, 0);
    
        //     // let landmarks = landmark_pred.face_landmarks(&matrix, &r);
    
        //     // for point in landmarks.iter() {
        //     //     draw_point(&mut image, &point, green);
        //     // }
        // }

        
        
        
        highgui::imshow("window", &frame)?;
        let key = highgui::wait_key(1)?;
        if key == 113 {
            // quit with q
            break;
        } else if key == 32 {
            //save image with space
            imgcodecs::imwrite(
                "../data/output/image.png",
                &frame,
                &opencv::types::VectorOfi32::new(),
            )?;
        }
    }
    Ok(())
}
