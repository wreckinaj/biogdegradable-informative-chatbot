import React, {useState} from "react";
import '../styles/ChatInput.css'
import { AiOutlineUpload } from "react-icons/ai";

interface ChatinputProps{
    onSend: (message?: string, file?: File) => void;
}

const ChatInput: React.FC<ChatinputProps> = ({onSend}) => {
    const [input, setInput] = useState('');
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleSend = () => {
        if (selectedFile){
            onSend("", selectedFile);
            setSelectedFile(null);
        }
        else if (input.trim()) {
            onSend(input, undefined);
            setInput("");
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        // const file = e.target.files ? e.target.files[0] : null;
        const target = e.target as HTMLInputElement & {
            files: FileList;
        }
        setSelectedFile(target.files[0]);
    };

    return (
        <div className="chat-input">
            <label htmlFor="file-upload" className="upload-icon">
                <AiOutlineUpload size={24}/>
            </label>
            <input type="file" id = "file-upload" onChange={handleFileChange} style={{display: 'none'}} disabled={!!input}/>

            <input type="text" value={input} onChange={handleInputChange} placeholder="Type your message"
                   className="Prompt_box" disabled={!!selectedFile}/>
            <button onClick={handleSend} className="Prompt_send">Send</button>
        </div>
    );
};

export default ChatInput;
