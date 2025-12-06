import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function ChapterTools() {
    const [isPersonalized, setIsPersonalized] = useState(false);
    const [isTranslated, setIsTranslated] = useState(false);
    const [personalizedContent, setPersonalizedContent] = useState('');
    const [translatedContent, setTranslatedContent] = useState('');
    const [loading, setLoading] = useState(''); // 'personalize' | 'translate' | ''
    const [error, setError] = useState('');
    const [userProfile, setUserProfile] = useState(null);

    useEffect(() => {
        try {
            const profile = JSON.parse(localStorage.getItem('user_profile'));
            setUserProfile(profile);
        } catch (e) {
            // ignore
        }
    }, []);

    const getContent = () => {
        const article = document.querySelector('article');
        return article ? article.innerText : '';
    };

    const handlePersonalize = async () => {
        if (!userProfile) {
            alert("Please login/configure your profile first (Top Right button).");
            return;
        }

        setLoading('personalize');
        setError('');
        const content = getContent();

        try {
            const res = await fetch('http://127.0.0.1:8000/personalize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_profile: userProfile, content: content })
            });
            const data = await res.json();
            setPersonalizedContent(data.response);
            setIsPersonalized(true);
        } catch (err) {
            setError('Failed to personalize. API error.');
            console.error(err);
        } finally {
            setLoading('');
        }
    };

    const handleTranslate = async () => {
        setLoading('translate');
        setError('');
        const content = getContent();

        try {
            const res = await fetch('http://127.0.0.1:8000/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: content, target_language: 'Urdu' })
            });
            const data = await res.json();
            setTranslatedContent(data.response);
            setIsTranslated(true);
        } catch (err) {
            setError('Failed to translate.');
            console.error(err);
        } finally {
            setLoading('');
        }
    };

    return (
        <div className={styles.toolsContainer}>
            <div className={styles.buttonGroup}>
                <button
                    onClick={handlePersonalize}
                    disabled={loading === 'personalize' || isPersonalized}
                    className={styles.toolButton}
                >
                    {loading === 'personalize' ? 'Generating...' : '✨ Personalize for Me'}
                </button>
                <button
                    onClick={handleTranslate}
                    disabled={loading === 'translate'} // Allow re-translate if needed, but simple toggle for now
                    className={styles.toolButton}
                >
                    {loading === 'translate' ? 'Translating...' : (isTranslated ? 'Show Original' : '🌐 Translate to Urdu')}
                </button>
            </div>

            {error && <div className={styles.error}>{error}</div>}

            {isPersonalized && (
                <div className={styles.personalizedBlock}>
                    <h4>🎓 Personalized for {userProfile.name}</h4>
                    <div style={{ whiteSpace: 'pre-wrap' }}>{personalizedContent}</div>
                    <button className={styles.closeButton} onClick={() => setIsPersonalized(false)}>Close</button>
                </div>
            )}

            {isTranslated && (
                <div className={styles.translatedOverlay}>
                    <div className={styles.translatedContent}>
                        <h3>📖 Urdu Translation</h3>
                        <div style={{ whiteSpace: 'pre-wrap', direction: 'rtl', fontFamily: 'Noto Nastaliq Urdu, serif', fontSize: '1.2rem' }}>
                            {translatedContent}
                        </div>
                        <button className={styles.closeButton} onClick={() => { setIsTranslated(false); setTranslatedContent('') }}>Close Translation</button>
                    </div>
                </div>
            )}
        </div>
    );
}
