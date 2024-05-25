import cv2
import numpy as np
import logging
import dlib
import os
import uuid
from imutils import face_utils

# Configure logging
logging.basicConfig(level=logging.INFO)


def load_detection_model(model_file, config_file):
    """Load pre-trained face detection model."""
    logging.info(f"Loading face detection model from "
                 f"{model_file} and {config_file}...")
    if not os.path.isfile(model_file):
        logging.error(f"Model file not found: {model_file}")
        return None
    if not os.path.isfile(config_file):
        logging.error(f"Config file not found: {config_file}")
        return None
    net = cv2.dnn.readNetFromCaffe(config_file, model_file)
    return net


def preprocess_image(image):
    """Preprocess the input image for face detection."""
    logging.info("Preprocessing image for face detection...")
    blob = cv2.dnn.blobFromImage(cv2.resize(
        image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    return blob


def detect_faces(net, blob, image):
    """Perform face detection on the preprocessed image."""
    logging.info("Performing face detection...")
    net.setInput(blob)
    detections = net.forward()

    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Adjust confidence threshold as needed
            box = detections[0, 0, i, 3:7] * np.array(
                [image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            faces.append((startX, startY, endX, endY))
    return faces


def load_recognition_model(model_path):
    """Load pre-trained face recognition model."""
    logging.info(f"Loading face recognition model from {model_path}...")
    if not os.path.isfile(model_path):
        logging.error(f"Recognition model file not found: {model_path}")
        return None
    return dlib.face_recognition_model_v1(model_path)


def encode_faces(recognition_model, shape_predictor, image, faces):
    """Encode faces detected in the image using the recognition model."""
    logging.info("Encoding faces...")
    encodings = []
    for (startX, startY, endX, endY) in faces:
        rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
        shape = shape_predictor(image, rect)
        face_encoding = recognition_model.compute_face_descriptor(image, shape)
        if face_encoding:
            encodings.append(np.array(face_encoding))
        else:
            logging.warning(f"Failed to encode face at location: ({
                            startX}, {startY}, {endX}, {endY})")
    return encodings


def recognize_faces(face_encodings, known_encodings, known_names):
    """Recognize faces based on the given encodings and known encodings/names."""
    recognized_names = []
    for face_encoding in face_encodings:
        if len(known_encodings) == 0:
            recognized_names.append(None)
            continue
        distances = np.linalg.norm(
            np.array(known_encodings) - face_encoding, axis=1)
        min_distance_index = np.argmin(distances)
        min_distance = distances[min_distance_index]
        if min_distance < 0.6:  # Adjust threshold as needed
            recognized_names.append(known_names[min_distance_index])
        else:
            recognized_names.append(None)  # Face not recognized
    return recognized_names


def draw_boxes(image, boxes, names, color=(0, 255, 0)):
    """Draw bounding boxes around detected faces and label them with names."""
    for ((startX, startY, endX, endY), name) in zip(boxes, names):
        cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
        cv2.putText(image, name if name else "Unknown", (startX,
                    startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def load_age_prediction_model(model_path):
    """Load pre-trained age prediction model."""
    logging.info(f"Loading age prediction model from {model_path}...")
    if not os.path.isfile(model_path):
        logging.error(f"Age prediction model file not found: {model_path}")
        return None
    try:
        age_predictor = dlib.dnn_age_prediction(model_path)
    except Exception as e:
        logging.error(f"Failed to load age prediction model: {str(e)}")
        return None
    return age_predictor


def predict_age(age_predictor, image, face):
    """Predict the age of the face using the age prediction model."""
    logging.info("Predicting age...")
    (startX, startY, endX, endY) = face
    face_roi = image[startY:endY, startX:endX]
    dlib_rect = dlib.rectangle(startX, startY, endX, endY)
    age_prediction = age_predictor(image, dlib_rect)
    return age_prediction


def main():
    # Define paths to the pre-trained models and input image
    model_file = "res10_300x300_ssd_iter_140000.caffemodel"
    config_file = "deploy.prototxt.txt"
    input_image_path = " "
    recognition_model_file = "dlib_face_recognition_resnet_model_v1.dat"
    shape_predictor_file = "shape_predictor_68_face_landmarks.dat"
    age_predictor_model_file = "dnn_age_prediction.dat"

    try:
        # Load pre-trained models
        detection_net = load_detection_model(model_file, config_file)
        if detection_net is None:
            return
        recognition_model = load_recognition_model(recognition_model_file)
        if recognition_model is None:
            return
        shape_predictor = dlib.shape_predictor(shape_predictor_file)
        age_predictor = load_age_prediction_model(age_predictor_model_file)
        if age_predictor is None:
            return

        # Predict age for each detected face
        for face, name in zip(faces, recognized_names):
            if name is not None:
                age = predict_age(age_predictor, image, face)
                print(f"Predicted age for {name}: {age}")

        # Display the results
        cv2.imshow("Face Detection and Recognition", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
