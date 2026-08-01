import streamlit as st
import requests
import streamlit.components.v1 as components


# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"


# Session state initialization
if "token" not in st.session_state:
    st.session_state.token = None

if "room_id" not in st.session_state:
    st.session_state.room_id = None

if "room_name" not in st.session_state:
    st.session_state.room_name = None

#Authorization helper
def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }

# Login / Register UI
def show_auth_page():

    st.title("📚 E-commerce & Retail Q&A Chatbot")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    # LOGIN
    with login_tab:

        st.subheader("Login")
        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button("Login"):

            response = requests.post(
                f"{API_URL}/auth/login",
                data={
                    "username": login_email,
                    "password": login_password
                }
            )


            if response.status_code == 200:

                data = response.json()
                st.session_state.token = data["access_token"]
                st.success("Login successful!")
                st.rerun()

            else:

                st.error(
                    response.json().get(
                        "detail",
                        "Login failed"
                    )
                )


    # REGISTER

    with register_tab:

        st.subheader("Create Account")

        register_username = st.text_input(
            "Username",
            key="register_username"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )


        if st.button("Register"):

            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "username": register_username,
                    "email": register_email,
                    "password": register_password
                }
            )


            if response.status_code in [200, 201]:

                st.success(
                    "Registration successful! "
                    "You can now login."
                )

            else:

                st.error(
                    response.json().get(
                        "detail",
                        "Registration failed"
                    )
                )

# Rooms Page
def show_rooms_page():

    st.title("📚 My Chat Rooms")

    # Logout
    if st.button("🚪 Logout"):
        st.session_state.token = None
        st.session_state.room_id = None
        st.session_state.room_name = None
        st.rerun()

    # Create New Room
    with st.expander("➕ Create New Room"):

        name = st.text_input(
            "Room Name",
            placeholder="Enter room name"
        )

        description = st.text_area(
            "Description",
            placeholder="Enter room description"
        )

        if st.button("Create Room"):

            response = requests.post(
                f"{API_URL}/rooms/",
                headers=get_headers(),
                json={
                    "name": name,
                    "description": description
                }
            )

            if response.status_code == 201:
                st.success("Room created successfully!")
                st.rerun()
            else:
                st.error(
                    response.json().get(
                        "detail",
                        "Failed to create room"
                    )
                )

    st.divider()
    st.subheader("Your Rooms")

    response = requests.get(
        f"{API_URL}/rooms/",
        headers=get_headers()
    )

    if response.status_code != 200:
        st.error(
            response.json().get(
                "detail",
                "Failed to load rooms"
            )
        )
        return

    rooms = response.json()

    if not rooms:
        st.info(
            "You don't have any rooms yet. "
            "Create your first room above."
        )
        return

    # 2 Rooms Per Row
    for i in range(0, len(rooms), 2):

        cols = st.columns(2)

        for col, room in zip(cols, rooms[i:i + 2]):

            with col, st.container(border=True):

                st.subheader(f"📁 {room['name']}")

                # Description
                if room.get("description"):
                    with st.expander("📄 View Description"):
                        st.write(room["description"])

                st.write("")

                # Buttons on Right Side
                empty, buttons = st.columns([1, 2])

                with buttons:

                    enter, delete = st.columns([1.4, 1.3])

                    with enter:
                        if st.button(
                            "Enter Room",
                            key=f"enter_{room['id']}",
                            use_container_width=True
                        ):
                            st.session_state.room_id = room["id"]
                            st.session_state.room_name = room["name"]
                            st.rerun()

                    with delete:
                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_{room['id']}",
                            use_container_width=True
                        ):

                            res = requests.delete(
                                f"{API_URL}/rooms/{room['id']}",
                                headers=get_headers()
                            )

                            if res.status_code == 200:
                                st.success("Room deleted!")
                                st.rerun()
                            else:
                                st.error(
                                    res.json().get(
                                        "detail",
                                        "Failed to delete room"
                                    )
                                )



