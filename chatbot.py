import streamlit as st
import requests
import json


import time

# Define a function to simulate the chatbot's responses
def chatbot_response(user_message,vector_db,user_prompt):
    url = 'http://35.202.171.250:8000/conversation'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "user_id": "testuser123",
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
    url = 'http://35.202.171.250:8000/get_collections'
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
        file_name = st.text_input("File Name:", help="Only txt and pdf are allowed.")
        file_content = st.text_area("File Content:")
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
            # Perform file upload and processing here
            # You can access the user input using file_name, file_content, and vector_db_name
            # Example: Save the uploaded file, perform processing, etc.
            print("File Name:", file_name)
            print("File Content:", file_content)
            print("Vector DB Name:", vector_db_name)
            # Simulate a chatbot response
            url = 'http://35.202.171.250:8000/upload_content'
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }

            data = {
                "file_name": file_name,
                "file_content": file_content,
                "vector_db_collection": vector_db_name
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                print("Request was successful")
                print(response.json())
                bot_response = response.json()['message']
                st.markdown(f'<div style="background-color: #338864; color: white; padding: 10px; border-radius: 10px;">Message: {bot_response}</div>', unsafe_allow_html=True)
            else:
                print("Request failed with status code:", response.status_code)
                print(response.text)
                bot_response = response.json()['message']
                st.markdown(f'<div style="background-color: #D30000; color: white; padding: 10px; border-radius: 10px;">Message: {bot_response}</div>', unsafe_allow_html=True)
                        
            
