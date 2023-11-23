#! /usr/bin/env python3

__version__ = "1.0.4"
__author__ = "Kevin Brown"

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pynetbox import api

#######################
# GLOBAL VARS - BEGIN #
#######################

# Load environment variables from the .env file
load_dotenv()

# Read the URL and API token from the environment variables
netbox_url = os.getenv("NETBOX_API_URL")
api_token = os.getenv("NETBOX_API_TOKEN")

# Connect to the NetBox API
nb = api(url=netbox_url, token=api_token, threading=True)

#####################
# GLOBAL VARS - END #
#####################

############################
# HELPER FUNCTIONS - BEGIN #
############################

def wait_for_user_input():
  st.checkbox("<- Click to Submit!", key="clicked")
  clicked = st.session_state.get("clicked", False)
  while not clicked:
    clicked = st.session_state.get("clicked", False)

def choice1():
    with st.spinner("Executing API calls and collecting responses. This may take a moment..."):
        user_query = nb.dcim.devices.all()
    return user_query

def choice2():
    with st.spinner("Executing API calls and collecting responses. This may take a moment..."):
        user_query = nb.dcim.interfaces.all()
    return user_query

def choice3():
    # Query user for Device ID
    device_id = st.number_input("Device ID:", value=None, placeholder=2383)
    
    wait_for_user_input()

    st.write("Querying:", device_id)

    # wait_for_user_input()

    # device_id = int(device_id)

    # Get the device name for the provided device id
    device_name = nb.dcim.devices.get(id=device_id)

    # Break if there is no entry for the provided device id
    if device_name == None:
        st.write(device_id, " does not have an entry. Please provide a valid Device ID.")

    st.write("Querying interfaces associated with Device ID ", device_id, " > > > > ", device_name, " ...")
    user_query = nb.dcim.interfaces.filter(device=device_name)
    return user_query

def choice4():
    # Query user for Rack Name
    rack_name = st.number_input("Rack Name", value=None, placeholder="Type in the name of the rack...")
    st.write("Querying: ", rack_name)

    # Execute code only if the (conditional) "Submit" button is pushed
    if st.button("Submit"):

        # Retrieve the rack by name
        rack = nb.dcim.racks.get(name=rack_name)
            
        # Break if there is no entry for the provided device id
        if rack == None:
            st.write(rack_name, " does not have an entry. Please provide a valid Rack Name.")
            exit()

        st.write("Querying Devices in Rack ", rack, " ...")
        user_query = nb.dcim.devices.filter(rack_id=rack.id)
        return user_query

def print_output(user_query, user_target):
    
    with st.spinner("Compiling output from API respose..."):

        # Create a new list of the desired data from the API respose
        data = []

        if user_target == "Devices":
            for query_reply in user_query:
                data.append([str(query_reply.rack), 
                            str(query_reply.position), 
                            str(query_reply.name), 
                            str(query_reply.device_type), 
                            str(query_reply.primary_ip), 
                            str(query_reply.id), 
                            str(query_reply.url)
                            ])
        
        elif user_target == "Interfaces":
            for query_reply in user_query:
                data.append([str(query_reply.device), 
                        str(query_reply.name), 
                        str(query_reply.id), 
                        str(query_reply.url)
                        ])
        
        # Load the data into a Pandas DataFrame
        df = pd.DataFrame(data)

        # Set column headers
        if user_target == "Devices":
            df.columns = ["rack","position","name","device_type","primary_ip","id","url"]
        elif user_target == "Interfaces":
            df.columns = ["device","name","id","url"]

    # Print to Streamlit
    st.write(df)

##########################
# HELPER FUNCTIONS - END #
##########################

################
# MAIN - BEGIN #
################

def main():   
    # Some quick Streamlit Notes:
    # 1 - Execute your Streamlit code via command line: streamlit run app.py
    # 2 - Set up SSH tunnel to localhost from your terminal: ssh -L 50000:localhost:8501 <SERVER-IP>
    # 3 - In your web browser, navigate to: http://localhost:50000/

    st.title("Netbox-Toolbox")

    # Prompt the user for the information they would like to see
    choice = st.selectbox("What information would you like to see?", ["1 - All Devices",
                                                                    "2 - All Interfaces",
                                                                    "3 - Interfaces on a specifc Device",
                                                                    "4 - Devices in a specific Rack"])

    # Execute code only if the (conditional) "Start" button is pushed
    if st.button("Start"):

        if choice == "1 - All Devices":
            user_query = choice1()
            user_target = "Devices"
            print_output(user_query, user_target)

        elif choice == "2 - All Interfaces":
            user_query = choice2()
            user_target = "Interfaces"
            print_output(user_query, user_target)

        elif choice == "3 - Interfaces on a specifc Device":
            user_query = choice3()
            user_target = "Devices"
            print_output(user_query, user_target)

        elif choice == "4 - Devices in a specific Rack":
            user_query = choice4()
            user_target = "Interfaces"
            print_output(user_query, user_target)
    pass

if __name__ == "__main__":
  main()

##############
# MAIN - END #
##############
