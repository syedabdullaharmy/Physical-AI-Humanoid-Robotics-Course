import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function AuthModal() {
    const [isOpen, setIsOpen] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const [formData, setFormData] = useState({
        name: '',
        softwareBg: '',
        hardwareBg: ''
    });

    useEffect(() => {
        try {
            const userStr = localStorage.getItem('user_profile');
            if (userStr) {
                const user = JSON.parse(userStr);
                setFormData(user);
                setIsLoggedIn(true);
            }
        } catch (e) {
            console.error("Auth init error", e);
        }
    }, []);

    const handleLogin = (e) => {
        e.preventDefault();
        localStorage.setItem('user_profile', JSON.stringify(formData));
        setIsLoggedIn(true);
        setIsOpen(false);
        window.location.reload();
    };

    const handleLogout = () => {
        localStorage.removeItem('user_profile');
        setIsLoggedIn(false);
        setIsOpen(false);
        setFormData({ name: '', softwareBg: '', hardwareBg: '' });
        window.location.reload();
    };

    return (
        <>
            {!isLoggedIn ? (
                <button className={styles.authButton} onClick={() => setIsOpen(true)}>
                    Start Here (Login)
                </button>
            ) : (
                <button className={styles.authButton} onClick={() => setIsOpen(true)} style={{ background: 'var(--ifm-color-secondary)' }}>
                    👤 {formData.name || 'Student'}
                </button>
            )}

            {isOpen && (
                <div className={styles.modalOverlay}>
                    <div className={styles.modalContent}>
                        {isLoggedIn ? (
                            <>
                                <h2>👤 Student Profile</h2>
                                <div className={styles.formGroup}>
                                    <p><strong>Name:</strong> {formData.name}</p>
                                    <p><strong>Software:</strong> {formData.softwareBg}</p>
                                    <p><strong>Hardware:</strong> {formData.hardwareBg}</p>
                                </div>
                                <button onClick={handleLogout} className={styles.submitButton} style={{ background: 'var(--ifm-color-danger)' }}>
                                    Logout
                                </button>
                                <button onClick={() => setIsOpen(false)} className={styles.cancelButton}>
                                    Close
                                </button>
                            </>
                        ) : (
                            <>
                                <h2>🎓 Student Profile</h2>
                                <p>Tell us about yourself to personalize the course.</p>
                                <form onSubmit={handleLogin}>
                                    <div className={styles.formGroup}>
                                        <label>Name</label>
                                        <input
                                            required
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        />
                                    </div>
                                    <div className={styles.formGroup}>
                                        <label>Software Experience</label>
                                        <select
                                            required
                                            value={formData.softwareBg}
                                            onChange={(e) => setFormData({ ...formData, softwareBg: e.target.value })}
                                        >
                                            <option value="">Select...</option>
                                            <option value="beginner">Beginner (No coding)</option>
                                            <option value="intermediate">Intermediate (Python/JS)</option>
                                            <option value="advanced">Advanced (System Architect)</option>
                                        </select>
                                    </div>
                                    <div className={styles.formGroup}>
                                        <label>Hardware/Robotics Experience</label>
                                        <select
                                            required
                                            value={formData.hardwareBg}
                                            onChange={(e) => setFormData({ ...formData, hardwareBg: e.target.value })}
                                        >
                                            <option value="">Select...</option>
                                            <option value="none">None</option>
                                            <option value="hobbyist">Hobbyist (Arduino/RPi)</option>
                                            <option value="professional">Professional (ROS/Industrial)</option>
                                        </select>
                                    </div>
                                    <button type="submit" className={styles.submitButton}>Begin Journey 🚀</button>
                                    <button type="button" onClick={() => setIsOpen(false)} className={styles.cancelButton}>Close</button>
                                </form>
                            </>
                        )}
                    </div>
                </div>
            )}
        </>
    );
}
