import React, { useState } from 'react';
import styles from './AuthForms.module.css';

interface SignupFormData {
    email: string;
    password: string;
    name: string;
    softwareBackground: 'beginner' | 'intermediate' | 'advanced';
    hardwareExperience: 'none' | 'hobbyist' | 'professional';
    programmingLanguages: string[];
    rosExperience: boolean;
    learningGoals: string;
}

export function SignupForm() {
    const [formData, setFormData] = useState<SignupFormData>({
        email: '',
        password: '',
        name: '',
        softwareBackground: 'beginner',
        hardwareExperience: 'none',
        programmingLanguages: [],
        rosExperience: false,
        learningGoals: '',
    });
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
                credentials: 'include',
            });

            if (!response.ok) {
                throw new Error('Signup failed');
            }

            const data = await response.json();
            alert('Signup successful! Welcome aboard!');
            window.location.href = '/';
        } catch (error) {
            console.error('Signup error:', error);
            alert('Signup failed. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleLanguageToggle = (lang: string) => {
        setFormData(prev => ({
            ...prev,
            programmingLanguages: prev.programmingLanguages.includes(lang)
                ? prev.programmingLanguages.filter(l => l !== lang)
                : [...prev.programmingLanguages, lang]
        }));
    };

    return (
        <form onSubmit={handleSubmit} className={styles.form}>
            <h2>Create Your Account</h2>
            <p className={styles.subtitle}>Tell us about your background to personalize your learning experience</p>

            <div className={styles.formGroup}>
                <label>Name</label>
                <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                />
            </div>

            <div className={styles.formGroup}>
                <label>Email</label>
                <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                />
            </div>

            <div className={styles.formGroup}>
                <label>Password</label>
                <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                    minLength={8}
                />
            </div>

            <div className={styles.section}>
                <h3>Background Information</h3>

                <div className={styles.formGroup}>
                    <label>Software Development Experience</label>
                    <select
                        value={formData.softwareBackground}
                        onChange={(e) => setFormData({ ...formData, softwareBackground: e.target.value as any })}
                    >
                        <option value="beginner">Beginner - Just starting out</option>
                        <option value="intermediate">Intermediate - Some experience</option>
                        <option value="advanced">Advanced - Professional developer</option>
                    </select>
                </div>

                <div className={styles.formGroup}>
                    <label>Hardware/Robotics Experience</label>
                    <select
                        value={formData.hardwareExperience}
                        onChange={(e) => setFormData({ ...formData, hardwareExperience: e.target.value as any })}
                    >
                        <option value="none">No experience</option>
                        <option value="hobbyist">Hobbyist - Personal projects</option>
                        <option value="professional">Professional - Industry experience</option>
                    </select>
                </div>

                <div className={styles.formGroup}>
                    <label>Programming Languages You Know</label>
                    <div className={styles.checkboxGrid}>
                        {['Python', 'C++', 'JavaScript', 'Java', 'Rust', 'Go'].map(lang => (
                            <label key={lang} className={styles.checkbox}>
                                <input
                                    type="checkbox"
                                    checked={formData.programmingLanguages.includes(lang)}
                                    onChange={() => handleLanguageToggle(lang)}
                                />
                                {lang}
                            </label>
                        ))}
                    </div>
                </div>

                <div className={styles.formGroup}>
                    <label className={styles.checkbox}>
                        <input
                            type="checkbox"
                            checked={formData.rosExperience}
                            onChange={(e) => setFormData({ ...formData, rosExperience: e.target.checked })}
                        />
                        I have experience with ROS (Robot Operating System)
                    </label>
                </div>

                <div className={styles.formGroup}>
                    <label>What are your learning goals?</label>
                    <textarea
                        value={formData.learningGoals}
                        onChange={(e) => setFormData({ ...formData, learningGoals: e.target.value })}
                        placeholder="E.g., Build a robot, Learn for work, Personal interest..."
                        rows={3}
                    />
                </div>
            </div>

            <button type="submit" disabled={isSubmitting} className={styles.submitButton}>
                {isSubmitting ? 'Creating Account...' : 'Sign Up'}
            </button>
        </form>
    );
}

export function SigninForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
            const response = await fetch(`${API_URL}/api/auth/signin`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
                credentials: 'include',
            });

            if (!response.ok) {
                throw new Error('Signin failed');
            }

            const data = await response.json();
            alert('Signin successful!');
            window.location.href = '/';
        } catch (error) {
            console.error('Signin error:', error);
            alert('Signin failed. Please check your credentials.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className={styles.form}>
            <h2>Welcome Back</h2>
            <p className={styles.subtitle}>Sign in to continue your learning journey</p>

            <div className={styles.formGroup}>
                <label>Email</label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>

            <div className={styles.formGroup}>
                <label>Password</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>

            <button type="submit" disabled={isSubmitting} className={styles.submitButton}>
                {isSubmitting ? 'Signing In...' : 'Sign In'}
            </button>
        </form>
    );
}
