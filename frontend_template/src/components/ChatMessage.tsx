import React from "react";
import {ChatMessage as ChatMessageTypes} from "../types/Chat";
import '../styles/ChatMessage.css'

interface ChatMessageProps {
    message: ChatMessageTypes;
}

const ChatMessage: React.FC<ChatMessageProps> = ({message}) => {
    return (
        <div className={`chat-message ${message.sender === 'user' ? 'chat-message-user' : 'chat-message-bot'}`}>
            <div className={`message-bubble ${message.sender}`}>
                {message.content}
            </div>
        </div>
    )
}

export default ChatMessage;