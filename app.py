import streamlit as st

from src.agent import handle_customer_query


st.set_page_config(
    page_title="NovaTech AI Support",
    page_icon="🤖",
    layout="centered",
)


st.title("🤖 NovaTech AI Customer Support")

st.caption(
    "AI-powered customer support with RAG, agentic tools, "
    "and human escalation."
)


# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display support information for assistant messages
        if message["role"] == "assistant":

            with st.expander("Support Details"):

                st.write(
                    f"**Intent:** {message['intent']}"
                )

                st.write(
                    f"**Confidence:** "
                    f"{message['confidence']:.2f}"
                )

                st.write(
                    f"**Escalated:** "
                    f"{message['escalated']}"
                )

                if message["action"]:
                    st.write("**Agent Action:**")
                    st.json(message["action"])


# Customer input
query = st.chat_input(
    "Ask NovaTech Support something..."
)


if query:

    # Display and save customer message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    # Process customer query
    with st.chat_message("assistant"):

        with st.spinner(
            "NovaTech Support is thinking..."
        ):

            try:

                result = handle_customer_query(
                    query
                )

                response = result["response"]

                st.markdown(response)

                # Display support information immediately
                with st.expander("Support Details"):

                    st.write(
                        f"**Intent:** "
                        f"{result['intent']}"
                    )

                    st.write(
                        f"**Confidence:** "
                        f"{result['confidence']:.2f}"
                    )

                    st.write(
                        f"**Escalated:** "
                        f"{result['escalated']}"
                    )

                    if result["action"]:

                        st.write(
                            "**Agent Action:**"
                        )

                        st.json(
                            result["action"]
                        )

                # Save complete assistant message
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "intent": result["intent"],
                        "confidence": result["confidence"],
                        "escalated": result["escalated"],
                        "action": result["action"],
                    }
                )

            except Exception as exc:

                error_message = (
                    f"An error occurred: {exc}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "intent": "error",
                        "confidence": 0.0,
                        "escalated": False,
                        "action": None,
                    }
                )