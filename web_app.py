import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import time

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
        if make_hashes(password) == hashed_text:
                return hashed_text
        return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

def login_user(username,password):
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()
        return data


def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

def estimate():
    #giving a title to the page
    st.title('House Price Prediction System')

    #getting the input data from the user
    district = st.selectbox("Select a District", list(district_data.keys()))
    if district:
        area = district_data[district]
        st.write(f"The area code of {district} is {area}")
								
    # Getting the input data from the user
    area = st.text_input('Area of the house')
    bedrooms = st.text_input('Number of Bedrooms')
    bathrooms = st.text_input('Number of Bathrooms')
    stories = st.text_input('Number of Storey')
    mainroad = st.text_input('Is there a Mainroad? (0 or 1)')
    guestroom = st.text_input('Is there a Guestroom? (0 or 1)')
    basement = st.text_input('Is there a Basement? (0 or 1)')
    hotwaterheating = st.text_input('Is there hot water heating? (0 or 1)')
    airconditioning = st.text_input('Is there air conditioning? (0 or 1)')
    parking = st.text_input('Number of parking spaces')
    prefarea = st.text_input('Is there a preferred area? (0 or 1)')
    
    sclarea = st.text_input('School / College nearby (0 or 1)')
    furnishingstatus = st.text_input('Furnishing status (unfurnished-0, semi-furnished-1, or furnished-2)')

    # Initialize session state for price and hiddenPrice
    if 'price' not in st.session_state:
        st.session_state.price = 0
    if 'hiddenPrice' not in st.session_state:
        st.session_state.hiddenPrice = 0

    #creating a button
    if st.button('Predict the price of the house'):
        try:
            area = int(area)
            bedrooms = int(bedrooms)
            bathrooms = int(bathrooms)
            stories = int(stories)
            mainroad = int(mainroad)
            guestroom = int(guestroom)
            basement = int(basement)
            hotwaterheating = int(hotwaterheating)
            airconditioning = int(airconditioning)
            parking = int(parking)
            prefarea = int(prefarea)
            furnishingstatus = int(furnishingstatus)
            st.session_state.price = house_price_prediction([area,bedrooms,bathrooms,stories,mainroad,guestroom,basement,hotwaterheating,airconditioning,parking,prefarea,furnishingstatus])
            st.success(f'The price of the house is: {st.session_state.price}')
        except ValueError:
            st.error("Please enter valid numerical values for all inputs.")

    st.divider()

    st.subheader('Hidden Costs while buying the house')
    transferFee = st.text_input(" 1 Society Transfer Fee (Cost that goes to society fund)")
    maintainance = st.text_input(" 2 Maintainance Cost (per year)")
    homeInsurance = st.text_input(" 3 Home Insurance (Basic - 3000, Comprehensive - 5000, Premium - 10000")
    propertyTax = st.text_input(" 4 Property Tax (Enter 20.4 for residential & 34.68 for Commercial)")
    brokerFee = st.text_input(" 5 Brokerage")
    st.text(" 6 Sales Deed (Price * 0.06)")

    hiddenPrice = 0

    if st.button('Calculate the hidden costs'):
        try:
            transferFee = int(transferFee)
            maintainance = int(maintainance)
            homeInsurance = int(homeInsurance)
            st.session_state.price = house_price_prediction([area,bedrooms,bathrooms,stories,mainroad,guestroom,basement,hotwaterheating,airconditioning,parking,prefarea,furnishingstatus])
            salesDeed = st.session_state.price * 0.06
            propertyTax = float(propertyTax)
            propertyTax = float(area) * propertyTax
            brokerFee = int(brokerFee)
            st.session_state.hiddenPrice = hidden_price_prediction([transferFee,maintainance,homeInsurance,salesDeed,propertyTax,brokerFee,st.session_state.price])
            st.success(f'The initial cost of the house: {st.session_state.price}')
            st.success(f'The final cost of the house in a year is: {st.session_state.hiddenPrice}')
        except ValueError:
            st.error("Please enter valid numerical values for all inputs.")



# Set the page config
st.set_page_config(page_title='House Price Prediction System')

