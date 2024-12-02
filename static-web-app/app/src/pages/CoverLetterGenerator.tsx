// frontend/src/pages/CoverLetterGenerator.js

import React, { useState, useEffect } from 'react';
import './CoverLetterGenerator.css';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { TextAreaEvent } from '../types';

const CoverLetterGenerator: React.FC = () => {
    const [cvFile, setCvFile] = useState<File | null>(null);
    const [hasCv, setHasCv] = useState(true);
    const [backgroundText, setBackgroundText] = useState('');
    const [jobAdOption, setJobAdOption] = useState('link');
    const [jobAdLink, setJobAdLink] = useState('');
    const [jobAdFile, setJobAdFile] = useState<File | null>(null);
    const [jobAdText, setJobAdText] = useState('');
    const [coverLetter, setCoverLetter] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showOptions, setShowOptions] = useState(false);

    useEffect(() => {
        // Set placeholder text for the cover letter
        setCoverLetter(`[Din søknadstekst vil vises her etter generering...]`);
    }, []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);
        setShowOptions(false);

        const formData = new FormData();
        
        formData.append('action', 'generate');
        
        if (hasCv && cvFile) {
            formData.append('cv_file', cvFile);
        } else {
            formData.append('background_text', backgroundText);
        }
        
        formData.append('job_ad_option', jobAdOption);
        
        if (jobAdOption === 'link') {
            formData.append('job_ad_link', jobAdLink);
        } else if (jobAdOption === 'upload' && jobAdFile) {
            formData.append('job_ad_file', jobAdFile);
        } else if (jobAdOption === 'freeform') {
            formData.append('job_description', jobAdText);
        }

        try {
            const response = await fetch('/api/generate_cover_letter', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                setCoverLetter(data.cover_letter || data.message);
                setShowOptions(true);
            } else {
                alert(data.message || 'En feil oppstod. Vennligst prøv igjen.');
            }
        } catch (error) {
            console.error('Error generating cover letter:', error);
            alert('En feil oppstod. Vennligst prøv igjen.');
        } finally {
            setIsLoading(false);
        }
    };

    const downloadDOCX = async () => {
        try {
            const formData = new FormData();
            formData.append('action', 'download');
            formData.append('cover_letter', coverLetter.replace(/<[^>]+>/g, ''));

            const response = await fetch('/api/generate_cover_letter', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to download');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Soknadsbrev.docx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Error downloading DOCX:', error);
            alert('En feil oppstod under nedlasting. Vennligst prøv igjen.');
        }
    };

    const sendEmail = async () => {
        const userEmail = prompt('Vennligst skriv inn din e-postadresse:');
        if (!userEmail) return;

        try {
            const formData = new FormData();
            formData.append('action', 'email');
            formData.append('cover_letter', coverLetter.replace(/<[^>]+>/g, ''));
            formData.append('email', userEmail);
            if (jobAdOption === 'link') {
                formData.append('job_ad_link', jobAdLink);
            }

            const response = await fetch('/api/generate_cover_letter', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                alert('Søknadsbrev sendt til din e-post!');
            } else {
                throw new Error(data.message || 'Failed to send email');
            }
        } catch (error) {
            console.error('Error sending email:', error);
            alert('En feil oppstod under sending av e-post. Vennligst prøv igjen.');
        }
    };

    const handleBackgroundTextChange = (e: TextAreaEvent): void => {
        setBackgroundText(e.target.value);
    };

    const handleJobAdTextChange = (e: TextAreaEvent): void => {
        setJobAdText(e.target.value);
    };

    return (
        <div className="container">
            <h1>Generer Søknadsbrev</h1>
            <form onSubmit={handleSubmit} className="generator-form">
                {/* Form Section */}
                <div className="form-section">
                    {/* Has CV or Background Text */}
                    <label>Har du en CV eller vil du skrive inn din bakgrunn?</label>
                    <div className="toggle-group">
                        <label>
                            <input
                                type="radio"
                                name="has_cv"
                                value="true"
                                checked={hasCv === true}
                                onChange={() => setHasCv(true)}
                            />
                            Last opp CV
                        </label>
                        <label>
                            <input
                                type="radio"
                                name="has_cv"
                                value="false"
                                checked={hasCv === false}
                                onChange={() => setHasCv(false)}
                            />
                            Skriv inn bakgrunn
                        </label>
                    </div>

                    {hasCv ? (
                        <>
                            <label htmlFor="cv_file">Last opp din CV:</label>
                            <input
                                type="file"
                                id="cv_file"
                                name="cv_file"
                                accept=".txt,.pdf,.docx"
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                                    const files = e.target.files;
                                    if (files && files.length > 0) {
                                        setCvFile(files[0]);
                                    }
                                }}
                                required
                            />
                        </>
                    ) : (
                        <>
                            <label htmlFor="background_text">Din bakgrunn:</label>
                            <textarea
                                id="background_text"
                                name="background_text"
                                value={backgroundText}
                                onChange={handleBackgroundTextChange}
                                placeholder="Skriv inn din bakgrunn og erfaring..."
                            ></textarea>
                        </>
                    )}

                    {/* Job Ad Option */}
                    <label>Hvordan vil du legge inn jobbannonsen?</label>
                    <div className="toggle-group">
                        <label>
                            <input
                                type="radio"
                                name="job_ad_option"
                                value="link"
                                checked={jobAdOption === 'link'}
                                onChange={() => setJobAdOption('link')}
                            />
                            Legg inn lenke
                        </label>
                        <label>
                            <input
                                type="radio"
                                name="job_ad_option"
                                value="upload"
                                checked={jobAdOption === 'upload'}
                                onChange={() => setJobAdOption('upload')}
                            />
                            Last opp fil
                        </label>
                        <label>
                            <input
                                type="radio"
                                name="job_ad_option"
                                value="freeform"
                                checked={jobAdOption === 'freeform'}
                                onChange={() => setJobAdOption('freeform')}
                            />
                            Skriv inn tekst
                        </label>
                    </div>

                    {jobAdOption === 'link' && (
                        <>
                            <label htmlFor="job_ad_link">Jobbannonse lenke:</label>
                            <input
                                type="url"
                                id="job_ad_link"
                                name="job_ad_link"
                                value={jobAdLink}
                                onChange={(e) => setJobAdLink(e.target.value)}
                                placeholder="https://www.finn.no/job/fulltime/ad.html?finnkode=..."
                                required
                            />
                        </>
                    )}

                    {jobAdOption === 'upload' && (
                        <>
                            <label htmlFor="job_ad_file">Last opp jobbannonse fil:</label>
                            <input
                                type="file"
                                id="job_ad_file"
                                name="job_ad_file"
                                accept=".txt,.pdf,.docx"
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                                    const files = e.target.files;
                                    if (files && files.length > 0) {
                                        setJobAdFile(files[0]);
                                    }
                                }}
                                required
                            />
                        </>
                    )}

                    {jobAdOption === 'freeform' && (
                        <>
                            <label htmlFor="job_ad_text">Jobbannonse tekst:</label>
                            <textarea
                                id="job_ad_text"
                                name="job_ad_text"
                                value={jobAdText}
                                onChange={handleJobAdTextChange}
                                placeholder="Kopier og lim inn teksten fra jobbannonsen her..."
                                required
                            ></textarea>
                        </>
                    )}

                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Genererer...' : 'Generer Søknadsbrev'}
                    </button>
                </div>

                {/* Output Section with Action Buttons Above Editor */}
                <div className="output-section">
                    <label htmlFor="cover_letter">Generert Søknadsbrev:</label>

                    {/* Action Buttons */}
                    {showOptions && (
                        <div className="additional-options">
                            {/* Only Word download option */}
                            <button
                                type="button"
                                onClick={downloadDOCX}
                                className="option-button"
                            >
                                Last ned som Word
                            </button>
                            <button
                                type="button"
                                onClick={sendEmail}
                                className="option-button"
                            >
                                Send e-post
                            </button>
                        </div>
                    )}

                    {/* ReactQuill Editor */}
                    <ReactQuill
                        theme="snow"
                        value={coverLetter}
                        onChange={setCoverLetter}
                        readOnly={false} // Always editable
                        placeholder="Ditt genererte søknadsbrev vil vises her..."
                    />
                </div>
            </form>
        </div>
    );
}

export default CoverLetterGenerator;
