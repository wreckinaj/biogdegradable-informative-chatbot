import React, {useState} from "react";
import '../styles/ChatInput.css'

interface ChatinputProps{
    onSend: (message: string) => void;
}

const ChatInput: React.FC<ChatinputProps> = ({onSend}) => {
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (input.trim()) {
            onSend(input);
            setInput('');
        }
    };

    return (
        <div className="chat-input">
            <input type="text" value = {input} onChange={ (e) => setInput(e.target.value)} placeholder="Type your message" className="Prompt_box"/>
            <button onClick={handleSend} className="Prompt_send">Send</button>
        </div>
    );
};

export default ChatInput;
