import streamlit as st
from openai import OpenAI

# Set the app name
st.set_page_config(page_title="GeniusDoc", page_icon="📄")

# Sidebar navigation for separate pages
def main():
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Upload Document", "Terms and Conditions"])

    if menu == "Upload Document":
        upload_document()
    elif menu == "Terms and Conditions":
        terms_and_conditions()

def upload_document():
    st.title("📄 Document Question Answering")
    st.write(
        "Upload a document below and ask a question about it – GPT will answer! "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
    )

    # Ask user for their OpenAI API key via `st.text_input`.
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:
        # Create an OpenAI client.
        client = OpenAI(api_key=openai_api_key)

        # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        # Ask the user for a question via `st.text_area`.
        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            disabled=not uploaded_file,
        )

        if uploaded_file and question:
            # Process the uploaded file and question.
            document = uploaded_file.read().decode()
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
            ]

            # Generate an answer using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

            # Stream the response to the app using `st.write_stream`.
            st.write_stream(stream)

def terms_and_conditions():
    st.title("Terms and Conditions")
    st.write("""
    ## Terms and Conditions
    Welcome to **GeniusDoc**. By using our application, you agree to the following terms:
    
    ### 1. Acceptance of Terms
    By accessing or using GeniusDoc, you agree to comply with these Terms and Conditions and our Privacy Policy.
    
    ### 2. Features
    - **Upload and Process Documents**: Users can upload files for analysis.
    - **AI Integration**: OpenAI models are used for analysis.
    - **VectorDB Storage**: Embedding data is stored securely in AstraDB.
    
    ### 3. User Responsibilities
    - Ensure that uploaded data complies with laws and regulations.
    - Avoid uploading sensitive or confidential information unless authorized.
    
    ### 4. Data Privacy
    - Uploaded data is used only for analysis and temporarily stored.
    - GeniusDoc does not share or sell your data to third parties.
    
    ### 5. Limitations
    - Service is provided "as is" without guarantees.
    - GeniusDoc is not liable for errors, delays, or interruptions.
    
    ### 6. Modifications
    - GeniusDoc may update these terms at any time, with continued use indicating acceptance.
    
    ### 7. Contact
    For inquiries, email support@geniusdoc.app.
    """)

if __name__ == "__main__":
    main()
