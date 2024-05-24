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
    logging.info(f"Loading face detection model from {
                 model_file} and {config_file}...")
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


def main():
    # Define paths to the pre-trained models and input image
    model_file = "res10_300x300_ssd_iter_140000.caffemodel"
    config_file = "deploy.prototxt.txt"
    input_image_path = " "
    recognition_model_file = "dlib_face_recognition_resnet_model_v1.dat"
    shape_predictor_file = "shape_predictor_68_face_landmarks.dat"

    try:
        # Load pre-trained models
        detection_net = load_detection_model(model_file, config_file)
        if detection_net is None:
            return
        recognition_model = load_recognition_model(recognition_model_file)
        if recognition_model is None:
            return
        shape_predictor = dlib.shape_predictor(shape_predictor_file)

        # Load known face encodings and names from existing folders
        known_encodings = []
        known_names = []
        name_to_folder_map = {}
        base_folder = "/Users/srivatsa/digiboxx/"

        for person_name in os.listdir(base_folder):
            person_folder = os.path.join(base_folder, person_name)
            if os.path.isdir(person_folder):
                name_to_folder_map[person_name] = person_folder
                for file_name in os.listdir(person_folder):
                    if file_name.endswith(".jpg"):
                        face_image_path = os.path.join(
                            person_folder, file_name)
                        face_image = cv2.imread(face_image_path)
                        if face_image is not None:
                            face_encoding = encode_faces(recognition_model, shape_predictor, face_image, [
                                                         (0, 0, face_image.shape[1], face_image.shape[0])])
                            known_encodings.extend(face_encoding)
                            known_names.extend(
                                [person_name] * len(face_encoding))

        # Read the input image
        image = cv2.imread(input_image_path)
        if image is None:
            logging.error("Failed to read input image.")
            return

        # Create a copy of the original image for saving later
        original_image = image.copy()

        # Preprocess the image for face detection
        blob = preprocess_image(image)

        # Perform face detection
        faces = detect_faces(detection_net, blob, image)

        # Encode faces using the recognition model
        face_encodings = encode_faces(
            recognition_model, shape_predictor, image, faces)

        # Recognize faces
        recognized_names = recognize_faces(
            face_encodings, known_encodings, known_names)

        # Draw bounding boxes around detected faces and label with recognized names
        draw_boxes(image, faces, recognized_names)

        # Display the results
        cv2.imshow("Face Detection and Recognition", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Automatically add photos to folders based on recognition results
        added_names = set()
        for name in recognized_names:
            if name is None:
                person_name = input("Please enter the name of the person: ")
            else:
                person_name = name

            if person_name not in added_names:
                folder_path = os.path.join(base_folder, person_name)
                os.makedirs(folder_path, exist_ok=True)
                added_names.add(person_name)

        # Save the original image to the appropriate folders
        for name in recognized_names:
            if name is not None:
                folder_path = os.path.join(base_folder, name)
                file_name = f"{uuid.uuid4()}.jpg"
                image_path = os.path.join(folder_path, file_name)
                cv2.imwrite(image_path, original_image)

        # Handle unknown faces
        for name in recognized_names:
            if name is None:
                person_name = input(
                    "Please enter the name for the unknown face: ")
                folder_path = os.path.join(base_folder, person_name)
                os.makedirs(folder_path, exist_ok=True)
                file_name = f"{uuid.uuid4()}.jpg"
                image_path = os.path.join(folder_path, file_name)
                cv2.imwrite(image_path, original_image)
                # Add the new face to the known faces list
                face_encoding = encode_faces(
                    recognition_model, shape_predictor, image, faces)
                known_encodings.extend(face_encoding)
                known_names.extend([person_name] * len(face_encoding))

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
