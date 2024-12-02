// frontend/src/components/Navbar.js

import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Ensure this CSS file exists for styling
import { NavbarProps } from '../types';

const Navbar: React.FC<NavbarProps> = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navRef = useRef<HTMLDivElement>(null);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (navRef.current && !navRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [navRef]);

  return (
    <nav className="navbar" ref={navRef}>
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          Soknadsbrev.no
        </Link>
        <div className="menu-icon" onClick={toggleMenu}>
          {isOpen ? '✕' : '☰'}
        </div>
        <ul className={isOpen ? 'navbar-menu active' : 'navbar-menu'}>
          <li className="navbar-item">
            <Link to="/om-oss" className="navbar-link" onClick={closeMenu}>Om Oss</Link>
          </li>
          <li className="navbar-item">
            <Link to="/kontakt" className="navbar-link" onClick={closeMenu}>Kontakt</Link>
          </li>
          <li className="navbar-item">
            <Link to="/betingelser" className="navbar-link" onClick={closeMenu}>Betingelser</Link>
          </li>
          <li className="navbar-item">
            <Link to="/jobb-matcher" className="navbar-link" onClick={closeMenu}>Jobb Matcher</Link>
          </li>
          <li className="navbar-item">
            <Link to="/cover-letter-generator" className="navbar-link" onClick={closeMenu}>Generer Søknadsbrev</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
