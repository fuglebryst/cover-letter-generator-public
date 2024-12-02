// frontend/src/pages/JobMatcher.js

import React, { useState } from 'react';
import './JobMatcher.css';
import { LocationData } from '../types';

const JobMatcher: React.FC = () => {
  const [email, setEmail] = useState('');
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobPreferences, setJobPreferences] = useState('');
  const [fylke, setFylke] = useState('Velg alle');
  const [kommuneBydel, setKommuneBydel] = useState('Velg alle');
  const [isLoading, setIsLoading] = useState(false);

  const locationData: LocationData = {
    'Oslo': ['Oslo'],
    'Østfold': ['Velg alle', 'Halden', 'Moss', 'Sarpsborg', 'Fredrikstad', 'Hvaler', 'Råde', 'Våler', 'Skiptvet', 'Indre Østfold', 'Rakkestad', 'Marker', 'Aremark'],
    'Akershus': ['Velg alle', 'Bærum', 'Asker', 'Lillestrøm', 'Nordre Follo', 'Ullensaker', 'Nesodden', 'Frogn', 'Vestby', 'Ås', 'Enebakk', 'Lørenskog', 'Rælingen', 'Aurskog-Høland', 'Nes', 'Gjerdrum', 'Nittedal', 'Lunner', 'Jevnaker', 'Nannestad', 'Eidsvoll', 'Hurdal'],
    'Buskerud': ['Velg alle', 'Drammen', 'Kongsberg', 'Ringerike', 'Hole', 'Lier', 'Øvre Eiker', 'Modum', 'Krødsherad', 'Flå', 'Nesbyen', 'Gol', 'Hemsedal', 'Ål', 'Hol', 'Sigdal', 'Flesberg', 'Rollag', 'Nore og Uvdal'],
    'Innlandet': ['Velg alle', 'Kongsvinger', 'Hamar', 'Lillehammer', 'Gjøvik', 'Ringsaker', 'Løten', 'Stange', 'Nord-Odal', 'Sør-Odal', 'Eidskog', 'Grue', 'Åsnes', 'Våler', 'Elverum', 'Trysil', 'Åmot', 'Stor-Elvdal', 'Rendalen', 'Engerdal', 'Tolga', 'Tynset', 'Alvdal', 'Folldal', 'Os', 'Dovre', 'Lesja', 'Skjåk', 'Lom', 'Vågå', 'Nord-Fron', 'Sel', 'Sør-Fron', 'Ringebu', 'Øyer', 'Gausdal', 'Østre Toten', 'Vestre Toten', 'Gran', 'Søndre Land', 'Nordre Land', 'Sør-Aurdal', 'Etnedal', 'Nord-Aurdal', 'Vestre Slidre', 'Øystre Slidre', 'Vang'],
    'Vestfold': ['Velg alle', 'Horten', 'Holmestrand', 'Tønsberg', 'Sandefjord', 'Larvik', 'Færder'],
    'Telemark': ['Velg alle', 'Porsgrunn', 'Skien', 'Notodden', 'Siljan', 'Bamble', 'Kragerø', 'Drangedal', 'Nome', 'Midt-Telemark', 'Seljord', 'Hjartdal', 'Tinn', 'Kviteseid', 'Nissedal', 'Fyresdal', 'Tokke', 'Vinje'],
    'Agder': ['Velg alle', 'Risør', 'Grimstad', 'Arendal', 'Kristiansand', 'Lindesnes', 'Farsund', 'Flekkefjord', 'Gjerstad', 'Vegårshei', 'Tvedestrand', 'Froland', 'Lillesand', 'Birkenes', 'Åmli', 'Iveland', 'Evje og Hornnes', 'Bygland', 'Valle', 'Bykle', 'Vennesla', 'Åseral', 'Lyngdal', 'Hægebostad', 'Kvinesdal', 'Sirdal'],
    'Rogaland': ['Velg alle', 'Eigersund', 'Stavanger', 'Haugesund', 'Sandnes', 'Sokndal', 'Lund', 'Bjerkreim', 'Hå', 'Klepp', 'Time', 'Gjesdal', 'Sola', 'Randaberg', 'Strand', 'Hjelmeland', 'Suldal', 'Sauda', 'Kvitsøy', 'Bokn', 'Tysvær', 'Karmøy', 'Utsira', 'Vindafjord'],
    'Vestland': ['Velg alle', 'Bergen', 'Kinn', 'Etne', 'Sveio', 'Bømlo', 'Stord', 'Fitjar', 'Tysnes', 'Kvinnherad', 'Ullensvang', 'Eidfjord', 'Ulvik', 'Voss', 'Kvam', 'Samnanger', 'Bjørnafjorden', 'Austevoll', 'Øygarden', 'Askøy', 'Vaksdal', 'Modalen', 'Osterøy', 'Alver', 'Austrheim', 'Fedje', 'Masfjorden', 'Gulen', 'Solund', 'Hyllestad', 'Høyanger', 'Vik', 'Sogndal', 'Aurland', 'Lærdal', 'Årdal', 'Luster', 'Askvoll', 'Fjaler', 'Sunnfjord', 'Bremanger', 'Stad', 'Gloppen', 'Stryn'],
    'Møre og Romsdal': ['Velg alle', 'Kristiansund', 'Molde', 'Ålesund', 'Vanylven', 'Sande', 'Herøy', 'Ulstein', 'Hareid', 'Ørsta', 'Stranda', 'Sykkylven', 'Sula', 'Giske', 'Vestnes', 'Rauma', 'Aukra', 'Averøy', 'Gjemnes', 'Tingvoll', 'Sunndal', 'Surnadal', 'Smøla', 'Aure', 'Volda', 'Fjord', 'Hustadvika', 'Haram'],
    'Trøndelag': ['Velg alle', 'Trondheim', 'Steinkjer', 'Namsos', 'Frøya', 'Osen', 'Oppdal', 'Rennebu', 'Røros', 'Holtålen', 'Midtre Gauldal', 'Melhus', 'Skaun', 'Malvik', 'Selbu', 'Tydal', 'Meråker', 'Stjørdal', 'Frosta', 'Levanger', 'Verdal', 'Snåsa', 'Lierne', 'Røyrvik', 'Namsskogan', 'Grong', 'Høylandet', 'Overhalla', 'Flatanger', 'Leka', 'Inderøy', 'Indre Fosen', 'Heim', 'Hitra', 'Ørland', 'Åfjord', 'Orkland', 'Nærøysund', 'Rindal'],
    'Nordland': ['Velg alle', 'Bodø', 'Narvik', 'Bindal', 'Sømna', 'Brønnøy', 'Vega', 'Vevelstad', 'Herøy', 'Alstahaug', 'Leirfjord', 'Vefsn', 'Grane', 'Hattfjelldal', 'Dønna', 'Nesna', 'Hemnes', 'Rana', 'Lurøy', 'Træna', 'Rødøy', 'Meløy', 'Gildeskål', 'Beiarn', 'Saltdal', 'Fauske', 'Sørfold', 'Steigen', 'Lødingen', 'Evenes', 'Røst', 'Værøy', 'Flakstad', 'Vestvågøy', 'Vågan', 'Hadsel', 'Bø', 'Øksnes', 'Sortland', 'Andøy', 'Moskenes', 'Hamarøy'],
    'Troms': ['Velg alle', 'Tromsø', 'Harstad', 'Kvæfjord', 'Tjeldsund', 'Ibestad', 'Gratangen', 'Lavangen', 'Bardu', 'Salangen', 'Målselv', 'Sørreisa', 'Dyrøy', 'Senja', 'Balsfjord', 'Karlsøy', 'Lyngen', 'Storfjord', 'Kåfjord', 'Skjervøy', 'Nordreisa', 'Kvænangen'],
    'Finnmark': ['Velg alle', 'Alta', 'Hammerfest', 'Sør-Varanger', 'Vadsø', 'Karasjok', 'Kautokeino', 'Loppa', 'Hasvik', 'Måsøy', 'Nordkapp', 'Porsanger', 'Lebesby', 'Gamvik', 'Tana', 'Berlevåg', 'Båtsfjord', 'Vardø', 'Nesseby'],
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    if (!email || !cvFile) {
      alert('Vennligst fyll ut alle påkrevde felt og last opp en CV.');
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('cv_file', cvFile);
    formData.append('job_preferences', jobPreferences);
    formData.append('fylke', fylke);
    formData.append('kommune_bydel', kommuneBydel);

    try {
      const response = await fetch('/api/enqueue_request', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        if (data.message === 'Success') {
          alert('Takk! Vi sender deg matchede jobber og søknadsbrev på e-post.');
          setEmail('');
          setCvFile(null);
          setJobPreferences('');
          setFylke('Velg alle');
          setKommuneBydel('Velg alle');
        } else {
          alert(data.message || 'Det oppstod en feil. Vennligst prøv igjen.');
        }
      } else {
        const errorData = await response.json();
        alert(errorData.message || 'Det oppstod en feil. Vennligst prøv igjen.');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('Det oppstod en feil. Vennligst prøv igjen.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFylkeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedFylke = e.target.value;
    setFylke(selectedFylke);
    setKommuneBydel('Velg alle');
  };

  const shouldShowKommuneBydel = fylke !== 'Oslo' && fylke !== 'Velg alle';

  return (
    <div className="container">
      <h1>Finn Matchede Jobber</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Din e-postadresse:</label>
        <input
          type="email"
          id="email"
          name="email"
          required
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
        />

        <label htmlFor="cv_file">Last opp din CV:</label>
        <input
          type="file"
          id="cv_file"
          name="cv_file"
          accept=".txt,.pdf,.docx"
          required
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
            const files = e.target.files;
            if (files && files.length > 0) {
              setCvFile(files[0]);
            }
          }}
        />

        <label htmlFor="job_preferences">Dine jobbpreferanser:</label>
        <textarea
          id="job_preferences"
          name="job_preferences"
          value={jobPreferences}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setJobPreferences(e.target.value)}
          placeholder="Beskriv hvilke typer jobber du er interessert i..."
        />

        <label htmlFor="fylke">Velg fylke:</label>
        <select id="fylke" name="fylke" value={fylke} onChange={handleFylkeChange}>
          <option value="Velg alle">Velg alle</option>
          {Object.keys(locationData).map((fylkeName) => (
            <option key={fylkeName} value={fylkeName}>
              {fylkeName}
            </option>
          ))}
        </select>

        {shouldShowKommuneBydel && (
          <>
            <label htmlFor="kommune_bydel">Velg kommune:</label>
            <select
              id="kommune_bydel"
              name="kommune_bydel"
              value={kommuneBydel}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setKommuneBydel(e.target.value)}
            >
              {locationData[fylke]?.map((kommune) => (
                <option key={kommune} value={kommune}>
                  {kommune}
                </option>
              ))}
            </select>
          </>
        )}

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Sender...' : 'Finn Jobber'}
        </button>
      </form>
    </div>
  );
};

export default JobMatcher;
