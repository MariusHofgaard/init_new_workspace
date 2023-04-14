import json

import requests
import streamlit as st


def delete_session(keys=[]):
    if keys == []:
        keys = st.session_state.keys()

    for key in keys:
        del st.session_state[key]


if "name" in st.session_state and st.session_state["name"] == "":
    delete_session(["name"])

if "logo_url" in st.session_state and st.session_state["logo_url"] == "":
    delete_session(["logo_url"])

if "users" in st.session_state and st.session_state["users"] == "":
    delete_session(["users"])


if "name" in st.session_state:
    st.write("The current workspace name is:")
    st.subheader(st.session_state["name"])

if "logo_url" in st.session_state:
    st.write("The logo is:")
    try:
        st.image(
            st.session_state["logo_url"],
            width=100,  # Manually Adjust the width of the image as per requirement
        )
    except:
        delete_session(["logo_url"])
        st.error("Not able to open image")


if "name" not in st.session_state:
    workspace_name = st.text_input("Workspace Name")
    st.session_state["name"] = workspace_name

if "logo_url" not in st.session_state:
    workspace_logo_url = st.text_input("Workspace Logo URL")
    st.session_state["logo_url"] = workspace_logo_url


applicable_users = {
    "Marius": "cY5BQ8eiZnevbysjzW7jXzw0wc52",
    "Fredrik": "wL1RFhYkBEaIYtY6jp3vYkgM1h32",
    "Alessandro": "6hmId4Xu21fr6bsxzLPIb1UVNaz1",
    "Vegard": "vWNMj8K2hlhErc3u57MxfEyKo3o2",
    "Harald": "1wJkEo4VOTMBH0XvBegvnFhecx62",
}

options = st.multiselect("Which users should have access", applicable_users.keys())

list_of_uid = []
for option in options:
    # get the uid

    list_of_uid.append(applicable_users[option])
st.session_state["users"] = list_of_uid


# Define the URL to send the post request to
url = "https://europe-west1-enernite-gis.cloudfunctions.net/createFredrikNewWorkspace"


if "name" in st.session_state and "logo_url" in st.session_state:
    # Define the body of the post request
    body = {
        "name": st.session_state["name"],
        "users_with_access": list_of_uid,
        "photo_url": st.session_state["logo_url"],
    }
    # Add a button to the Streamlit app
    if st.button("Activate workspace"):
        # Send the post request when the button is clicked
        response = requests.post(url, json=body)
        if response.status_code == 200:
            st.success("Workspace Created")

            st.write("The workspace ID is: ", json.loads(response.text)["workspace_id"])
        else:
            st.error("Error sending post request.")


def reset_session_state():
    st.session_state.clear()


if st.button("Reset"):
    reset_session_state()
