import React, { useState } from 'react';
import styles from './PersonalizeButton.module.css';

interface PersonalizeButtonProps {
    content: string;
    onPersonalize: (personalizedContent: string) => void;
}

export default function PersonalizeButton({ content, onPersonalize }: PersonalizeButtonProps) {
    const [isPersonalizing, setIsPersonalizing] = useState(false);
    const [isPersonalized, setIsPersonalized] = useState(false);

    const handlePersonalize = async () => {
        setIsPersonalizing(true);

        try {
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/personalize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: content,
                    // User profile will be fetched from session/token in backend
                }),
                credentials: 'include', // Include cookies for auth
            });

            if (!response.ok) {
                throw new Error('Personalization failed');
            }

            const data = await response.json();
            onPersonalize(data.personalized_content);
            setIsPersonalized(true);
        } catch (error) {
            console.error('Personalization error:', error);
            alert('Personalization failed. Please make sure you are logged in.');
        } finally {
            setIsPersonalizing(false);
        }
    };

    const handleReset = () => {
        setIsPersonalized(false);
        onPersonalize(''); // Clear personalization
    };

    return (
        <div className={styles.personalizeButton}>
            {!isPersonalized ? (
                <button
                    onClick={handlePersonalize}
                    disabled={isPersonalizing}
                    className={styles.button}
                >
                    {isPersonalizing ? (
                        <>
                            <span className={styles.spinner}></span>
                            Personalizing...
                        </>
                    ) : (
                        <>
                            ✨ Personalize for Me
                        </>
                    )}
                </button>
            ) : (
                <button onClick={handleReset} className={styles.resetButton}>
                    ← Show Original
                </button>
            )}
        </div>
    );
}
