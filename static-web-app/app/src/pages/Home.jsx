// frontend/src/pages/Home.js

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Home.css'; // We'll create this CSS file
import heroImage from '../assets/hero.jpg'; // Ensure you have a hero image at this path
import soknadsbrevButikkmedarbeider from '../assets/soknadsbrev-butikkmedarbeider.jpg';
import soknadsbrevMarkedsforing from '../assets/soknadsbrev-markedsforing.jpg';
import soknadsbrevSalgskonsulent from '../assets/soknadsbrev-salgskonsulent.jpg';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileWord, faRobot, faClock, faCheckCircle, faMoneyBillWave, faLightbulb } from '@fortawesome/free-solid-svg-icons';

function Home() {
  // State for modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalImageSrc, setModalImageSrc] = useState('');
  const [modalImageAlt, setModalImageAlt] = useState('');

  const openModal = (imageSrc, imageAlt) => {
    setModalImageSrc(imageSrc);
    setModalImageAlt(imageAlt);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setModalImageSrc('');
    setModalImageAlt('');
  };


  return (
    <div className="home">
      {/* Hero Section */}
      <div className="hero-section" style={{ backgroundImage: `url(${heroImage})` }}>
        <div className="hero-overlay">
          <h1>Få ditt perfekte søknadsbrev på få minutter</h1>
          <p>
            Spar tid og øk sjansene dine med vårt AI-drevne verktøy. Generer profesjonelle søknadsbrev skreddersydd for din drømmejobb.
          </p>
          <Link to="/cover-letter-generator">
            <button className="cta-button">Generer Søknadsbrev</button>
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <div className="features">
          <div className="feature">
            <FontAwesomeIcon icon={faRobot} size="3x" />
            <h3>Nyeste AI-teknologi</h3>
            <p>Vår løsning er drevet av ChatGPT 4 for optimal kvalitet.</p>
          </div>
          <div className="feature">
            <FontAwesomeIcon icon={faClock} size="3x" />
            <h3>Spar Tid</h3>
            <p>Generer søknadsbrev på minutter i stedet for timer.</p>
          </div>
          <div className="feature">
            <FontAwesomeIcon icon={faCheckCircle} size="3x" />
            <h3>Ingen Skrivefeil</h3>
            <p>Få feilfrie søknadsbrev hver gang.</p>
          </div>
        </div>
      </div>

      {/* Why Choose Us Section */}
      <div className="why-us-section">
        <h2>Hvorfor Velge Oss?</h2>
        <div className="benefits">
          <div className="benefit">
            <FontAwesomeIcon icon={faLightbulb} size="3x" />
            <h3>Tilpasset Dine Behov</h3>
            <p>Vår AI tilpasser søknadsbrevet basert på din CV og ønsket stilling.</p>
          </div>
          <div className="benefit">
            <FontAwesomeIcon icon={faFileWord} size="3x" />
            <h3>Last Ned som Word</h3>
            <p>Rediger søknadsbrevet ditt enkelt i Word-format.</p>
          </div>
          <div className="benefit">
            <FontAwesomeIcon icon={faMoneyBillWave} size="3x" />
            <h3>Kostnadseffektivt</h3>
            <p>Få profesjonelle søknadsbrev uten å tømme lommeboken.</p>
          </div>
        </div>
      </div>

      {/* Example Section */}
      <div className="example-section">
        <h2>Eksempler på AI-genererte søknadsbrev</h2>
        <div className="examples">
          <div className="example">
            <img
              src={soknadsbrevButikkmedarbeider}
              alt="Søknadsbrev for Butikkmedarbeider"
              onClick={() =>
                openModal(
                  soknadsbrevButikkmedarbeider,
                  'Søknadsbrev for Butikkmedarbeider'
                )
              }
            />
            <p>Butikkmedarbeiderstilling</p>
          </div>
          <div className="example">
            <img
              src={soknadsbrevMarkedsforing}
              alt="Søknadsbrev for Markedsføring"
              onClick={() =>
                openModal(
                  soknadsbrevMarkedsforing,
                  'Søknadsbrev for Markedsføring'
                )
              }
            />
            <p>Markedsførerstilling</p>
          </div>
          <div className="example">
            <img
              src={soknadsbrevSalgskonsulent}
              alt="Søknadsbrev for Salgskonsulent"
              onClick={() =>
                openModal(
                  soknadsbrevSalgskonsulent,
                  'Søknadsbrev for Salgskonsulent'
                )
              }
            />
            <p>Salgskonsulentstilling</p>
          </div>
        </div>
        <Link to="/cover-letter-generator">
          <button className="cta-button">Generer ditt eget søknadsbrev</button>
        </Link>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="modal-overlay" onClick={closeModal}>
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <span className="close-button" onClick={closeModal}>
              &times;
            </span>
            <img
              src={modalImageSrc}
              alt={modalImageAlt}
              className="modal-image"
            />
          </div>
        </div>
      )}

      {/* Pricing Section */}
      <div className="pricing-section">
        <h2>Priser</h2>
        <div className="pricing">
          <div className="price-option">
            <h3>Enkel Søknad</h3>
            <p>kr 49,- per søknad</p>
            <ul>
              <li>AI-generert søknadsbrev</li>
              <li>Last ned som Word-fil</li>
            </ul>
            <Link to="/cover-letter-generator">
              <button className="cta-button">Kom i gang</button>
            </Link>
          </div>
          {/* You can add more pricing options here if needed */}
        </div>
      </div>

      {/* Benefits of AI Section */}
      <div className="ai-benefits-section">
        <h2>Fordeler med AI-genererte Søknadsbrev</h2>
        <ul>
          <li>Tilpasset hver enkelt stilling</li>
          <li>Profesjonell språkbruk</li>
          <li>Ingen skrivefeil eller grammatiske feil</li>
          <li>Økt sjanse for å bli innkalt til intervju</li>
        </ul>
      </div>
    
      {/* Articles Section 
      <div className="articles-section">
        <h2>Søknadstips</h2>
        <p>Les våre artikler for tips om jobbsøking og karriereutvikling.</p>
        <Link to="/articles">
          <button className="cta-button">Les mer</button>
        </Link>
      </div>*/}
    </div>
  );
}

export default Home;
