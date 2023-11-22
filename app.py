#! /usr/bin/env python3

__version__ = "1.0.4"
__author__ = "Kevin Brown"

import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from pynetbox import api

st.title("Netbox-Toolbox")

# Some quick Streamlit Notes:
# 1 - Execute your code via Streamlit: streamlit run app.py
# 2 - Set up SSH tunnel to localhost from your terminal: ssh -L 50000:localhost:8501 <SERVER-IP>
# 3 - In your web browser, navigate to: http://localhost:50000/

# Load environment variables from the .env file
load_dotenv()

# Read the URL and API token from the environment variables
netbox_url = os.getenv("NETBOX_API_URL")
api_token = os.getenv("NETBOX_API_TOKEN")

# Connect to the NetBox API
nb = api(url=netbox_url, token=api_token, threading=True)


# Define functions for Streamlit to use

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
    device_id = st.number_input("Device ID", value=None, step=1, placeholder="Type in a Device ID number...")
    st.write("Querying: ", device_id)

    # Execute code only if the (conditional) "Submit" button is pushed
    if st.button("Submit"):

        # Get the device name for the provided device id
        device_name = nb.dcim.devices.get(id=device_id)

        # Break if there is no entry for the provided device id
        if device_name == None:
            st.write(device_id, " does not have an entry. Please provide a valid Device ID.")
            exit()

        with st.spinner("Querying interfaces associated with Device ID ", device_id, " > > > > ", device_name, " ..."):
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

        with st.spinner("Querying Devices in Rack ", rack, " ..."):
            # API call for interfaces with a filter based on the device name
            user_query = nb.dcim.devices.filter(rack_id=rack.id)

        return user_query


# Prompt the user for the information they would like to see
choice = st.selectbox("What information would you like to see?", ["1 - All Devices",
                                                                  "2 - All Interfaces",
                                                                  "3 - Interfaces on a specifc Device",
                                                                  "4 - Devices in a specific Rack"])


# Execute code only if the (conditional) "Start" button is pushed
if st.button("Start"):

    if choice == "1 - All Devices":
        user_query = choice1()

    elif choice == "2 - All Interfaces":
        user_query = choice2()

    elif choice == "3 - Interfaces on a specifc Device":
        user_query = choice3()
        st.write(["device","name","id","url"])
        for query_reply in user_query:
            st.write([query_reply.device, query_reply.name, query_reply.id, query_reply.url])

    elif choice == "4 - Devices in a specific Rack":
        user_query = choice4()
        st.write(["rack","position","name","device_type","primary_ip","id","url"])
        for query_reply in user_query:
            st.write([query_reply.rack, query_reply.position, query_reply.name, query_reply.device_type, query_reply.primary_ip, query_reply.id, query_reply.url])

# End
