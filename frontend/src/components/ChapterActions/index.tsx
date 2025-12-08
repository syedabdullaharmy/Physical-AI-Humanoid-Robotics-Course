import React, { useState } from 'react';
import PersonalizeButton from '../PersonalizeButton';
import TranslateButton from '../TranslateButton';
import styles from './ChapterActions.module.css';

interface ChapterActionsProps {
    originalContent: string;
}

export default function ChapterActions({ originalContent }: ChapterActionsProps) {
    const [displayContent, setDisplayContent] = useState(originalContent);
    const [personalizedContent, setPersonalizedContent] = useState('');
    const [translatedContent, setTranslatedContent] = useState('');

    const handlePersonalize = (content: string) => {
        if (content) {
            setPersonalizedContent(content);
            setDisplayContent(content);
        } else {
            setDisplayContent(translatedContent || originalContent);
        }
    };

    const handleTranslate = (content: string) => {
        if (content) {
            setTranslatedContent(content);
            setDisplayContent(content);
        } else {
            setDisplayContent(personalizedContent || originalContent);
        }
    };

    return (
        <div className={styles.chapterActions}>
            <div className={styles.buttonsContainer}>
                <PersonalizeButton 
                    content={originalContent}
                    onPersonalize={handlePersonalize}
                />
                <TranslateButton 
                    content={originalContent}
                    onTranslate={handleTranslate}
                />
            </div>
            
            {displayContent !== originalContent && (
                <div className={styles.contentPreview}>
                    <div 
                        className={styles.modifiedContent}
                        dangerouslySetInnerHTML={{ __html: displayContent }}
                    />
                </div>
            )}
        </div>
    );
}
