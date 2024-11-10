import axios from "axios";

export const fetchNews = async (query: string) => {
    const apiKey = process.env.REACT_APP_NEWS_API_KEY;
    const url = `https://newsapi.org/v2/everything?q=${query}&apiKey=${apiKey}`;

    try {
        const response = await axios.get(url);
        console.log("API response:", response.data.articles)
        return response.data.articles || [];
    } catch (error) {
        return [];
    }
};