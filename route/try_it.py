import streamlit as st
import os
import numpy as np
import cv2
import streamlit.components.v1 as html_components
from route.utils import set_css
from route.components import title
from keras.preprocessing import image
from keras.models import load_model

@st.cache_resource()
def load():
    model = load_model('effb3.keras')
    return model

class_names = {0: 'glioma', 1: 'meningioma', 2: 'notumor', 3: 'pituitary'}

def predict(image_file, model):
    # Read the image file
    img = image.load_img(image_file, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Make predictions
    prediction = model.predict(img_array)[0]
    predicted_class_index = np.argmax(prediction)
    predicted_class_name = class_names[predicted_class_index]

    return predicted_class_name, prediction[predicted_class_index]


def main():
    html_components.html(title())
    set_css("route/css/streamlit.css")
    st.write(
        """Here, you can upload your MRI image of choice and see the analysis results.
    The program will automatically crop the image to the brain area and then analyzes the 
    image. The results will be displayed below."""
    )
    image_bytes = st.file_uploader(
        "Upload a brain MRI scan image", type=["png", "jpeg", "jpg"]
    )

    def format_func(item):
        return item

    if image_bytes:
        array = np.fromstring(image_bytes.read(), np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (128, 128))
        st.write(
            """
                #### Brain MRI scan image
                """
        )
        st.image(image)
    

    if st.button("Analyze"):
        if image_bytes is None:
            st.warning("Please upload an image.")
        else:
            with st.spinner(text="Analyzing..."):
                model = load()
                predicted_class, confidence = predict(image_bytes, model)
    
                st.write(
                    """
                    #### Prediction
                            """
                )
                st.write(f"Predicted Class: {predicted_class}")
                st.write(f"Confidence: {confidence*100:.2f}%")