# Room View
def show_room_page():

    room_id = st.session_state.room_id
    room_name = st.session_state.room_name

    st.title(f"📚 {room_name}")

    # Back to Rooms
    if st.button("⬅️ Back to Rooms"):

        st.session_state.room_id = None
        st.session_state.room_name = None

        st.rerun()


    st.divider()


    # Two Column Layout
    left_column, right_column = st.columns([1, 3])


    # LEFT SIDEBAR - FILES
    with left_column:

        # UPLOAD SECTION (expandable)
        with st.expander("📤 Upload File", expanded=False):

            # File uploader
            uploaded_file = st.file_uploader(
                "Upload a file",
                type=["pdf","docx","csv","txt","md","pptx","jpg","jpeg",
                    "png","mp3","wav","m4a","mp4","mov","avi"]
            )

            # Upload button
            if uploaded_file is not None:
                if st.button("Upload File"):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }


                    response = requests.post(
                        f"{API_URL}/upload/{room_id}",
                        headers=get_headers(),
                        files=files
                    )


                    if response.status_code == 200:
                        st.success("File uploaded successfully!")
                        st.rerun()

                    else:

                        try:
                            error_message = response.json().get(
                                "detail",
                                "File upload failed"
                            )
                        except:
                            error_message = "File upload failed"

                        st.error(error_message)


        # FILE LIST (expandable)
        with st.expander("📁 Your Files", expanded=False):

            # Get uploaded files for current room
            files_response = requests.get(f"{API_URL}/upload/{room_id}",headers=get_headers())


            if files_response.status_code == 200:
                uploaded_files = files_response.json()

                if not uploaded_files:
                    st.info("No files uploaded yet.")

                else:
                    for uploaded_file in uploaded_files:

                        filename = uploaded_file.get("filename","Unknown")
                        file_type = uploaded_file.get("file_type","Unknown")
                        file_status = uploaded_file.get("status","Unknown")

                        st.write(f"📄 **{filename}**")
                        st.write(f"Type: `{file_type}`")

                        # Status badge
                        if file_status == "ready":
                            st.success("🟢 Ready")
                        elif file_status == "processing":
                            st.warning("🟡 Processing")
                        elif file_status == "failed":
                            st.error("🔴 Failed")
                        else:
                            st.info(f"Status: {file_status}")

                        st.divider()
            else:
                try:
                    error_message = files_response.json().get("detail", "Failed to load uploaded files")

                except:
                    error_message = ("Failed to load uploaded files")

                st.error(error_message)

        st.divider()

        # CLEAR CHAT HISTORY
        if st.button("🗑️ Clear Chat History"):

            delete_response = requests.delete(
                f"{API_URL}/chat/{room_id}/history",
                headers=get_headers()
            )

            if delete_response.status_code == 200:

                st.success("Chat history deleted successfully!")
                st.rerun()

            else:

                try:
                    error_message = delete_response.json().get(
                        "detail",
                        "Failed to delete chat history"
                    )

                except:
                    error_message = "Failed to delete chat history"

                st.error(error_message)


    with right_column:
        st.subheader("💬 Chat")

        # LOAD CHAT HISTORY (messages render above the chat input)
        history_response = requests.get(
            f"{API_URL}/chat/{room_id}/history",
            headers=get_headers(),
            params={
                "skip": 0,
                "limit": 100
            }
        )

        if history_response.status_code == 200:
            history = history_response.json()

            # Display previous messages
            for message in history:
                role = message.get("role")
                content = message.get("content", "")

                if role == "user":
                    with st.chat_message("user"):
                        st.write(content)


                elif role == "assistant":
                    with st.chat_message("assistant"):
                        st.write(content)

                        # SOURCES SECTION
                        with st.expander("📚 Sources",expanded=False):
                            sources = message.get( "sources",[])

                            if sources:
                                for source in sources:
                                    filename = source.get("filename","Unknown")
                                    file_type = source.get("file_type","Unknown")
                                    chunk_index = source.get("chunk_index","Unknown")
                                    excerpt = source.get("excerpt","")

                                    st.write(
                                        f"📄 **{filename}** "
                                        f"| Type: `{file_type}` "
                                        f"| Chunk: `{chunk_index}`"
                                        f"| Excerpt: {excerpt}"
                                    )
                            else:
                                st.write("No sources found")

            # AUTO SCROLL TO BOTTOM
            if history:
                st.markdown('<div id="chat-bottom-anchor"></div>', unsafe_allow_html=True)

                components.html(
                    """
                    <script>
                        var anchor = window.parent.document.getElementById("chat-bottom-anchor");
                        if (anchor) {
                            anchor.scrollIntoView({behavior: "smooth", block: "end"});
                        }
                    </script>
                    """,
                    height=0,
                )

        else:
            st.error("Failed to load chat history.")


        # CHAT INPUT 
        query = st.chat_input("Ask a question about your documents...")

        if query:

            # SEND QUERY TO BACK
            response = requests.post(
                f"{API_URL}/chat/{room_id}",
                headers=get_headers(),
                json={
                    "query": query
                }
            )

            if response.status_code == 200:
                # Reload history from backend so the new message
                # appears above the chat input, in its normal place
                st.rerun()

            else:
                try:
                    error_message = response.json().get("detail","Chat request failed")

                except:
                    error_message = "Chat request failed"

                st.error(error_message)


# main app routing
if st.session_state.token is None:
    show_auth_page()
elif st.session_state.room_id is None:
    show_rooms_page()
else:
    show_room_page()