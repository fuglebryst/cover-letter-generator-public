# shared_code/matcher.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
import copy

logger = logging.getLogger(__name__)

location_data = {
    'Oslo': ['Oslo'],
    'Østfold': ['Halden', 'Moss', 'Sarpsborg', 'Fredrikstad', 'Hvaler', 'Råde', 'Våler', 'Skiptvet', 'Indre Østfold', 'Rakkestad', 'Marker', 'Aremark'],
    'Akershus': ['Bærum', 'Asker', 'Lillestrøm', 'Nordre Follo', 'Ullensaker', 'Nesodden', 'Frogn', 'Vestby', 'Ås', 'Enebakk', 'Lørenskog', 'Rælingen', 'Aurskog-Høland', 'Nes', 'Gjerdrum', 'Nittedal', 'Lunner', 'Jevnaker', 'Nannestad', 'Eidsvoll', 'Hurdal'],
    'Buskerud': ['Drammen', 'Kongsberg', 'Ringerike', 'Hole', 'Lier', 'Øvre Eiker', 'Modum', 'Krødsherad', 'Flå', 'Nesbyen', 'Gol', 'Hemsedal', 'Ål', 'Hol', 'Sigdal', 'Flesberg', 'Rollag', 'Nore og Uvdal'],
    'Innlandet': ['Kongsvinger', 'Hamar', 'Lillehammer', 'Gjøvik', 'Ringsaker', 'Løten', 'Stange', 'Nord-Odal', 'Sør-Odal', 'Eidskog', 'Grue', 'Åsnes', 'Våler', 'Elverum', 'Trysil', 'Åmot', 'Stor-Elvdal', 'Rendalen', 'Engerdal', 'Tolga', 'Tynset', 'Alvdal', 'Folldal', 'Os', 'Dovre', 'Lesja', 'Skjåk', 'Lom', 'Vågå', 'Nord-Fron', 'Sel', 'Sør-Fron', 'Ringebu', 'Øyer', 'Gausdal', 'Østre Toten', 'Vestre Toten', 'Gran', 'Søndre Land', 'Nordre Land', 'Sør-Aurdal', 'Etnedal', 'Nord-Aurdal', 'Vestre Slidre', 'Øystre Slidre', 'Vang'],
    'Vestfold': ['Horten', 'Holmestrand', 'Tønsberg', 'Sandefjord', 'Larvik', 'Færder'],
    'Telemark': ['Porsgrunn', 'Skien', 'Notodden', 'Siljan', 'Bamble', 'Kragerø', 'Drangedal', 'Nome', 'Midt-Telemark', 'Seljord', 'Hjartdal', 'Tinn', 'Kviteseid', 'Nissedal', 'Fyresdal', 'Tokke', 'Vinje'],
    'Agder': ['Risør', 'Grimstad', 'Arendal', 'Kristiansand', 'Lindesnes', 'Farsund', 'Flekkefjord', 'Gjerstad', 'Vegårshei', 'Tvedestrand', 'Froland', 'Lillesand', 'Birkenes', 'Åmli', 'Iveland', 'Evje og Hornnes', 'Bygland', 'Valle', 'Bykle', 'Vennesla', 'Åseral', 'Lyngdal', 'Hægebostad', 'Kvinesdal', 'Sirdal'],
    'Rogaland': ['Eigersund', 'Stavanger', 'Haugesund', 'Sandnes', 'Sokndal', 'Lund', 'Bjerkreim', 'Hå', 'Klepp', 'Time', 'Gjesdal', 'Sola', 'Randaberg', 'Strand', 'Hjelmeland', 'Suldal', 'Sauda', 'Kvitsøy', 'Bokn', 'Tysvær', 'Karmøy', 'Utsira', 'Vindafjord'],
    'Vestland': ['Bergen', 'Kinn', 'Etne', 'Sveio', 'Bømlo', 'Stord', 'Fitjar', 'Tysnes', 'Kvinnherad', 'Ullensvang', 'Eidfjord', 'Ulvik', 'Voss', 'Kvam', 'Samnanger', 'Bjørnafjorden', 'Austevoll', 'Øygarden', 'Askøy', 'Vaksdal', 'Modalen', 'Osterøy', 'Alver', 'Austrheim', 'Fedje', 'Masfjorden', 'Gulen', 'Solund', 'Hyllestad', 'Høyanger', 'Vik', 'Sogndal', 'Aurland', 'Lærdal', 'Årdal', 'Luster', 'Askvoll', 'Fjaler', 'Sunnfjord', 'Bremanger', 'Stad', 'Gloppen', 'Stryn'],
    'Møre og Romsdal': ['Kristiansund', 'Molde', 'Ålesund', 'Vanylven', 'Sande', 'Herøy', 'Ulstein', 'Hareid', 'Ørsta', 'Stranda', 'Sykkylven', 'Sula', 'Giske', 'Vestnes', 'Rauma', 'Aukra', 'Averøy', 'Gjemnes', 'Tingvoll', 'Sunndal', 'Surnadal', 'Smøla', 'Aure', 'Volda', 'Fjord', 'Hustadvika', 'Haram'],
    'Trøndelag': ['Trondheim', 'Steinkjer', 'Namsos', 'Frøya', 'Osen', 'Oppdal', 'Rennebu', 'Røros', 'Holtålen', 'Midtre Gauldal', 'Melhus', 'Skaun', 'Malvik', 'Selbu', 'Tydal', 'Meråker', 'Stjørdal', 'Frosta', 'Levanger', 'Verdal', 'Snåsa', 'Lierne', 'Røyrvik', 'Namsskogan', 'Grong', 'Høylandet', 'Overhalla', 'Flatanger', 'Leka', 'Inderøy', 'Indre Fosen', 'Heim', 'Hitra', 'Ørland', 'Åfjord', 'Orkland', 'Nærøysund', 'Rindal'],
    'Nordland': ['Bodø', 'Narvik', 'Bindal', 'Sømna', 'Brønnøy', 'Vega', 'Vevelstad', 'Herøy', 'Alstahaug', 'Leirfjord', 'Vefsn', 'Grane', 'Hattfjelldal', 'Dønna', 'Nesna', 'Hemnes', 'Rana', 'Lurøy', 'Træna', 'Rødøy', 'Meløy', 'Gildeskål', 'Beiarn', 'Saltdal', 'Fauske', 'Sørfold', 'Steigen', 'Lødingen', 'Evenes', 'Røst', 'Værøy', 'Flakstad', 'Vestvågøy', 'Vågan', 'Hadsel', 'Bø', 'Øksnes', 'Sortland', 'Andøy', 'Moskenes', 'Hamarøy'],
    'Troms': ['Tromsø', 'Harstad', 'Kvæfjord', 'Tjeldsund', 'Ibestad', 'Gratangen', 'Lavangen', 'Bardu', 'Salangen', 'Målselv', 'Sørreisa', 'Dyrøy', 'Senja', 'Balsfjord', 'Karlsøy', 'Lyngen', 'Storfjord', 'Kåfjord', 'Skjervøy', 'Nordreisa', 'Kvænangen'],
    'Finnmark': ['Alta', 'Hammerfest', 'Sør-Varanger', 'Vadsø', 'Karasjok', 'Kautokeino', 'Loppa', 'Hasvik', 'Måsøy', 'Nordkapp', 'Porsanger', 'Lebesby', 'Gamvik', 'Tana', 'Berlevåg', 'Båtsfjord', 'Vardø', 'Nesseby']
}

