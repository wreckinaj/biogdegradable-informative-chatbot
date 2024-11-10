import React from "react";
import {Link} from "react-router-dom";
import '../styles/LandingPage.css'

const LandingPage: React.FC = () => {
    return (
        <div className="landing-page">
            <h1> Welcome to the Chatbot </h1>
            <Link to="/chat">
                <button>Start Chatting</button>
            </Link>
        </div>
    );
};

export default LandingPage;