#loading the model
loaded_model = pickle.load(open('Property_acquisition_cost_predictor.sav','rb'))
district_data = {
    "Ariyalur": 2000,
    "Chengalpattu": 2145,
    "Chennai": 16200,
    "Coimbatore": 2135,
    "Cuddalore": 2400,
    "Dharmapuri": 2400,
    "Dindigul": 1836,
    "Erode": 1700,
    "Kallakurichi": 2430,
    "Kanchipuram": 2400,
    "Kanniyakumari": 2430,
    "Karur": 2430,
    "Krishnagiri": 1836,
    "Madurai": 2135,
    "Mayiladuthurai": 1836,
    "Nagapattinam": 2430,
    "Namakkal": 2400,
    "Nilgiris": 2400,
    "Perambalur": 2430,
    "Pudukkottai": 1836,
    "Ramanathapuram": 2430,
    "Ranipet": 1836,
    "Salem": 2000,
    "Sivagangai": 2400,
    "Tenkasi": 2430,
    "Thanjavur": 2430,
    "Theni": 2400,
    "Thoothukudi": 1836,
    "Tiruchirappalli": 2430,
    "Tirunelveli": 2430,
    "Tirupathur": 2400,
    "Tiruppur": 1836,
    "Tiruvallur": 2430,
    "Tiruvannamalai": 2400,
    "Tiruvarur": 2430,
    "Vellore": 2430,
    "Viluppuram": 2400,
    "Virudhunagar": 1836,
    "Bangalore": 1905
}

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'House Price Prediction System',
        ['Home','Estimate Cost', 'Visualiser'],
        default_index=0
    )

def house_price_prediction(input_data):

    #changing input data as numpy array
    input_data_numpy = np.asarray(input_data)

    #reshaping the array because if we don't the model thinks we will provide 543 data but we are provided only 1 and so we need to reshape for one instance.
    input_data_numpy_reshape = input_data_numpy.reshape(1,-1)

    prediction1 = loaded_model.predict(input_data_numpy_reshape)
    return prediction1[0]

def hidden_price_prediction(input_data):
    finalPrice = sum(input_data)
    return finalPrice

if selected == 'Home':
    st.title('House Price Prediction System')
    st.markdown(
        """
        ### 🔍 What It Does:
        1. Predicts House Costs: Utilizing a robust machine learning model, it accurately estimates the cost of a house based on various features like number of bedrooms, bathrooms, and more.
        2. Calculates Hidden Costs: Beyond the base price, it calculates hidden costs such as society transfer fees, maintenance, insurance, property tax, brokerage, and sales deeds.
        3. Visualizes Housing Data: With an intuitive visualizer, users can explore and understand housing data trends through different types of plots.

        ### 🔧 Technologies Used:
        - Streamlit: For an interactive and user-friendly web interface.
        - Pandas, Seaborn, Matplotlib: For data handling and visualization.
        - Numpy, Pickle: For efficient data processing and model loading.
    """
    )

if selected=='Estimate Cost': 
	st.markdown("<h4 style='text-align: center; color: green;'>Login / Sign up Page</h4>", unsafe_allow_html=True)
	menu = ["ADMIN LOGIN","USER LOGIN","SIGN UP","ABOUT US"]
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "ADMIN LOGIN":
		st.markdown("<h1 style='text-align: center;'>Admin Login Section</h1>", unsafe_allow_html=True)
		user = st.sidebar.text_input('Username')
		passwd = st.sidebar.text_input('Password',type='password')
		if st.sidebar.checkbox("LOGIN"):
			if user == "Admin" and passwd == 'admin123':
				st.success("Logged In as {}".format(user))
				st.subheader("User Profiles")
				user_result = view_all_users()
				clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                                st.dataframe(clean_db)
				 estimate()
				 
                         else:
                                st.warning("Incorrect Admin Username/Password")
          
                         
                        

        elif choice == "USER LOGIN":
                st.markdown("<h1 style='text-align: center;'>User Login Section</h1>", unsafe_allow_html=True)
                username = st.sidebar.text_input("User Name")
                password = st.sidebar.text_input("Password",type='password')
                if st.sidebar.checkbox("LOGIN"):
                        # if password == '12345':
                        create_usertable()
                        hashed_pswd = make_hashes(password)

                        result = login_user(username,check_hashes(password,hashed_pswd))
                        if result:

                                st.success("Logged In as {}".format(username))
				estimate()
                        else:
                                st.warning("Incorrect Username/Password")
                                st.warning("Please Create an Account if not Created")





        elif choice == "SIGN UP":
                st.subheader("Create New Account")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password",type='password')

                if st.button("SIGN UP"):
                        create_usertable()
                        add_userdata(new_user,make_hashes(new_password))
                        st.success("You have successfully created a valid Account")
                        st.info("Go to User Login Menu to login")

	estimate()


if selected == 'Visualiser':
    #giving a title to the page
    st.title('Data Visualizer for housing price dataset')

    # Read the selected CSV file
    df = pd.read_csv("Housing.csv")

    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

    # Generate the plot based on user selection
    if st.button('Generate Plot'):

        fig, ax = plt.subplots(figsize=(6, 4))

        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
            y_axis='Density'
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
            y_axis = 'Count'

        # Adjust label sizes
        ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
        ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

        # Adjust title and axis labels with a smaller font size
        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)

        # Show the results
        st.pyplot(fig)