def get_embedding(client, text, model="text-embedding-3-small"):
    """
    Generates an embedding for the given text using OpenAI's embedding model.
    """
    try:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding for text: {e}", exc_info=True)
        return []

def match_jobs(client, cv_text, jobs, job_preferences, fylke, kommune_bydel):
    """
    Matches jobs to the user's CV and preferences using embeddings.
    """
    if not jobs:
        logger.info("No jobs to match.")
        return []

    logger.debug("Computing CV embedding...")
    cv_embedding = get_embedding(client, cv_text)

    if not cv_embedding:
        logger.error("Failed to generate CV embedding.")
        return []

    # Compute job preferences embedding if provided
    preferences_embedding = None
    if job_preferences:
        logger.debug("Computing job preferences embedding...")
        preferences_embedding = get_embedding(client, job_preferences)

    # Normalize inputs to avoid case sensitivity and whitespace issues
    fylke = fylke.strip().lower()
    kommune_bydel = kommune_bydel.strip().lower()

    # Normalize location data
    normalized_location_data = {
        k.strip().lower(): [v.strip().lower() for v in vs]
        for k, vs in location_data.items()
    }

    filtered_jobs = []
    for job in jobs:
        # Skip jobs with missing or empty 'location' field
        if 'location' not in job or not job['location']:
            logger.warning(f"Skipping job with missing location: {job}")
            continue

        # Normalize job location
        job_location = job.get('location').strip().lower()

        if fylke == "velg alle":
            # Include all jobs
            filtered_jobs.append(job)
        else:
            if kommune_bydel == "velg alle":
                # Include jobs where job_location is in the selected fylke
                if fylke in normalized_location_data:
                    if job_location in normalized_location_data[fylke]:
                        filtered_jobs.append(job)
                    else:
                        logger.debug(f"Job location '{job_location}' not in selected fylke '{fylke}'")
                else:
                    logger.warning(f"Fylke '{fylke}' not found in location data.")
            else:
                # Include jobs where job_location matches the selected kommune_bydel
                if job_location == kommune_bydel:
                    filtered_jobs.append(job)

    if not filtered_jobs:
        logger.error("No jobs matched the location criteria.")
        return []

    # Prepare job embeddings from precomputed data
    valid_jobs = []
    valid_job_embeddings = []

    for job in filtered_jobs:
        embedding = job.get('embedding')
        if embedding:
            job_copy = job.copy()
            valid_jobs.append(job_copy)
            valid_job_embeddings.append(embedding)
        else:
            logger.warning(f"No embedding found for job {job.get('id', 'unknown')}")

    if not valid_jobs:
        logger.error("No jobs with embeddings available.")
        return []

    # Calculate similarity scores between CV and jobs
    logger.debug("Calculating similarity scores...")
    cv_embedding = np.array(cv_embedding).reshape(1, -1)
    job_embeddings_array = np.array(valid_job_embeddings)
    cv_similarities = cosine_similarity(cv_embedding, job_embeddings_array)[0]

    # Adjust scores based on job preferences if available
    if preferences_embedding:
        preferences_embedding = np.array(preferences_embedding).reshape(1, -1)
        preferences_similarities = cosine_similarity(preferences_embedding, job_embeddings_array)[0]
        # Combine CV and preferences scores, with a minor weight for preferences
        combined_scores = cv_similarities + 0.1 * preferences_similarities
    else:
        combined_scores = cv_similarities

    # Assign combined scores to jobs
    for i, job in enumerate(valid_jobs):
        job['score'] = combined_scores[i]

    # Sort jobs by score in descending order
    matched_jobs = sorted(valid_jobs, key=lambda x: x['score'], reverse=True)

    # Remove 'embedding' field from job dictionaries to prevent issues
    for job in matched_jobs:
        job.pop('embedding', None)

    return matched_jobs