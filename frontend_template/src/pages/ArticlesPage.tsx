import React, {useEffect, useState} from "react";
import {fetchNews} from '../services/newsService'
import '../styles/ArticlesPage.css'

interface Articles {
    title: string,
    description: string,
    url: string,
    sources?: { name: string };
}

const ArticlePage: React.FC = () => {
    const [articles, setArticles] = useState<Articles[]>([]);
    const topics = ["composting", "Green Tech", "sustainable"];

    useEffect(() => {
        const fetchArticles = async () => {
            const allArticles: Articles[] = [];

            for (const topic of topics) {
                try {
                    const articlesForTopics = await fetchNews(topic);
                    if (articlesForTopics && Array.isArray(articlesForTopics)) {
                        allArticles.push(...articlesForTopics);
                    }
                } catch (error) {
                    console.log(`Error fetching articles for topics "${topic}": `, error);
                }
            }

            setArticles(allArticles);
        };

        fetchArticles();
    }, []);

    return (
        <div className="articles-page">
            <h1>Composting & Green Tech News</h1>
            <div className="articles-list">
                {articles.length === 0 ? (
                    <p>Loading news...</p>
                ) : (
                    articles.map((article, index) => (
                        <div key={index} className="article-card">
                            <h2>{article.title}</h2>
                            <p><strong>Source:</strong> {article.sources?.name || "Unknown source"}</p>
                            <p>{article.description}</p>
                            <a href={article.url} target="_blank" rel="noopener noreferrer">
                                Read More
                            </a>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default ArticlePage;