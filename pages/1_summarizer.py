import streamlit as st
import pdfplumber
import requests
from bs4 import BeautifulSoup
from streamlit_chat import message
import openai_summarize

OpenAI_Key = st.secrets["OPENAI_KEY"]

def chatbot():
    message("My message") 
    message("Hello bot!", is_user=True)  # align's the message to the right


@st.cache_data
def summarizer(text):
    openai_summarizer = openai_summarize.OpenAISummarize(OpenAI_Key)
    summary = openai_summarizer.summarize_text(text)

    return summary


def main():
    st.title('Text summarizer')
    
    col1, col2 = st.columns([2, 1])

    with col1: 
        Option = st.selectbox("Choose the format", ('Text Input', 'Upload PDF', 'Web Article'), index=2)
        if Option == 'Text Input':
            txt = st.text_area('Text to summarize', '''Blockchain defined: Blockchain is a shared, immutable ledger that facilitates the process of recording transactions and tracking assets in a business network. An asset can be tangible (a house, car, cash, land) or intangible (intellectual property, patents, copyrights, branding). Virtually anything of value can be tracked and traded on a blockchain network, reducing risk and cutting costs for all involved.''')
            if txt is not None:
                summarized_text = summarizer(txt)
                if summarized_text:
                    st.success("Successfully summarized!")
                    st.write(summarized_text)

        elif Option == 'Upload PDF':
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file:
                try:
                    fulltext = ""
                    with pdfplumber.open(uploaded_file) as pdf:
                        # loop over all the pages
                        for page in pdf.pages:
                            fulltext += page.extract_text()
                        with st.expander("Extracted Text", expanded=False):
                            st.write(fulltext)
                        summarized_text = summarizer(fulltext)
                        
                        if summarized_text:
                            st.success("Successfully summarized!")
                            st.write(summarized_text)

                except:
                    st.error("Something went wrong!")

        elif Option == 'Web Article':   
            url = st.text_input("URL")
            if url:
                res = requests.get(url)
                html_page = res.content
                soup = BeautifulSoup(html_page, 'html.parser')
                text = soup.find_all(text=True)
                output = ''
                blacklist = [
                    '[document]',
                    'noscript',
                    'header',
                    'html',
                    'meta',
                    'head', 
                    'input',
                    'script',
                    'style',
                    'header_navMenu',
                    'sponsor_message',
                    'thread__wrapper',
                ]

                for t in text:
                    if t.parent.name not in blacklist:
                        output += '{} '.format(t).strip()

                fulltext = output.strip()
                with st.expander("Extracted Text", expanded=False):
                    st.write(fulltext)
                
                summarized_text = summarizer(fulltext)
                
                if summarized_text:
                    st.success("Successfully summarized!")
                    st.write(summarized_text)
    
    with col2:
        chatbot()
        


if __name__ == "__main__":
    main()


