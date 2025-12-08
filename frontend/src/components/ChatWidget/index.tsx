import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatWidget.module.css';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    citations?: Array<{
        source_number: number;
        module: string;
        chapter: string;
        score: number;
    }>;
}

interface ErrorState {
    message: string;
    retryable: boolean;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const STORAGE_KEY = 'physicalai_chat_history';
const MAX_STORED_MESSAGES = 50;

const SUGGESTED_QUESTIONS = [
    "What is ROS 2 and why is it important for robotics?",
    "Explain the concept of Digital Twins in robotics",
    "How do Vision-Language-Action models work?",
    "What are the key components of a humanoid robot?",
    "How do I set up NVIDIA Isaac Sim?"
];

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<ErrorState | null>(null);
    const [showSuggestions, setShowSuggestions] = useState(true);
    const [copyFeedback, setCopyFeedback] = useState<number | null>(null);
    const [selectedText, setSelectedText] = useState<string>('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Text selection handler
    useEffect(() => {
        const handleTextSelection = () => {
            const selection = window.getSelection();
            const text = selection?.toString().trim();
            if (text && text.length > 10) { // Minimum 10 characters
                setSelectedText(text);
                setIsOpen(true); // Auto-open chat
            }
        };

        document.addEventListener('mouseup', handleTextSelection);
        document.addEventListener('touchend', handleTextSelection);

        return () => {
            document.removeEventListener('mouseup', handleTextSelection);
            document.removeEventListener('touchend', handleTextSelection);
        };
    }, []);

    // Load chat history from localStorage on mount
    useEffect(() => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                const parsed = JSON.parse(stored);
                setMessages(parsed.slice(-MAX_STORED_MESSAGES));
                if (parsed.length > 0) {
                    setShowSuggestions(false);
                }
            }
        } catch (e) {
            console.error('Failed to load chat history:', e);
        }
    }, []);

    // Save chat history to localStorage when messages change
    useEffect(() => {
        if (messages.length > 0) {
            try {
                localStorage.setItem(
                    STORAGE_KEY,
                    JSON.stringify(messages.slice(-MAX_STORED_MESSAGES))
                );
            } catch (e) {
                console.error('Failed to save chat history:', e);
            }
        }
    }, [messages]);

    const clearHistory = () => {
        setMessages([]);
        localStorage.removeItem(STORAGE_KEY);
        setShowSuggestions(true);
        setError(null);
    };

    const sendMessage = async (messageText?: string, retryCount = 0) => {
        const textToSend = messageText || input;
        if (!textToSend.trim() || isLoading) return;

        const userMessage: Message = {
            role: 'user',
            content: textToSend,
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        setError(null);
        setShowSuggestions(false);

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout

            const response = await fetch(`${API_URL}/api/chat/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: textToSend,
                    chat_history: messages.slice(-6), // Last 3 exchanges
                }),
                signal: controller.signal,
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                if (response.status >= 500) {
                    throw new Error('SERVER_ERROR');
                } else if (response.status === 429) {
                    throw new Error('RATE_LIMIT');
                }
                throw new Error('REQUEST_FAILED');
            }

            const data = await response.json();

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.answer,
                citations: data.citations,
            };

            setMessages((prev) => [...prev, assistantMessage]);
            setError(null);
        } catch (err: any) {
            console.error('Chat error:', err);

            let errorMessage = 'Sorry, something went wrong. Please try again.';
            let retryable = true;

            if (err.name === 'AbortError') {
                errorMessage = '⏱️ Request timed out. The server took too long to respond.';
            } else if (err.message === 'SERVER_ERROR') {
                errorMessage = '🔧 Server is experiencing issues. Please try again later.';
            } else if (err.message === 'RATE_LIMIT') {
                errorMessage = '⚠️ Too many requests. Please wait a moment before trying again.';
                retryable = false;
            } else if (err.name === 'TypeError' || err.message.includes('fetch')) {
                errorMessage = '🔌 Cannot connect to AI service. Please check your connection.';

                // Auto-retry once for network errors
                if (retryCount === 0) {
                    setTimeout(() => sendMessage(textToSend, 1), 2000);
                    setError({ message: '🔄 Connection failed, retrying...', retryable: false });
                    return;
                }
            }

            setError({ message: errorMessage, retryable });
        } finally {
            setIsLoading(false);
        }
    };

    const handleSuggestionClick = (question: string) => {
        setInput(question);
        sendMessage(question);
    };

    const copyMessage = async (content: string, index: number) => {
        try {
            await navigator.clipboard.writeText(content);
            setCopyFeedback(index);
            setTimeout(() => setCopyFeedback(null), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    const getCitationPath = (module: string, chapter: string): string => {
        // Convert module and chapter to URL-friendly format
        const moduleSlug = module.toLowerCase().replace(/\s+/g, '-');
        const chapterSlug = chapter.toLowerCase().replace(/\s+/g, '-');
        return `/docs/${moduleSlug}/${chapterSlug}`;
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <>
            {/* Chat Button */}
            {!isOpen && (
                <button
                    className={styles.chatButton}
                    onClick={() => setIsOpen(true)}
                    aria-label="Open chat"
                >
                    <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                    >
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                </button>
            )}

            {/* Chat Panel */}
            {isOpen && (
                <div className={styles.chatPanel}>
                    {/* Header */}
                    <div className={styles.chatHeader}>
                        <h3>AI Assistant</h3>
                        <div className={styles.chatHeaderActions}>
                            {messages.length > 0 && (
                                <button
                                    className={styles.clearHistoryButton}
                                    onClick={clearHistory}
                                    aria-label="Clear history"
                                >
                                    Clear History
                                </button>
                            )}
                            <button
                                className={styles.closeButton}
                                onClick={() => setIsOpen(false)}
                                aria-label="Close chat"
                            >
                                ×
                            </button>
                        </div>
                    </div>

                    {/* Error Banner */}
                    {error && (
                        <div className={styles.errorBanner}>
                            <span>{error.message}</span>
                            {error.retryable && (
                                <button onClick={() => sendMessage(messages[messages.length - 2]?.content)}>
                                    Retry
                                </button>
                            )}
                        </div>
                    )}

                    {/* Messages */}
                    <div className={styles.chatMessages}>
                        {messages.length === 0 && (
                            <div className={styles.welcomeMessage}>
                                <p>👋 Hi! I'm your AI assistant for this textbook.</p>
                                <p>Ask me anything about Physical AI, ROS 2, or humanoid robotics!</p>
                                <p className={styles.tip}>
                                    💡 Tip: Try one of the suggested questions below!
                                </p>

                                {showSuggestions && (
                                    <div className={styles.suggestedQuestions}>
                                        {SUGGESTED_QUESTIONS.map((question, index) => (
                                            <button
                                                key={index}
                                                className={styles.suggestedQuestion}
                                                onClick={() => handleSuggestionClick(question)}
                                            >
                                                {question}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`${styles.message} ${message.role === 'user' ? styles.userMessage : styles.assistantMessage
                                    }`}
                            >
                                <div className={styles.messageContent}>
                                    {message.content}
                                </div>

                                {/* Message Actions */}
                                {message.role === 'assistant' && (
                                    <div className={styles.messageActions}>
                                        <button
                                            className={styles.messageAction}
                                            onClick={() => copyMessage(message.content, index)}
                                            aria-label="Copy message"
                                        >
                                            {copyFeedback === index ? '✓ Copied' : '📋 Copy'}
                                        </button>
                                    </div>
                                )}

                                {/* Citations with clickable links */}
                                {message.citations && message.citations.length > 0 && (
                                    <div className={styles.citations}>
                                        <strong>Sources:</strong>
                                        <div>
                                            {message.citations.map((citation, i) => (
                                                <a
                                                    key={i}
                                                    href={getCitationPath(citation.module, citation.chapter)}
                                                    className={styles.citation}
                                                    title={`${citation.module} - ${citation.chapter} (relevance: ${(citation.score * 100).toFixed(0)}%)`}
                                                >
                                                    [{citation.source_number}] {citation.module} - {citation.chapter}
                                                    <svg
                                                        className={styles.externalLinkIcon}
                                                        viewBox="0 0 12 12"
                                                        fill="none"
                                                        stroke="currentColor"
                                                        strokeWidth="2"
                                                    >
                                                        <path d="M10 6v3a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h3M7 2h3v3M10 2L5 7" />
                                                    </svg>
                                                </a>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}

                        {isLoading && (
                            <div className={`${styles.message} ${styles.assistantMessage}`}>
                                <div className={styles.typing}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className={styles.chatInput}>
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask a question..."
                            rows={2}
                            disabled={isLoading}
                        />
                        <button
                            onClick={() => sendMessage()}
                            disabled={!input.trim() || isLoading}
                            aria-label="Send message"
                        >
                            <svg
                                width="20"
                                height="20"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <line x1="22" y1="2" x2="11" y2="13" />
                                <polygon points="22 2 15 22 11 13 2 9 22 2" />
                            </svg>
                        </button>
                    </div>
                </div>
            )}
        </>
    );
}
