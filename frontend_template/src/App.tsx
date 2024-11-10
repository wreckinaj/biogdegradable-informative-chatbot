import React, {useState} from 'react';
import './App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import ChatPage from "./pages/ChatPage";

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path = "/" element={<LandingPage/>}/>
                <Route path = "chat" element={<ChatPage/>}/>
            </Routes>
        </Router>
    );
};

export default App;
