# Description

A simple client for CSC209, written in Python + Streamlit.

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

# Understanding the code

The code is pretty much a mess. I didn't put much thought into the design of the client. I just built it quickly mainly for testing purposes.

# Limitations

Since the socket library in Python is kinda high-level, I can't seem to find a way to block the readfd. So this might not be the best tool to properly test all the functionality required in Q3 of the assignment. However, the manual send & receive feature might still be somewhat useful for testing the read/write buffer.
