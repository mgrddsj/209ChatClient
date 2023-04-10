import socket
import time
import streamlit as st

def connect():
    try:
        with st.spinner("Connecting..."):
            st.session_state.get("socket").connect((addr, port))
            st.session_state.get("socket").setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,0)
            st.session_state["connected"] = True
        st.success("Connected", icon='✔')
        st.experimental_set_query_params(addr=addr, port=port)
    except Exception as e:
        st.error("Connection failed", icon='❌')
        st.error(f"Exception details: {e}")

def disconnect():
    try:
        with st.spinner("Disconnecting..."):
            st.session_state.get("socket").close()
        st.success("Connection closed. Thanks for using this client!", icon='💨')
        st.info("Refresh the page to start a new connection.", icon='🔁')
    except Exception as e:
        st.error("An error occured when closing the connection", icon='❌')
        st.error(f"Exception details: {e}")

def update_user_list():
    try:
        st.session_state.get("socket").sendall(bytes("list\n", "utf-8"))
        result = st.session_state.get("socket").recv(1163).decode("utf-8")
        if result.startswith("users:"):
            st.session_state["users"] = result[6:].split(" ")
            st.session_state.get("users").insert(0, "")
    except Exception as e:
        st.error("Failed to update user list automatically, auto update disabled", icon='😓')
        st.error(f"Exception details: {e}")
        st.session_state["auto_update"] = False

def quick_send():
    st.session_state["partial"] = ""
    action = st.session_state.get("action")
    try:
        st.session_state.get("socket").sendall(bytes(f"{action}\n", "utf-8"))
        st.session_state.get("log").append(f"> {action}\n")
        result = st.session_state.get("socket").recv(1163).decode("utf-8")
        st.session_state.get("history").append(result)
        st.session_state.get("log").append(result)
        if result.startswith("users:"):
            st.session_state["users"] = result[6:].split(" ")
            st.session_state.get("users").insert(0, "")
    except Exception as e:
        st.error("Timed out waiting for response", icon='⌛')
        st.error(f"Exception details: {e}")

def send():
    st.session_state["partial"] = ""
    try:
        st.session_state.get("socket").sendall(bytes(f"{message}\n", "utf-8"))
        st.session_state.get("log").append(f"> {message}\n")
        st.session_state["message"] = ""
        result = st.session_state.get("socket").recv(1163).decode("utf-8")
        st.session_state.get("history").append(result)
        st.session_state.get("log").append(result)
    except Exception as e:
        st.error("Timed out waiting for response", icon='⌛')
        st.error(f"Exception details: {e}")

def send_partial():
    st.session_state["partial"] = st.session_state.get("partial") + f"{message}"
    try:
        st.session_state.get("socket").sendall(bytes(f"{message}", "utf-8"))
        st.session_state.get("log").append(f"> {message} [Partial]\n")
        st.session_state["message"] = ""
        st.session_state.get("socket").settimeout(3)
        with st.spinner("Waiting for response..."):
            result = st.session_state.get("socket").recv(1163).decode("utf-8")
        st.session_state.get("history").append(result)
        st.session_state.get("log").append(result)
    except Exception as e:
        st.info("Timed out waiting for response (which should be a good sign unless connection is closed)", icon='ℹ')
        st.info(f"Socket details: {e}")
    st.session_state.get("socket").settimeout(5)

def send_wo_receive():
    st.session_state["partial"] = ""
    try:
        st.session_state.get("socket").sendall(bytes(f"{message}", "utf-8"))
        st.session_state.get("log").append(f"> {message} [Without Receive]\n")
        st.session_state["message"] = ""
    except Exception as e:
        st.error("Send failed", icon='❗')
        st.error(f"Exception details: {e}")

def manual_receive():
    try:
        manual_receive_bytes = st.session_state.get("manual_receive_bytes")
        st.session_state.get("socket").settimeout(st.session_state.get("manual_receive_timeout"))
        result = st.session_state.get("socket").recv(manual_receive_bytes).decode("utf-8")
        st.session_state.get("history").append(result)
        st.session_state.get("log").append(result)
    except Exception as e:
        st.error("Receive failed", icon='❗')
        st.error(f"Exception details: {e}")
    st.session_state.get("socket").settimeout(5)

