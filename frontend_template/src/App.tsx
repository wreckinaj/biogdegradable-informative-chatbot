import React, {useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import ChatPage from "./pages/ChatPage";
import ArticlePage from "./pages/ArticlesPage";

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage/>}/>
                <Route path="chat" element={<ChatPage/>}/>
                <Route path="articles" element={<ArticlePage/>}/>
            </Routes>
        </Router>
    );
};

export default App;
