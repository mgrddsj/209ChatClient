# Description

A simple client for CSC209, written in Python + Streamlit.

# Live Demo

Simply head to [209client.jessexu.me](https://209client.jessexu.me/). It's a live instance running on dh2010pc47, connections will be instantiated on that PC. It should be able to connect to any server hosted on the UTM CS Lab machines.

# Running Instructions

Simply install streamlit with pip:

```
pip install streamlit
```

Then, run the file with streamlit:

```
streamlit run chat_client_web.py
```

or, if you want to specify a port:

```
streamlit run chat_client_web.py --server.port 8080
```

# Functionality

The client has some basic functionalities such as sending and receiving messages. It also provides a easy way to send messages to existing users (from `list`), as well as functions that allows sending partial messages. It also has some tools for debugging Q2 and Q3 such as flood test and manual send/receive.

# Limitations

Since the socket library in Python is kinda high-level, I can't seem to find a way to block the readfd. So this might not be the best tool to properly test all the functionality required in Q3 of the assignment (i.e. blocking writes). However, the manual send & receive feature might still be somewhat useful for testing the read/write buffer.

# Other Notes

The code is pretty much a mess. I didn't put much thought into the design of the client. I just built it quickly mainly for testing purposes. But streamlit is pretty straight-forward, it shouldn't be too hard to understand what the code is doing here.

# Video Demo



https://user-images.githubusercontent.com/36990144/231008716-a7443693-c41f-490b-8259-bf7cb42b73b6.mp4