if __name__ == "__main__":
    st.set_page_config(page_title="Chat Web Client", layout="wide")

    # Set up socket
    if "socket" not in st.session_state:
        st.session_state["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        st.session_state.get("socket").settimeout(5)

    # Set up history
    if "history" not in st.session_state: st.session_state["history"] = []
    # Set up log
    if "log" not in st.session_state: st.session_state["log"] = []
    # Set up connection status
    if "connected" not in st.session_state: st.session_state["connected"] = False
    # Set up user list
    if "message" not in st.session_state: st.session_state["message"] = ""
    # Set up partial message
    if "partial" not in st.session_state: st.session_state["partial"] = ""
    # Set up user list
    if "users" not in st.session_state: st.session_state["users"] = []
    # Set up flood test expand state
    if "flood_expand" not in st.session_state: st.session_state["flood_expand"] = False
    
    with st.sidebar:
        if not st.session_state.get("connected"):
            params = st.experimental_get_query_params()
            addr_val = params.get("addr")
            port_val = params.get("port")
            if addr_val is None:
                addr_val = "dh2010pc50.utm.utoronto.ca"
            else:
                addr_val = str(addr_val[0])
            if port_val is None:
                port_val = 1000
            else:
                port_val = int(port_val[0])
            addr = st.text_input("Server Address", value=addr_val)
            port = st.number_input("Server Port", value=port_val)
            connect_button = st.button("Connect", on_click=connect)
        else: 
            st.subheader("Quick actions")
            name = st.text_input("User name", "Arnold")
            def register_action(): st.session_state["action"] = f"register:{name}"; quick_send()
            register_button = st.button("🔑Register", on_click=register_action)
            def list_action(): st.session_state["action"] = f"list"; quick_send()
            list_button = st.button("📃List users", on_click=list_action)
            def send_message_action():
                if st.session_state.get("auto_update"):
                    update_user_list()
                st.session_state["message"] = f"message:{name}:"
            list_button = st.button("📤Send Message", on_click=send_message_action)
            def get_message_action(): st.session_state["action"] = f"getMessage"; quick_send()
            list_button = st.button("📥Get Messages", on_click=get_message_action)
            def quit_action(): st.session_state["action"] = f"quit"; quick_send(); disconnect()
            quit_button = st.button("🛑Quit", on_click=quit_action)
            with st.expander("Online user list", True):
                for i in st.session_state.get("users"):
                    if i.strip() != "":
                        st.write(f"- {i}")
                pass
            with st.expander("Client Settings"):
                st.subheader("Auto update")
                auto_get_users = st.checkbox("Automatically get users when sending message", True, key="auto_update")
                st.subheader("Recent Responses")
                response_count = st.number_input("Responses to keep in \"Recent Responses\"", value=10)
                st.write("Note: full message logs can be viewed in the \"Raw Logs\" tab")
                st.subheader("Clear history")
                def clear_logs(): 
                    st.session_state["history"] = []
                    st.session_state["log"] = []
                st.button("Clear responses & logs", on_click=clear_logs, use_container_width=True)
                st.subheader("Flood test wait time")
                st.number_input("Flood test spawn wait time", value=0.05, key="flood_wait_time")
            with st.expander("Manual Send & Receive Options"):
                st.subheader("Manual receive")
                st.number_input("Number of bytes to receive for manual receive", value=5, key="manual_receive_bytes")
                st.number_input("Manual receive timeout (seconds)", value=5, key="manual_receive_timeout")

    if not st.session_state.get("connected"):
        st.title("CSC209 Chat Client")
        st.write("Hi! Welcome to the chat client. 😊")
        st.write("👈Please set up your server on the left.")
        st.write("Please remember to use \"quit\" when possible, or the connection may not close for a long time.")
        st.write("If you encounter any error, simply refresh the page.🔁")
    else:
        main_content = st.empty()

        history_tab, log_tab = st.tabs(["Recent Responses", "Raw Logs"])

        with history_tab:
            history_container = st.container()

            while (len(st.session_state.get("history")) > response_count):
                st.session_state.get("history").pop(0)

            for item in st.session_state.get("history"):
                history_container.text(item)
            
        with log_tab:
            logs_text = ""
            
            for item in st.session_state.get("log"):
                logs_text += item

            logs_container = st.code(logs_text, None)

        if st.session_state.get("partial") != "":
            partial = st.session_state.get("partial")
            st.code(f"Current partial input: {partial}", None)

        if st.session_state.get("message").startswith(f"message:{name}:"):
            user_dropdown_placeholder, message_placeholder = st.columns([1,8])
            def select_user():
                msg_parts = st.session_state.get("message").split(":")
                msg_parts[2] = st.session_state.get("user_selected")
                if msg_parts[2].strip() != "" and len(msg_parts) == 3: msg_parts.append("")
                if msg_parts[2].strip() == "" and len(msg_parts) == 4: msg_parts.pop(3)
                st.session_state["message"] = ":".join(msg_parts)
            user_dropdown_placeholder.selectbox("To User", st.session_state.get("users"), key="user_selected", on_change=select_user)
        else:
            message_placeholder = st.empty()
        message = message_placeholder.text_area("Enter your message here", key="message")

        clear_button_col, send_partial_button_col, send_button_col = st.columns(3)
        with clear_button_col:
            def clear_input(): st.session_state["message"] = ""
            clear_button = st.button("Clear input", on_click=clear_input, use_container_width=True)
        with send_partial_button_col:
            send_partial_button = st.button("Send Partial", on_click=send_partial, use_container_width=True)
        with send_button_col:
            send_button = st.button("**Send** (with \\n)", on_click=send, use_container_width=True)

        with st.expander("Manual Send & Receive (Q3 Tools) (Raw Logs view recommended)", expanded=True):
            manual_recv_button_col, send_wo_recv_button_col = st.columns(2)
            with manual_recv_button_col:
                manual_receive_bytes = st.session_state.get("manual_receive_bytes")
                st.button(f"Manually receive {manual_receive_bytes} bytes", on_click=manual_receive, use_container_width=True)
            with send_wo_recv_button_col:
                st.button(f"Send without receive (without \\n)", on_click=send_wo_receive, use_container_width=True)
            st.caption("Try sending multiple messages without receiving, then receive them all at once?")
            st.caption("(Due to Python socket limitations, it seems like I cannot mimic the readfd of the client not being ready. So the OS buffer may have effected the results.)")

        with st.expander("Flood Test", expanded=st.session_state.get("flood_expand")):
            st.write("This section allows you to spawn a lot of dummy clients (aside from the main one connected).")
            st.write("It will spawn dummies until it can't anymore. In normal circumstances, it should be able to spawn 31 clients, then stop.")

            # Set up dummy list
            if "dummies" not in st.session_state: st.session_state["dummies"] = []
            # Set up dummy logs
            if "dummy_log" not in st.session_state: st.session_state["dummy_log"] = "Logs:\n"

            status = st.empty()
            status.metric("Dummy count", len(st.session_state.get("dummies")))

            def spawn():
                failed = False
                st.session_state["dummy_log"] = "Logs:\n"
                st.session_state["flood_expand"] = True
                params = st.experimental_get_query_params()
                addr_val = params.get("addr")
                port_val = params.get("port")
                addr_val = str(addr_val[0])
                port_val = int(port_val[0])
                spawn_placeholder = st.empty()
                dummy_realtime_log_placeholder = spawn_placeholder.container()
                while not failed:
                    try:
                        dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        num = len(st.session_state.get("dummies")) + 1
                        with st.spinner("Connecting..."):
                            st.session_state.get("dummies").append(dummy)
                            dummy.connect((addr_val, port_val))
                            dummy.sendall(bytes(f"register:dummy{num}\n", "utf-8"))
                            result = dummy.recv(1163).decode("utf-8")
                        st.session_state["dummy_log"] = st.session_state.get("dummy_log") + f"Dummy{num} connected and register message send. Got this back: {result}\n"
                        dummy_realtime_log_placeholder.write(f"Dummy{num} connected and register message send. Got this back: {result}")
                        if result == "":
                            dummy_realtime_log_placeholder.write(f"It seems like dummy {num} cannot get a \"registered\" message. Removing & stopping.")
                            st.session_state["dummy_log"] = st.session_state.get("dummy_log") + f"It seems like dummy {num} cannot get a \"registered\" message. Removing & stopping."
                            st.session_state.get("dummies").pop()
                            failed = True
                        time.sleep(st.session_state.get("flood_wait_time"))
                    except Exception as e:
                        st.error("Connection failed. (Don't worry, this might be normal as the server rejects a connection.)", icon='😥')
                        st.error(f"Exception details: {e}")
                        st.session_state.get("dummies").pop()
                        failed = True
                spawn_placeholder.empty()

            def quit_all():
                count = len(st.session_state.get("dummies"))
                close_count_placeholder = st.empty()
                st.session_state["dummy_log"] = "Logs:\n"
                st.session_state["flood_expand"] = True
                while st.session_state.get("dummies"):
                    dummy = st.session_state.get("dummies").pop(0)
                    try:
                        dummy.sendall(bytes(f"quit\n", "utf-8"))
                        result = dummy.recv(1163).decode("utf-8")
                        st.session_state["dummy_log"] = st.session_state.get("dummy_log") + f"On count = {count}, got {result}"
                        if ("closing" in result):
                            dummy.close()
                        count -= 1
                        close_count_placeholder.metric("Remaining clients", value=count)
                        time.sleep(st.session_state.get("flood_wait_time"))
                    except Exception as e:
                        st.error("An error occured when closing a connection. (It might just be a problem with my janky code.)", icon='🤔')
                        st.error(f"Exception details: {e}")
                        failed = True
                close_count_placeholder.empty()

            spawn_button = st.button("Spawn and register", on_click=spawn)
            quit_all_button = st.button("Quit all", on_click=quit_all)

            st.text(st.session_state.get("dummy_log"))
