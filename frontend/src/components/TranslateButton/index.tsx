import React, { useState } from 'react';
import styles from './TranslateButton.module.css';

interface TranslateButtonProps {
    content: string;
    onTranslate: (translatedContent: string) => void;
}

export default function TranslateButton({ content, onTranslate }: TranslateButtonProps) {
    const [isTranslating, setIsTranslating] = useState(false);
    const [isTranslated, setIsTranslated] = useState(false);

    const handleTranslate = async () => {
        setIsTranslating(true);

        try {
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/translate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    target_language: 'urdu',
                }),
            });

            if (!response.ok) {
                throw new Error('Translation failed');
            }

            const data = await response.json();
            onTranslate(data.translated_content);
            setIsTranslated(true);
        } catch (error) {
            console.error('Translation error:', error);
            alert('Translation failed. Please try again.');
        } finally {
            setIsTranslating(false);
        }
    };

    const handleReset = () => {
        setIsTranslated(false);
        onTranslate(''); // Clear translation
    };

    return (
        <div className={styles.translateButton}>
            {!isTranslated ? (
                <button
                    onClick={handleTranslate}
                    disabled={isTranslating}
                    className={styles.button}
                >
                    {isTranslating ? (
                        <>
                            <span className={styles.spinner}></span>
                            Translating...
                        </>
                    ) : (
                        <>
                            🌐 Translate to Urdu
                        </>
                    )}
                </button>
            ) : (
                <button onClick={handleReset} className={styles.resetButton}>
                    ← Back to English
                </button>
            )}
        </div>
    );
}
