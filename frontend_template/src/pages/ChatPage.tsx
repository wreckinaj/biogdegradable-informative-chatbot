import React, {useState} from "react";
import {ChatMessage as ChatMessageType} from "../types/Chat";
import ChatInput from "../components/ChatInput";
import ChatMessage from "../components/ChatMessage";
import '../styles/ChatPage.css'
import axios from "axios";

const ChatPage: React.FC = () => {
    const [message, setMessage] = useState<ChatMessageType[]>([]);

    const sendMessage = async (text: string) => {
        const userMessage: ChatMessageType = {sender: "user", text};
        setMessage((prevMessage) => [...prevMessage, userMessage]);
        console.log(userMessage)

        try {
            const response = await axios.post("https://localhost:3000/chat", {message: text})
            const botMessage: ChatMessageType = {sender: "bot", text: response.data.reply};
            setMessage((prevMessage) => [...prevMessage, botMessage]);
        } catch (error) {
            console.error("Error handling message: ", error);
            setMessage((prevMessage) => [...prevMessage, {sender: "bot", text: "Sorry, something went wrong. "}]);
        }
    };

    return (
        <div className="chat-page">
            <div className="chat-page-messages">
                {message.map((msg, index) => (<ChatMessage key={index} message={msg}/>))}
            </div>
            <ChatInput onSend={sendMessage}/>
        </div>
    );
};

export default ChatPage;