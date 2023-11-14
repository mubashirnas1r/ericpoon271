import streamlit as st
import requests
import json


import time
BASE_URL = 'http://35.202.171.250:8000'
# Define a function to simulate the chatbot's responses
def chatbot_response(user_message,vector_db,user_prompt):
    url = f'{BASE_URL}/conversation'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "user_id": "test",
        "user_prompt": user_prompt,
        "user_message": user_message,
        "vector_db_collection": vector_db
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Request was successful")
        print(response.json())
    else:
        print("Request failed with status code:", response.status_code)
        print(response.text)
    
    return response.json()['message']

def extract_collection_names(data):
    if 'colllections' in data:
        collections = data['colllections']
        collection_names = [collection['collection_name'] for collection in collections]
        return collection_names
    else:
        return []
# Streamlit app


# Add a sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to:", ["Chat", "Train Chatbot"])

if selected_page == "Chat":
    # Chatbot page
    st.title("Chatbot (user_id=testuser123)")
    # Chatbot page
    url = f'{BASE_URL}/get_collections'
    headers = {
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Request was successful")
        print(response.json())
    else:
        print("Request failed with status code:", response.status_code)
        print(response.text)

    with st.form(key="chat_form"):
        user_input = st.text_input("Your Query:", "")

        # Additional parameters for the chatbot
        collections = st.multiselect("Select Collections:", extract_collection_names(response.json()))
        user_prompt = st.text_input("User Prompt:", "")

        # Use JavaScript to trigger the form submission on Enter key press
        st.markdown(
            """
            <script>
            var input = document.querySelector("input");
            input.addEventListener("keyup", function(event) {
                if (event.key === "Enter") {
                    document.querySelector("form").submit();
                }
            });
            </script>
            """,
            unsafe_allow_html=True,
        )

        submit_button = st.form_submit_button("Submit")
    if submit_button:
        with st.spinner("Chatbot is responding..."):
            print("User Input: ", user_input)
            print("collections to search: ",collections)
            print("user prompt: ",user_prompt)
            bot_response = chatbot_response(user_message=user_input,vector_db=collections,user_prompt=user_prompt)
            st.markdown(f'<div style="background-color: #0B7BC7; color: white; padding: 10px; border-radius: 10px;">Chatbot: {bot_response}</div>', unsafe_allow_html=True)
else:
    # File upload page
    st.title("Train Chatbot")
    with st.form(key="file_upload_form"):
        st.write("File Information")
        file_name = st.file_uploader("Upload File (txt or pdf):", type=["txt", "pdf"])
        vector_db_name = st.text_input("Vector DB Name:")

        # Use JavaScript to trigger the form submission on Enter key press
        st.markdown(
            """
            <script>
            var inputs = document.querySelectorAll("input, textarea");
            inputs.forEach(function(input) {
                input.addEventListener("keyup", function(event) {
                    if (event.key === "Enter") {
                        document.querySelector("form").submit();
                    }
                });
            });
            </script>
            """,
            unsafe_allow_html=True,
        )

        submit_button = st.form_submit_button("Submit")

    # Handle the form submission
    if submit_button:
        with st.spinner("Uploading file..."):
            if file_name is not None:
                # Prepare data for the request
                url = f'{BASE_URL}/upload_content'
                headers = {
                    'accept': 'application/json',
                }

                # Determine file type
                file_type = "application/pdf" if file_name.type == "application/pdf" else "text/plain"

                files = {'file': (file_name.name, file_name, file_type)}
                params = {'vector_db_collection': vector_db_name}

                # Make the API request
                response = requests.post(url, headers=headers, files=files, params=params)

                if response.status_code == 200:
                    print("Request was successful")
                    print(response.json())
                    bot_response = response.json()['message']
                    st.markdown(
                        f'<div style="background-color: #338864; color: white; padding: 10px; border-radius: 10px;">Message: {bot_response}</div>',
                        unsafe_allow_html=True)
                else:
                    print("Request failed with status code:", response.status_code)
                    print(response.text)
                    bot_response = response.json()['message']
                    st.markdown(
                        f'<div style="background-color: #D30000; color: white; padding: 10px; border-radius: 10px;">Message: {bot_response}</div>',
                        unsafe_allow_html=True)
            else:
                st.warning("Please upload a .txt or .pdf file before submitting.")
