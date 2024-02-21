import base64
import re
from io import BytesIO

import requests
import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text
import os

# configuring the page and the logo
st.set_page_config(
  page_title='روبوت استقطاب العملاء المدعوم بالذكاء الاصطناعي - نموذج الرد على الاستفسارات الصوتية', page_icon='Logo_Transperentackground.png',
    layout='centered',
    initial_sidebar_state='auto')

# removing everything related to streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Define the API URL (replace with your actual API endpoint)
api_url = "http://51.20.55.92:3000/api/v1/prediction/48a3831b-0708-4d87-8de4-d26ac3215cc7"


# Function to make API calls
def query(payload):
  response = requests.post(api_url, json=payload)
  return response.json()

# Function to extract and format hyperlinks
def format_hyperlinks(text):
  hyperlinks = re.findall(r"https?://\S+", text)  # Find URLs in the text
  for link in hyperlinks:
      text = text.replace(link, f"<br><a href='{link}'>{link}</a>") 
#Replace with formatted links
  return text


def autoplay_audio(file_path: str):
  with open(file_path, "rb") as f:
      data = f.read()
      b64 = base64.b64encode(data).decode()
      md = f"""
        <audio controls autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
      audio_container = st.empty()
      audio_container.markdown(
          md,
          unsafe_allow_html=True,
      )
      return audio_container

previous_container = None
previous_text = None  # Store the previous displayed text


#centering the logo
left_co, cent_co, last_co = st.columns(3)
with left_co:
  st.write("")
with cent_co:
  # st.image(logo)
  st.markdown(
      """<center><a href="https://www.morafiqy.com">
      <img src="data:image/png;base64,{}" width="100">
      </a></center>""".format(
          base64.b64encode(
              open("images/Logo_Transperentackground.png",
                   "rb").read()).decode()),
      unsafe_allow_html=True,
  )
with last_co:
  st.write("")

# changing the color and font of a specific text line in streamlit
# st.title("Streamlit API Interaction with Fixed Response Area")
original_title = '<p style="font-family:Tajawal; color:#00008B; font-size: 25px; text-align: center;"><b>روبوت استقطاب العملاء المدعوم بالذكاء الاصطناعي - نموذج الرد على الاستفسارات الصوتية</b></p>'
st.markdown(original_title, unsafe_allow_html=True)


#dividing the page to center the text and the image
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:

    text = speech_to_text(language='ar', use_container_width=True, key='STT')
    # st.markdown(':arrow_up:')
    # st.rerun()

with col3:
    st.write(' ')

if text:
  # Clear previous audio and text if different from current
  if text != previous_text:
      # st.rerun()
      if previous_container:
          previous_container.empty()
      if previous_text:
          st.empty()  # Clear the text container where previous_text was displayed
      payload = {"question": text}
      api_response = query(payload)

      # ... (rest of your code, including API call, generating/saving audio)
      if "text" in api_response:
        st.markdown(
            f"""<p style="font-family:Tajawal; color:red; font-size: 20px;text-align: right;"><b>{text}</b></p>""",
            unsafe_allow_html=True)

        # convert text to speech
        text_to_speech = gTTS(text=api_response["text"],
                              tld="us",
                              lang='ar',
                              slow=False)

        # save the audio file
        text_to_speech.save('audioResponse/test.mp3')

  # Update references for next iteration
  if previous_container:
      previous_container.empty()  # Ensure audio is cleared regardless of playback status
  new_container = autoplay_audio("audioResponse/test.mp3")
  previous_container = new_container

  # Parse and format the text
  formatted_text = format_hyperlinks(api_response["text"])

  # Create the styled paragraph
  api_answer = f"""<p style="font-family:Tajawal; color:#00008B; font-size: 16px; text-align: right; direction: rtl;">{formatted_text}</p>"""

  # Display the formatted text with hyperlinks
  st.markdown(api_answer, unsafe_allow_html=True)
  previous_text = formatted_text  # Update the stored text

  # st.markdown(api_response["text"])
else:
  initial_warning='<p style="font-family:Tajawal; color:brown; font-size: 20px;text-align: center;"><b> تفضل بالضغط على الزر بالأعلى واطرح سؤالك</b></p>'
  # initial_warning='<center>'+ ':arrow_up:'+'</center>'
  st.markdown(initial_warning, unsafe_allow_html=True)
    # initial_warning="\:tulip::cherry_blossom::rose::hibiscus::sunflower::blossom::arrow_up_small::arrow_double_up::arrow_up:"


warning_title = '<p style="font-family:Tajawal; color:brown; font-size: 10px;text-align: center;"><b>ملحوظة هامة: ** تمتلك شركة مرافقي جميع حقوق الملكية الفكرية لمنتجاتها، بما في ذلك حقوق الطبع والنشر والعلامات التجارية والاختراعات. يحظر أي استخدام أو توزيع أو نسخ أو تعديل أو إعادة إنتاج أو نشر أو ترجمة أو تحويل أو استغلال لأي من منتجات مرافقي بأي شكل من الأشكال دون إذن كتابي مسبق من الشركة. يعرض أي انتهاك لهذه الحقوق الشركة لاتخاذ الإجراءات القانونية المناسبة، بما في ذلك المطالبة بالتعويضات عن الأضرار. </b></p>'
st.markdown(warning_title, unsafe_allow_html=True)

#dividing the page to center the text and the image
col1, col2, col3 = st.columns(3)

with col1:
  st.write(' ')

with col2:
  url = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ2BaKz9afnmfWTN3djAAR17pweSaeRa6FSgqi0ISQ3mbhb6Bm99R7mBKf7odChWFXN02zM1YZRQ"
  # # st.write(<div style="text-align: center"> url </div>
  st.write("إ[حصل على موعد استشارة مجانية](%s)" % url)

  #hyperlinking an image
  st.markdown(
      """<center><a href="https://www.morafiqy.com">
      <img src="data:image/png;base64,{}" width="100">
      </a></center>""".format(
          base64.b64encode(open("images/Logo_Transperentackground.png", "rb").read()).decode()
      ),
      unsafe_allow_html=True,
  )

with col3:
  st.write(' ')





with open("css/style.css") as f:
  st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Powered by: <a href="https://www.Morafiqy.com">Morafiqy</a></p>
<!--img src="images/Logo_Transperentackground.png" width="30" height="30">
</div>
"""
st.markdown(footer,unsafe_allow_html=True)