import streamlit as st
import pandas as pd

st.title("WELCOME TO *BMI Calculator* La *calculatrice de l'avenir*")
poid,statut= st.columns(2)
weight = poid.number_input('Enter your weight in kgs')
status = statut.radio('Select you heit format :',('cms','meters','feats'))

try:
    if status == 'cms':
        heigth = st.number_input('Centimeters')
        bmi = weight/((heigth/100)**2)
    elif status == 'meters':
        heigth = st.number_input('Meters')
        bmi = weight/((heigth)**2)
    else : 
        heigth = st.number_input('Feets')
        bmi = weight/((heigth/3.28)**2)
except:
    print('Zero division error')

if (st.button('Calculate BMI')) : 
    st.write('Your BMI index is {}'.format(round(bmi)))
    if bmi < 16:
        st.error('Your are extremely underweight')
    elif(bmi>=16 and bmi <18.5):
        st.warning('Your are underweight')
    elif (bmi>=18.5 and bmi <25):
        st.success('Your are Healthy')
    elif (bmi>=25 and bmi <30):
        st.warning('Your are Overweight')
    elif (bmi>=30):
        st.error('Your are extremely Overweight')