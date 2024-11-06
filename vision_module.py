import cv2  # OpenCV for computer vision tasks
import numpy as np
from error_logger import ErrorLogger
from tensorflow.keras.models import load_model  # Example for a deep learning model
from tensorflow.keras.applications import ResNet50  # Pre-trained model
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

class VisionModule:
    """
    Advanced Vision Module for image processing, object recognition, classification, and feature extraction.
    """

    def __init__(self):
        self.error_logger = ErrorLogger()
        self.model = ResNet50(weights='imagenet')  # Load pre-trained model for classification
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def load_image(self, file_path: str) -> np.ndarray:
        """
        Loads an image from a specified file path.
        Args:
            file_path (str): Path to the image file.
        Returns:
            np.ndarray: Loaded image as an array.
        """
        try:
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError("Image not found or unsupported format.")
            return image
        except Exception as e:
            self.error_logger.log(f"Failed to load image: {e}")
            return None

    def preprocess_image_for_model(self, image: np.ndarray, target_size: tuple = (224, 224)) -> np.ndarray:
        """
        Preprocesses an image for model input (e.g., resizing, normalization).
        Args:
            image (np.ndarray): Image array.
            target_size (tuple): Target size for resizing.
        Returns:
            np.ndarray: Preprocessed image.
        """
        try:
            resized_image = cv2.resize(image, target_size)
            image_array = np.expand_dims(resized_image, axis=0)
            return preprocess_input(image_array)
        except Exception as e:
            self.error_logger.log(f"Failed to preprocess image for model: {e}")
            return None

    def detect_faces(self, image: np.ndarray) -> list:
        """
        Detects faces in an image using Haar cascades.
        Args:
            image (np.ndarray): Image array.
        Returns:
            list: List of bounding boxes for detected faces.
        """
        try:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            return [{"x": x, "y": y, "width": w, "height": h} for (x, y, w, h) in faces]
        except Exception as e:
            self.error_logger.log(f"Failed to detect faces: {e}")
            return []

    def detect_edges(self, image: np.ndarray, threshold1: int = 100, threshold2: int = 200) -> np.ndarray:
        """
        Applies edge detection on an image using the Canny method.
        Args:
            image (np.ndarray): Input image.
            threshold1 (int): First threshold for the hysteresis procedure.
            threshold2 (int): Second threshold for the hysteresis procedure.
        Returns:
            np.ndarray: Image with detected edges.
        """
        try:
            edges = cv2.Canny(image, threshold1, threshold2)
            return edges
        except Exception as e:
            self.error_logger.log(f"Failed to detect edges: {e}")
            return None

    def recognize_objects(self, image: np.ndarray) -> list:
        """
        Recognizes objects in an image using a pre-trained ResNet model.
        Args:
            image (np.ndarray): Image to analyze.
        Returns:
            list: Detected objects with their labels and confidence.
        """
        try:
            preprocessed_image = self.preprocess_image_for_model(image)
            if preprocessed_image is None:
                return []

            predictions = self.model.predict(preprocessed_image)
            decoded_predictions = decode_predictions(predictions, top=5)[0]
            return [{"label": label, "description": desc, "confidence": float(conf)} for (label, desc, conf) in decoded_predictions]
        except Exception as e:
            self.error_logger.log(f"Failed to recognize objects: {e}")
            return []

    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """
        Extracts feature embeddings from an image using the ResNet model's layers.
        Args:
            image (np.ndarray): Image to analyze.
        Returns:
            np.ndarray: Feature vector for the image.
        """
        try:
            preprocessed_image = self.preprocess_image_for_model(image)
            if preprocessed_image is None:
                return None

            # Using the layer output just before the classifier
            feature_extractor = Model(inputs=self.model.input, outputs=self.model.get_layer('avg_pool').output)
            features = feature_extractor.predict(preprocessed_image)
            return features
        except Exception as e:
            self.error_logger.log(f"Failed to extract features: {e}")
            return None

    def classify_image(self, image: np.ndarray) -> str:
        """
        Classifies an image using the ResNet model to return the top prediction.
        Args:
            image (np.ndarray): Image to classify.
        Returns:
            str: Classification label.
        """
        try:
            detected_objects = self.recognize_objects(image)
            if detected_objects:
                return detected_objects[0]["description"]  # Return the most likely label
            return "unknown"
        except Exception as e:
            self.error_logger.log(f"Failed to classify image: {e}")
            return "error"

# Example usage
if __name__ == "__main__":
    vision = VisionModule()

    # Load and preprocess an example image
    image = vision.load_image("example.jpg")
    if image is not None:
        # Detect faces
        faces = vision.detect_faces(image)
        print("Detected faces:", faces)

        # Edge detection
        edges = vision.detect_edges(image)
        print("Detected edges:", edges)

        # Object recognition
        objects = vision.recognize_objects(image)
        print("Recognized objects:", objects)

        # Feature extraction
        features = vision.extract_features(image)
        print("Extracted features:", features)

        # Classification
        label = vision.classify_image(image)
        print("Classification label:", label)