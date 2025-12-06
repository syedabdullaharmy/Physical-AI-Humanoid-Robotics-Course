import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

export default function ChatWidget() {
    const { siteConfig } = useDocusaurusContext();
    const API_URL = siteConfig.customFields?.REACT_APP_API_URL || 'http://127.0.0.1:8000';

    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [selectedText, setSelectedText] = useState('');
    const [connectionStatus, setConnectionStatus] = useState('unknown'); // 'unknown', 'connected', 'disconnected'
    const [retryCount, setRetryCount] = useState(0);
    const messagesEndRef = useRef(null);

    // Load chat history from localStorage
    useEffect(() => {
        const savedMessages = localStorage.getItem('chatHistory');
        if (savedMessages) {
            try {
                setMessages(JSON.parse(savedMessages));
            } catch (e) {
                console.error('Failed to load chat history:', e);
            }
        }
    }, []);

    // Save chat history to localStorage
    useEffect(() => {
        if (messages.length > 0) {
            localStorage.setItem('chatHistory', JSON.stringify(messages));
        }
    }, [messages]);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Handle text selection
    useEffect(() => {
        const handleMouseUp = () => {
            const text = window.getSelection().toString().trim();
            if (text && text.length > 3) {
                setSelectedText(text);
            }
        };
        document.addEventListener('mouseup', handleMouseUp);
        return () => document.removeEventListener('mouseup', handleMouseUp);
    }, []);

    // Check backend health on mount
    useEffect(() => {
        checkBackendHealth();
    }, []);

    const checkBackendHealth = async () => {
        try {
            const response = await fetch(`${API_URL}/health`, {
                method: 'GET',
                signal: AbortSignal.timeout(5000) // 5 second timeout
            });

            if (response.ok) {
                setConnectionStatus('connected');
            } else {
                setConnectionStatus('disconnected');
            }
        } catch (error) {
            setConnectionStatus('disconnected');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = {
            role: 'user',
            content: input,
            context: selectedText,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // Retry logic with exponential backoff
        const maxRetries = 3;
        let lastError = null;

        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: userMessage.content,
                        context: userMessage.context
                    }),
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                setMessages(prev => [...prev, {
                    role: 'bot',
                    content: data.response,
                    timestamp: new Date().toISOString()
                }]);

                setConnectionStatus('connected');
                setRetryCount(0);
                setIsLoading(false);
                setSelectedText('');
                return; // Success, exit the retry loop

            } catch (error) {
                lastError = error;
                console.error(`Chat error (attempt ${attempt + 1}/${maxRetries}):`, error);

                if (attempt < maxRetries - 1) {
                    // Wait before retrying (exponential backoff)
                    const delay = Math.min(1000 * Math.pow(2, attempt), 5000);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }

        // All retries failed
        setConnectionStatus('disconnected');
        setRetryCount(prev => prev + 1);
        setIsLoading(false);

        let errorMessage = "I'm having trouble connecting to the AI service. ";

        if (lastError.name === 'AbortError') {
            errorMessage += "The request timed out. Please try again with a shorter question.";
        } else if (lastError.message.includes('Failed to fetch')) {
            errorMessage += "Please make sure the backend server is running at " +
                API_URL +
                ". You can start it with: cd backend && uvicorn main:app --reload";
        } else {
            errorMessage += "Please try again later or check the console for details.";
        }

        setMessages(prev => [...prev, {
            role: 'bot',
            content: errorMessage,
            isError: true,
            timestamp: new Date().toISOString()
        }]);

        setSelectedText('');
    };

    const clearHistory = () => {
        if (window.confirm('Are you sure you want to clear the chat history?')) {
            setMessages([]);
            localStorage.removeItem('chatHistory');
        }
    };

    const getConnectionStatusIcon = () => {
        switch (connectionStatus) {
            case 'connected':
                return '🟢';
            case 'disconnected':
                return '🔴';
            default:
                return '🟡';
        }
    };

    return (
        <div className={clsx(styles.chatWidget, { [styles.open]: isOpen })}>
            {!isOpen && (
                <button className={styles.toggleButton} onClick={() => setIsOpen(true)}>
                    🤖 Ask AI {getConnectionStatusIcon()}
                </button>
            )}

            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.header}>
                        <div>
                            <h3>AI Tutor {getConnectionStatusIcon()}</h3>
                            <small style={{ fontSize: '0.7rem', opacity: 0.9 }}>
                                {connectionStatus === 'connected' ? 'Connected' :
                                    connectionStatus === 'disconnected' ? 'Disconnected' : 'Checking...'}
                            </small>
                        </div>
                        <div>
                            {messages.length > 0 && (
                                <button
                                    onClick={clearHistory}
                                    style={{ marginRight: '10px', fontSize: '0.9rem' }}
                                    title="Clear chat history"
                                >
                                    🗑️
                                </button>
                            )}
                            <button onClick={() => setIsOpen(false)}>✖</button>
                        </div>
                    </div>

                    <div className={styles.messages}>
                        {messages.length === 0 && (
                            <div className={styles.welcomeMessage}>
                                👋 Hi! I'm your AI tutor for Physical AI & Humanoid Robotics.
                                Ask me anything about the course material!
                                <br /><br />
                                💡 <strong>Tip:</strong> Select text on the page and ask me about it for context-aware answers.
                            </div>
                        )}
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={clsx(
                                    styles.message,
                                    styles[msg.role],
                                    { [styles.errorMessage]: msg.isError }
                                )}
                            >
                                <div className={styles.messageContent}>{msg.content}</div>
                                {msg.context && (
                                    <div className={styles.contextQuote}>
                                        📌 Context: "{msg.context.substring(0, 100)}{msg.context.length > 100 ? '...' : ''}"
                                    </div>
                                )}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={styles.loading}>
                                <div className={styles.typingIndicator}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                                Thinking...
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {selectedText && (
                        <div className={styles.selectionPreview}>
                            <span>📌 Selected: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"</span>
                            <button onClick={() => setSelectedText('')}>✖</button>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className={styles.inputArea}>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder={connectionStatus === 'connected' ? "Ask a question..." : "Backend disconnected..."}
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading || !input.trim()}>
                            {isLoading ? '⏳' : '📤'}
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
}
