import streamlit as st
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

st.title("顔認証アプリ")

subscription_key = 'e00e27f8985045b18c1204f55c2d1d7e'
assert subscription_key
face_api_url = 'https://20210418kazu.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file = st.file_uploader("Choose an image...",type=None)
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    

    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img = output.getvalue() #バイナリ取得ß
    
    
    headers = {"Content-Type" : "application/octet-stream",
               "Ocp-Apim-Subscription-Key":subscription_key}
    
    params = {
              "returnFaceId"  :  "true",
              "returnFaceAttributes" : "age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"}
           
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)



    results = res.json()

    number = len(results)

    st.write(f"写ってる人数は {number}名　です。")

    for result in results:
        rect = result["faceRectangle"]
        age = result["faceAttributes"]["age"]
        str_age = str(age)
        gender = result["faceAttributes"]["gender"]
        str_gender = str(gender)
        emotion = result["faceAttributes"]["emotion"]
        emotion_text = max(emotion,key=emotion.get)
        text = "age :" + str_age + "\n" + str_gender
        text2 = emotion_text
        fontsize = int(rect["width"]/6)
        font = ImageFont.truetype("TakaoPGothic.ttf",size=fontsize)
        
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect["left"],rect["top"]),(rect["left"]+rect["width"],rect["top"]+rect["height"])],fill=None,outline="red",width=2)
        draw.text((rect["left"],rect["top"]-rect["height"]/5),text,font=font,fill=(0,225,255,0))
        draw.text((rect["left"],rect["top"]+rect["height"]*4/5),text2,font=font,fill=(0,225,255,0))

  
    

    st.image(img,caption="Uploaded Image...",use_column_width=True)
