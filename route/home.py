import streamlit as st
import os
import numpy as np
from keras.models import load_model
import cv2
from PIL import Image
from keras.preprocessing import image
import streamlit.components.v1 as html_components
from route.utils import set_css
from route.components import title

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
    set_css("route/css/streamlit.css")
    html_components.html(title())
    st.write("These are pre-cropped MRI scan samples. They were used to validate the model.\n")
    samples = os.listdir("route/samples")
    option = st.selectbox("Select an image for analysis", (range(1, len(samples) + 1)))
    collection = []
    for i in range(0, len(samples), 3):
        collection.append(st.columns(3))

    if i < len(samples) - 3:
        collection.append(st.columns(len(samples) - i))

    index = 0
    for column_list in collection:
        for i in range(len(column_list)):
            selected_image = Image.open(f"route/samples/{samples[index]}")
            selected_image = selected_image.resize((150, 150))
            column_list[i].image(selected_image)
            column_list[i].subheader(index + 1)
            index += 1

    if st.button("Analyze"):
        with st.spinner(text="Analyzing..."):
            model = load()
            selected_image_path = f"route/samples/{samples[option-1]}"
            predicted_class, confidence = predict(selected_image_path, model)

            st.write(
                """
                #### Prediction
                """
            )
            # Display the selected image
            selected_image = Image.open(selected_image_path)
            st.image(selected_image, width=300)

            st.write(f"Predicted Class: {predicted_class}")
            st.write(f"Confidence: {confidence*100:.2f}%")
