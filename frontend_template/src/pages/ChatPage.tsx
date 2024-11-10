// npm i -D @types/react to run react npm env
import React, {useState} from "react";
import {ChatMessage as ChatMessageType} from "../types/Chat";
import ChatInput from "../components/ChatInput";
import ChatMessage from "../components/ChatMessage";
import '../styles/ChatPage.css'
import axios from "axios";
import {Form} from "react-router-dom";

const ChatPage: React.FC = () => {
    const [chatHistory, setChatHistory] = useState<ChatMessageType[]>([]);

    const sendMessage = async (textMessage?: string, file?: File) => {
        if (textMessage) {
            const userTextMessage: ChatMessageType = {sender: "user", content: textMessage};
            setChatHistory((chatHistory) => [...chatHistory, userTextMessage]);
            console.log("User message:", userTextMessage);

            try {
                const response = await axios.post("https://localhost:3000/chat", {message: textMessage});
                const botReplyMessage: ChatMessageType = {sender: "bot", content: response.data.reply};
                setChatHistory((prevMessage) => [...prevMessage, botReplyMessage]);
            } catch (error) {
                console.error("Error handling message: ", error);
                setChatHistory((prevMessage) => [...prevMessage, {
                    sender: "bot",
                    content: "Sorry, something went wrong. "
                }]);
            }

        } else if (file) {
            const userFileMessage: ChatMessageType = {sender: "user", content: "Uploading image of item for classification"};
            setChatHistory((prevHistory) => [...prevHistory, userFileMessage]);
            console.log("Upload file: " + file.name);

            try {
                const formData = new FormData();
                formData.append("file", file);
                const response = await axios.post("https://localhost:3000/chat", formData, {
                    headers: { "Content-Type": "multipart/form-data" }
                });

                const classificationType: string = "biodegradable";
                setChatHistory((prevHistory) => [...prevHistory, {
                    sender: "bot",
                    content: `Your item is ${classificationType}.`}]);
            }catch(error){
                console.error("Error uploading file: " + error);
                setChatHistory((prevHistory) => [
                    ...prevHistory,
                    { sender: "bot", content: "Sorry, there was an error classifying the file." }]);
            }
        }
    };

    return (
        <div className="chat-page">
            <div className="chat-page-messages">
                {chatHistory.map((msg, index) => (<ChatMessage key={index} message={msg}/>))}
            </div>
            <ChatInput onSend={sendMessage}/>
        </div>
    );
};

export default ChatPage;

