import json
import os

DB_FILE = 'database.json'
FACE_DATA_DIR = 'face_data'

def create_database():
    """
    Generates a massive medical database with cartoon avatars and deep medical data.
    """
    if not os.path.exists(FACE_DATA_DIR):
        os.makedirs(FACE_DATA_DIR)

    # Base URL for Cartoon Doctor Avatars (Reliable, never 404s)
    def get_avatar(name, gender='male'):
        # using dicebear avataaars for cartoon style
        base = "https://api.dicebear.com/9.x/avataaars/svg"
        # varying accessories to look like doctors
        return f"{base}?seed={name}&clothing=blazerAndShirt&eyebrows=defaultNatural&eyes=default"

    # --- DEEP MEDICAL KNOWLEDGE BASE ---
    medical_knowledge = {
        # 1. QUESTION FLOWS
        "flows": {
            "root": {
                "question": "I am HealthGuard AI. Please select the location of your pain or symptom.",
                "type": "option",
                "options": [
                    {"label": "Head / Face / Mental", "next_flow": "head"},
                    {"label": "Chest / Heart / Lungs", "next_flow": "chest"},
                    {"label": "Stomach / Digestion", "next_flow": "stomach"},
                    {"label": "Skin / Allergies", "next_flow": "skin"},
                    {"label": "Limbs / Joints / Bones", "next_flow": "limbs"},
                    {"label": "Teeth / Mouth", "next_flow": "mouth"},
                    {"label": "Eyes / Vision", "next_flow": "eyes"},
                    {"label": "Reproductive / Urinary", "next_flow": "uro_gyn"},
                    {"label": "General Body / Fever / Kids", "next_flow": "general"}
                ]
            },
            # --- HEAD FLOW ---
            "head": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "How would you describe the issue?",
                        "type": "option",
                        "options": ["Throbbing Headache", "Pressure/Tightness", "Dizziness/Vertigo", "Sadness/Anxiety/Panic", "Confusion/Memory"]
                    },
                    {
                        "id": "q2",
                        "question": "On a scale of 1-10, how severe is it?",
                        "type": "scale"
                    },
                    {
                        "id": "q3",
                        "question": "Are you experiencing sensitivity to light or sound?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- CHEST FLOW ---
            "chest": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "Describe the sensation in your chest.",
                        "type": "option",
                        "options": ["Crushing/Squeezing Pain", "Burning (Heartburn)", "Wheezing/Difficulty Breathing", "Sharp stabbing", "Fluttering Heart"]
                    },
                    {
                        "id": "q2",
                        "question": "Does the pain radiate to your left arm or jaw?",
                        "type": "yes_no"
                    },
                    {
                        "id": "q3",
                        "question": "Do you have a cough producing mucus?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- STOMACH FLOW ---
            "stomach": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "Where exactly is the pain located?",
                        "type": "option",
                        "options": ["Upper Middle (Heartburn)", "Lower Right", "All over / Cramping", "Lower Left", "Upper Right"]
                    },
                    {
                        "id": "q2",
                        "question": "Do you have diarrhea, vomiting, or blood in stool?",
                        "type": "yes_no"
                    },
                    {
                        "id": "q3",
                        "question": "Is the pain worse after eating fatty foods?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- SKIN FLOW ---
            "skin": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "What does the skin look like?",
                        "type": "option",
                        "options": ["Red Itchy Patches", "Fluid-filled Blisters", "Circular Ring Rash", "Hives/Welts", "Acne/Pimples", "Scaly Silver Patches"]
                    },
                    {
                        "id": "q2",
                        "question": "Is it spreading rapidly?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- LIMBS FLOW ---
            "limbs": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "Is the pain in the joint, muscle, or bone?",
                        "type": "option",
                        "options": ["Joint (Knee, Elbow)", "Muscle (Calf, Thigh)", "Bone (Deep pain)", "Nerve (Shooting pain)"]
                    },
                    {
                        "id": "q2",
                        "question": "Is the area red, swollen, and hot to touch?",
                        "type": "yes_no"
                    },
                    {
                        "id": "q3",
                        "question": "Is it difficult to move the limb?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- MOUTH FLOW ---
            "mouth": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "What is the issue?",
                        "type": "option",
                        "options": ["Severe Toothache", "Bleeding Gums", "Swollen Jaw/Abscess", "Bad Breath", "Loose Tooth"]
                    },
                    {
                        "id": "q2",
                        "question": "Is there visible swelling on your face?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- EYES FLOW ---
            "eyes": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "What is wrong with your vision/eyes?",
                        "type": "option",
                        "options": ["Red/Pink Eye", "Blurred Vision", "Itchy/Watery", "Eye Pain", "Floaters/Flashes"]
                    },
                    {
                        "id": "q2",
                        "question": "Do you wear contact lenses?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- URO/GYN FLOW ---
            "uro_gyn": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "Describe the symptom.",
                        "type": "option",
                        "options": ["Painful Urination", "Lower Abdominal Pain", "Frequent Urination", "Discharge/Itching"]
                    },
                    {
                        "id": "q2",
                        "question": "is there blood in your urine?",
                        "type": "yes_no"
                    }
                ]
            },
            # --- GENERAL FLOW ---
            "general": {
                "steps": [
                    {
                        "id": "q1",
                        "question": "What is your primary symptom?",
                        "type": "option",
                        "options": ["High Fever (>38C)", "Extreme Fatigue", "Body Aches", "Sore Throat", "Unexplained Weight Loss"]
                    },
                    {
                        "id": "q2",
                        "question": "How many days have you felt this way?",
                        "type": "number"
                    },
                    {
                        "id": "q3",
                        "question": "Is this for a child (under 12)?",
                        "type": "yes_no"
                    }
                ]
            }
        },

        # 2. DIAGNOSIS DATABASE (Massively Expanded)
        "diseases": [
            # -- HEAD & NEURO --
            {"name": "Migraine", "keywords": ["head", "throbbing", "light", "pulsing", "nausea"], "desc": "Severe throbbing pain, usually on one side of the head.", "specialty": "Neurologist", "medicine_id": 1},
            {"name": "Tension Headache", "keywords": ["head", "tight band", "pressure", "stress"], "desc": "Mild to moderate pain, feeling like a tight band around the head.", "specialty": "General Practitioner", "medicine_id": 2},
            {"name": "Vertigo (BPPV)", "keywords": ["head", "dizziness", "spinning", "nausea", "balance"], "desc": "A sensation of spinning caused by inner ear issues.", "specialty": "Neurologist", "medicine_id": 14},
            {"name": "Concussion", "keywords": ["head", "confusion", "injury", "dizziness", "vomiting"], "desc": "Mild traumatic brain injury. Requires rest.", "specialty": "Neurologist", "medicine_id": 2},
            {"name": "Cluster Headache", "keywords": ["head", "eye", "severe", "piercing", "one side"], "desc": "Excruciating attacks of pain in one side of the head, often around the eye.", "specialty": "Neurologist", "medicine_id": 1},
            
            # -- HEART & CIRCULATION --
            {"name": "Hypertension (High BP)", "keywords": ["head", "dizziness", "general", "heavy", "neck"], "desc": "High blood pressure requiring monitoring.", "specialty": "Cardiologist", "medicine_id": 3},
            {"name": "Angina Pectoris", "keywords": ["chest", "squeezing", "effort", "pressure"], "desc": "Chest pain caused by reduced blood flow to the heart.", "specialty": "Cardiologist", "medicine_id": 24},
            {"name": "Heart Attack (MI)", "keywords": ["chest", "crushing", "radiate", "jaw", "arm", "sweat"], "desc": "CRITICAL: Blockage of blood flow to the heart. CALL AMBULANCE.", "specialty": "Cardiologist", "medicine_id": 11},
            {"name": "Arrhythmia", "keywords": ["chest", "fluttering", "palpitations", "racing"], "desc": "Improper beating of the heart, whether too fast or too slow.", "specialty": "Cardiologist", "medicine_id": 25},

            # -- LUNGS --
            {"name": "Asthma", "keywords": ["chest", "wheezing", "breath", "cough", "tightness"], "desc": "Airways narrow and swell producing extra mucus.", "specialty": "Pulmonologist", "medicine_id": 16},
            {"name": "Acute Bronchitis", "keywords": ["chest", "cough", "mucus", "fatigue", "fever"], "desc": "Inflammation of the lining of bronchial tubes.", "specialty": "General Practitioner", "medicine_id": 5},
            {"name": "Pneumonia", "keywords": ["chest", "fever", "chills", "cough", "breath"], "desc": "Infection that inflames air sacs in one or both lungs.", "specialty": "Pulmonologist", "medicine_id": 26},
            {"name": "COPD", "keywords": ["chest", "breath", "chronic", "cough", "smoke"], "desc": "Chronic inflammatory lung disease that causes obstructed airflow.", "specialty": "Pulmonologist", "medicine_id": 16},

            # -- DIGESTION --
            {"name": "GERD / Acid Reflux", "keywords": ["chest", "burning", "stomach", "heartburn", "acid"], "desc": "Stomach acid irritates the food pipe lining.", "specialty": "Gastroenterologist", "medicine_id": 4},
            {"name": "Appendicitis", "keywords": ["stomach", "lower right", "vomiting", "fever", "sharp"], "desc": "Inflammation of the appendix. Emergency surgery required.", "specialty": "Surgeon", "medicine_id": 12},
            {"name": "Food Poisoning", "keywords": ["stomach", "cramping", "diarrhea", "vomiting"], "desc": "Illness caused by bacteria/toxins in food.", "specialty": "General Practitioner", "medicine_id": 13},
            {"name": "Gastritis", "keywords": ["stomach", "burning", "nausea", "fullness"], "desc": "Inflammation of the protective lining of the stomach.", "specialty": "Gastroenterologist", "medicine_id": 4},
            {"name": "IBS (Irritable Bowel)", "keywords": ["stomach", "cramping", "bloating", "gas", "constipation"], "desc": "Common disorder affecting the large intestine.", "specialty": "Gastroenterologist", "medicine_id": 27},
            {"name": "Gallstones", "keywords": ["stomach", "upper right", "pain", "fatty", "nausea"], "desc": "Hardened deposits of digestive fluid in the gallbladder.", "specialty": "Surgeon", "medicine_id": 12},

            # -- SKIN --
            {"name": "Eczema (Atopic Dermatitis)", "keywords": ["skin", "itchy", "red", "patches", "dry"], "desc": "Condition making skin red and itchy.", "specialty": "Dermatologist", "medicine_id": 8},
            {"name": "Acne Vulgaris", "keywords": ["skin", "pimples", "face", "oily", "spots"], "desc": "Hair follicles plug with oil and dead skin cells.", "specialty": "Dermatologist", "medicine_id": 17},
            {"name": "Tinea Corporis (Ringworm)", "keywords": ["skin", "ring", "itchy", "rash", "circular"], "desc": "Skin disease caused by fungus.", "specialty": "Dermatologist", "medicine_id": 18},
            {"name": "Psoriasis", "keywords": ["skin", "scaly", "silver", "patches", "dry"], "desc": "Skin cells build up and form scales and itchy, dry patches.", "specialty": "Dermatologist", "medicine_id": 8},
            {"name": "Urticaria (Hives)", "keywords": ["skin", "welts", "itchy", "raised", "allergy"], "desc": "Skin rash triggered by a reaction to food, medicine, or other irritants.", "specialty": "Dermatologist", "medicine_id": 9},

            # -- ORTHO --
            {"name": "Gout", "keywords": ["limbs", "joint", "red", "hot", "swollen", "toe"], "desc": "Arthritis characterized by severe pain/redness in joints, often the big toe.", "specialty": "Rheumatologist", "medicine_id": 6},
            {"name": "Muscle Strain", "keywords": ["limbs", "muscle", "sports", "activity", "pull"], "desc": "Injury to a muscle or a tendon.", "specialty": "Orthopedist", "medicine_id": 7},
            {"name": "Fracture", "keywords": ["limbs", "bone", "snap", "severe pain", "deformity"], "desc": "A broken bone. Requires X-ray and casting.", "specialty": "Orthopedist", "medicine_id": 12},
            {"name": "Osteoarthritis", "keywords": ["limbs", "joint", "stiff", "knee", "aging"], "desc": "Wear and tear arthritis.", "specialty": "Orthopedist", "medicine_id": 6},
            {"name": "Sciatica", "keywords": ["limbs", "nerve", "shooting", "leg", "back"], "desc": "Pain radiating along the sciatic nerve.", "specialty": "Neurologist", "medicine_id": 28},

            # -- INFECTIONS / GENERAL --
            {"name": "Dengue Fever", "keywords": ["general", "high fever", "body aches", "rash", "eyes"], "desc": "Mosquito-borne viral disease causing severe flu-like symptoms.", "specialty": "Internist", "medicine_id": 2},
            {"name": "Common Cold", "keywords": ["general", "sneeze", "runny nose", "sore throat"], "desc": "Viral infection of nose and throat.", "specialty": "General Practitioner", "medicine_id": 5},
            {"name": "Influenza (Flu)", "keywords": ["general", "fever", "fatigue", "aches", "cough"], "desc": "Viral infection attacking the respiratory system.", "specialty": "General Practitioner", "medicine_id": 29},
            {"name": "Typhoid Fever", "keywords": ["general", "fever", "stomach", "headache", "weakness"], "desc": "Bacterial infection caused by Salmonella typhi.", "specialty": "Internist", "medicine_id": 20},
            {"name": "Malaria", "keywords": ["general", "shaking chills", "fever", "sweating"], "desc": "Disease caused by a plasmodium parasite, transmitted by mosquitoes.", "specialty": "Internist", "medicine_id": 30},
            {"name": "Diabetes Type 2", "keywords": ["general", "thirst", "fatigue", "urination", "hunger"], "desc": "Chronic condition affecting sugar processing.", "specialty": "Internist", "medicine_id": 19},

            # -- MENTAL HEALTH --
            {"name": "Generalized Anxiety", "keywords": ["head", "panic", "worry", "heart", "fear"], "desc": "Intense, excessive and persistent worry and fear.", "specialty": "Psychiatrist", "medicine_id": 21},
            {"name": "Major Depression", "keywords": ["head", "sadness", "hopeless", "fatigue", "sleep"], "desc": "Mood disorder causing persistent sadness and loss of interest.", "specialty": "Psychiatrist", "medicine_id": 21},
            {"name": "Insomnia", "keywords": ["head", "sleep", "awake", "tired"], "desc": "Habitual sleeplessness or inability to sleep.", "specialty": "Psychiatrist", "medicine_id": 31},

            # -- DENTAL --
            {"name": "Pulpitis (Deep Cavity)", "keywords": ["mouth", "tooth", "pain", "sensitive", "gum"], "desc": "Inflammation of dental pulp tissue. Needs root canal or filling.", "specialty": "Dentist", "medicine_id": 22},
            {"name": "Gingivitis", "keywords": ["mouth", "gum", "bleed", "swollen", "red"], "desc": "Gum disease causing irritation/redness.", "specialty": "Dentist", "medicine_id": 23},
            {"name": "Dental Abscess", "keywords": ["mouth", "swollen jaw", "pus", "severe pain"], "desc": "Pocket of pus caused by bacterial infection.", "specialty": "Dentist", "medicine_id": 26},

            # -- EYES --
            {"name": "Conjunctivitis (Pink Eye)", "keywords": ["eyes", "red", "pink", "itchy", "crust"], "desc": "Inflammation or infection of the outer membrane of the eyeball.", "specialty": "Ophthalmologist", "medicine_id": 32},
            {"name": "Dry Eye Syndrome", "keywords": ["eyes", "dry", "gritty", "burning"], "desc": "Eyes don't produce enough tears.", "specialty": "Ophthalmologist", "medicine_id": 33},

            # -- URO/GYN --
            {"name": "UTI (Urinary Tract Infection)", "keywords": ["uro_gyn", "painful urination", "frequent", "burning"], "desc": "Infection in any part of the urinary system.", "specialty": "Urologist", "medicine_id": 20},
            {"name": "Kidney Stones", "keywords": ["uro_gyn", "severe back pain", "blood urine", "nausea"], "desc": "Hard deposits made of minerals and salts forming inside kidneys.", "specialty": "Urologist", "medicine_id": 6},
        ],

        # 3. DOCTOR DATABASE (13 Specialties x 10 Doctors minimum = 130+ Doctors)
        # Using DiceBear for "Cartoon Doctor Style"
        "doctors": [
            # --- 1. GENERAL PRACTITIONERS (IDs 100+) ---
            {"id": 100, "name": "Dr. Budi Santoso", "specialty": "General Practitioner", "hospital": "Klinik Sehat Jakarta", "rating": 4.5, "price": 75000, "image": get_avatar("Dr. Budi Santoso")},
            {"id": 101, "name": "Dr. Siti Aminah", "specialty": "General Practitioner", "hospital": "Puskesmas Tebet", "rating": 4.6, "price": 50000, "image": get_avatar("Dr. Siti Aminah", "female")},
            {"id": 102, "name": "Dr. Kevin Wijaya", "specialty": "General Practitioner", "hospital": "Klinik 24 Jam", "rating": 4.4, "price": 85000, "image": get_avatar("Dr. Kevin Wijaya")},
            {"id": 103, "name": "Dr. Rina Wati", "specialty": "General Practitioner", "hospital": "RSUD Bekasi", "rating": 4.7, "price": 90000, "image": get_avatar("Dr. Rina Wati", "female")},
            {"id": 104, "name": "Dr. Asep Sunarya", "specialty": "General Practitioner", "hospital": "Klinik Keluarga", "rating": 4.3, "price": 60000, "image": get_avatar("Dr. Asep Sunarya")},
            {"id": 105, "name": "Dr. Dewi Lestari", "specialty": "General Practitioner", "hospital": "Mayapada Clinic", "rating": 4.8, "price": 120000, "image": get_avatar("Dr. Dewi Lestari", "female")},
            {"id": 106, "name": "Dr. Joko Anwar", "specialty": "General Practitioner", "hospital": "Klinik Pratama", "rating": 4.5, "price": 70000, "image": get_avatar("Dr. Joko Anwar")},
            {"id": 107, "name": "Dr. Putri Indah", "specialty": "General Practitioner", "hospital": "RS Hermina", "rating": 4.6, "price": 100000, "image": get_avatar("Dr. Putri Indah", "female")},
            {"id": 108, "name": "Dr. Bayu Saputra", "specialty": "General Practitioner", "hospital": "Halodoc Online", "rating": 4.9, "price": 45000, "image": get_avatar("Dr. Bayu Saputra")},
            {"id": 109, "name": "Dr. Mega Sari", "specialty": "General Practitioner", "hospital": "Klinik Kimia Farma", "rating": 4.7, "price": 80000, "image": get_avatar("Dr. Mega Sari", "female")},

            # --- 2. NEUROLOGISTS (IDs 200+) ---
            {"id": 200, "name": "Dr. Sarah Sp.S", "specialty": "Neurologist", "hospital": "RS Siloam", "rating": 4.9, "price": 250000, "image": get_avatar("Dr. Sarah Sp.S", "female")},
            {"id": 201, "name": "Dr. Bambang Sp.S", "specialty": "Neurologist", "hospital": "RSCM Kencana", "rating": 4.8, "price": 300000, "image": get_avatar("Dr. Bambang Sp.S")},
            {"id": 202, "name": "Dr. Jenny Lee Sp.S", "specialty": "Neurologist", "hospital": "RS Pondok Indah", "rating": 4.8, "price": 350000, "image": get_avatar("Dr. Jenny Lee Sp.S", "female")},
            {"id": 203, "name": "Dr. Handoko Sp.S", "specialty": "Neurologist", "hospital": "RS Mitra Keluarga", "rating": 4.7, "price": 275000, "image": get_avatar("Dr. Handoko Sp.S")},
            {"id": 204, "name": "Dr. Clara Sp.S", "specialty": "Neurologist", "hospital": "RS Mayapada", "rating": 4.9, "price": 320000, "image": get_avatar("Dr. Clara Sp.S", "female")},
            {"id": 205, "name": "Dr. Donny Sp.S", "specialty": "Neurologist", "hospital": "RS Carolus", "rating": 4.6, "price": 240000, "image": get_avatar("Dr. Donny Sp.S")},
            {"id": 206, "name": "Dr. Fiona Sp.S", "specialty": "Neurologist", "hospital": "RSPI Puri", "rating": 4.8, "price": 290000, "image": get_avatar("Dr. Fiona Sp.S", "female")},
            {"id": 207, "name": "Dr. Gunawan Sp.S", "specialty": "Neurologist", "hospital": "National Brain Center", "rating": 5.0, "price": 400000, "image": get_avatar("Dr. Gunawan Sp.S")},
            {"id": 208, "name": "Dr. Hesti Sp.S", "specialty": "Neurologist", "hospital": "RS Fatmawati", "rating": 4.5, "price": 200000, "image": get_avatar("Dr. Hesti Sp.S", "female")},
            {"id": 209, "name": "Dr. Indra Sp.S", "specialty": "Neurologist", "hospital": "RS Gading Pluit", "rating": 4.7, "price": 260000, "image": get_avatar("Dr. Indra Sp.S")},

            # --- 3. CARDIOLOGISTS (IDs 300+) ---
            {"id": 300, "name": "Dr. Andi Sp.JP", "specialty": "Cardiologist", "hospital": "RS Harapan Kita", "rating": 5.0, "price": 350000, "image": get_avatar("Dr. Andi Sp.JP")},
            {"id": 301, "name": "Dr. Maya Putri Sp.JP", "specialty": "Cardiologist", "hospital": "Siloam Heart Center", "rating": 4.9, "price": 400000, "image": get_avatar("Dr. Maya Putri Sp.JP", "female")},
            {"id": 302, "name": "Dr. Robert Hartono Sp.JP", "specialty": "Cardiologist", "hospital": "RS Medistra", "rating": 4.9, "price": 450000, "image": get_avatar("Dr. Robert Hartono Sp.JP")},
            {"id": 303, "name": "Dr. Sisca Sp.JP", "specialty": "Cardiologist", "hospital": "RS Premier Jatinegara", "rating": 4.7, "price": 300000, "image": get_avatar("Dr. Sisca Sp.JP", "female")},
            {"id": 304, "name": "Dr. Taufik Sp.JP", "specialty": "Cardiologist", "hospital": "RS MMC", "rating": 4.8, "price": 380000, "image": get_avatar("Dr. Taufik Sp.JP")},
            {"id": 305, "name": "Dr. Vina Sp.JP", "specialty": "Cardiologist", "hospital": "RS Husada", "rating": 4.6, "price": 280000, "image": get_avatar("Dr. Vina Sp.JP", "female")},
            {"id": 306, "name": "Dr. William Sp.JP", "specialty": "Cardiologist", "hospital": "RS PIK", "rating": 4.9, "price": 420000, "image": get_avatar("Dr. William Sp.JP")},
            {"id": 307, "name": "Dr. Yulia Sp.JP", "specialty": "Cardiologist", "hospital": "RS Gandaria", "rating": 4.7, "price": 310000, "image": get_avatar("Dr. Yulia Sp.JP", "female")},
            {"id": 308, "name": "Dr. Zainal Sp.JP", "specialty": "Cardiologist", "hospital": "RS Pasar Rebo", "rating": 4.5, "price": 250000, "image": get_avatar("Dr. Zainal Sp.JP")},
            {"id": 309, "name": "Dr. Elly Sp.JP", "specialty": "Cardiologist", "hospital": "RS Abdi Waluyo", "rating": 4.8, "price": 360000, "image": get_avatar("Dr. Elly Sp.JP", "female")},

            # --- 4. GASTROENTEROLOGISTS (IDs 400+) ---
            {"id": 400, "name": "Dr. Citra Sp.PD-KGEH", "specialty": "Gastroenterologist", "hospital": "RS Pondok Indah", "rating": 4.8, "price": 350000, "image": get_avatar("Dr. Citra Sp.PD-KGEH", "female")},
            {"id": 401, "name": "Dr. Hendra Sp.PD-KGEH", "specialty": "Gastroenterologist", "hospital": "RSCM Kencana", "rating": 4.9, "price": 400000, "image": get_avatar("Dr. Hendra Sp.PD-KGEH")},
            {"id": 402, "name": "Dr. Bernard Sp.PD", "specialty": "Gastroenterologist", "hospital": "Siloam Kebon Jeruk", "rating": 4.7, "price": 300000, "image": get_avatar("Dr. Bernard Sp.PD")},
            {"id": 403, "name": "Dr. Diana Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS Puri Indah", "rating": 4.8, "price": 320000, "image": get_avatar("Dr. Diana Sp.PD", "female")},
            {"id": 404, "name": "Dr. Edward Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS Pluit", "rating": 4.6, "price": 280000, "image": get_avatar("Dr. Edward Sp.PD")},
            {"id": 405, "name": "Dr. Farida Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS Jakarta", "rating": 4.7, "price": 290000, "image": get_avatar("Dr. Farida Sp.PD", "female")},
            {"id": 406, "name": "Dr. Gerry Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS Omni", "rating": 4.5, "price": 250000, "image": get_avatar("Dr. Gerry Sp.PD")},
            {"id": 407, "name": "Dr. Hanny Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS YPK", "rating": 4.8, "price": 310000, "image": get_avatar("Dr. Hanny Sp.PD", "female")},
            {"id": 408, "name": "Dr. Iwan Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS Antam", "rating": 4.6, "price": 260000, "image": get_avatar("Dr. Iwan Sp.PD")},
            {"id": 409, "name": "Dr. Julia Sp.PD", "specialty": "Gastroenterologist", "hospital": "RS Kramat 128", "rating": 4.7, "price": 275000, "image": get_avatar("Dr. Julia Sp.PD", "female")},

            # --- 5. DERMATOLOGISTS (IDs 500+) ---
            {"id": 500, "name": "Dr. Fani Sp.KK", "specialty": "Dermatologist", "hospital": "Erha Clinic", "rating": 4.6, "price": 250000, "image": get_avatar("Dr. Fani Sp.KK", "female")},
            {"id": 501, "name": "Dr. Jessica Sp.KK", "specialty": "Dermatologist", "hospital": "Miracle Clinic", "rating": 4.9, "price": 350000, "image": get_avatar("Dr. Jessica Sp.KK", "female")},
            {"id": 502, "name": "Dr. Kevin Sp.KK", "specialty": "Dermatologist", "hospital": "Natasha Skin Care", "rating": 4.7, "price": 200000, "image": get_avatar("Dr. Kevin Sp.KK")},
            {"id": 503, "name": "Dr. Lilis Sp.KK", "specialty": "Dermatologist", "hospital": "Bamed Skin Care", "rating": 4.8, "price": 300000, "image": get_avatar("Dr. Lilis Sp.KK", "female")},
            {"id": 504, "name": "Dr. Mike Sp.KK", "specialty": "Dermatologist", "hospital": "ZAP Clinic", "rating": 4.5, "price": 180000, "image": get_avatar("Dr. Mike Sp.KK")},
            {"id": 505, "name": "Dr. Nina Sp.KK", "specialty": "Dermatologist", "hospital": "RS Siloam TB", "rating": 4.9, "price": 320000, "image": get_avatar("Dr. Nina Sp.KK", "female")},
            {"id": 506, "name": "Dr. Oscar Sp.KK", "specialty": "Dermatologist", "hospital": "Jakarta Skin Center", "rating": 4.8, "price": 400000, "image": get_avatar("Dr. Oscar Sp.KK")},
            {"id": 507, "name": "Dr. Priska Sp.KK", "specialty": "Dermatologist", "hospital": "RS Cinta Kasih", "rating": 4.6, "price": 220000, "image": get_avatar("Dr. Priska Sp.KK", "female")},
            {"id": 508, "name": "Dr. Qory Sp.KK", "specialty": "Dermatologist", "hospital": "Klinik Estetika", "rating": 4.7, "price": 275000, "image": get_avatar("Dr. Qory Sp.KK", "female")},
            {"id": 509, "name": "Dr. Riko Sp.KK", "specialty": "Dermatologist", "hospital": "RS Pelni", "rating": 4.5, "price": 210000, "image": get_avatar("Dr. Riko Sp.KK")},

            # --- 6. ORTHOPEDISTS (IDs 600+) ---
            {"id": 600, "name": "Dr. Gunawan Sp.OT", "specialty": "Orthopedist", "hospital": "RS Fatmawati", "rating": 4.8, "price": 220000, "image": get_avatar("Dr. Gunawan Sp.OT")},
            {"id": 601, "name": "Dr. Henry Sp.OT", "specialty": "Orthopedist", "hospital": "RS Siaga Raya", "rating": 4.9, "price": 300000, "image": get_avatar("Dr. Henry Sp.OT")},
            {"id": 602, "name": "Dr. Imam Sp.OT", "specialty": "Orthopedist", "hospital": "RS EMC", "rating": 4.7, "price": 280000, "image": get_avatar("Dr. Imam Sp.OT")},
            {"id": 603, "name": "Dr. Johny Sp.OT", "specialty": "Orthopedist", "hospital": "RS Premier Bintaro", "rating": 4.8, "price": 320000, "image": get_avatar("Dr. Johny Sp.OT")},
            {"id": 604, "name": "Dr. Kiki Sp.OT", "specialty": "Orthopedist", "hospital": "RS Columbia", "rating": 4.6, "price": 250000, "image": get_avatar("Dr. Kiki Sp.OT", "female")},
            {"id": 605, "name": "Dr. Lukman Sp.OT", "specialty": "Orthopedist", "hospital": "RS Mitra Kelapa Gading", "rating": 4.9, "price": 350000, "image": get_avatar("Dr. Lukman Sp.OT")},
            {"id": 606, "name": "Dr. Maman Sp.OT", "specialty": "Orthopedist", "hospital": "RS UKI", "rating": 4.5, "price": 200000, "image": get_avatar("Dr. Maman Sp.OT")},
            {"id": 607, "name": "Dr. Nurdin Sp.OT", "specialty": "Orthopedist", "hospital": "RS Islam", "rating": 4.7, "price": 230000, "image": get_avatar("Dr. Nurdin Sp.OT")},
            {"id": 608, "name": "Dr. Opik Sp.OT", "specialty": "Orthopedist", "hospital": "RS Persahabatan", "rating": 4.8, "price": 260000, "image": get_avatar("Dr. Opik Sp.OT")},
            {"id": 609, "name": "Dr. Paul Sp.OT", "specialty": "Orthopedist", "hospital": "RS Siloam Asri", "rating": 4.9, "price": 330000, "image": get_avatar("Dr. Paul Sp.OT")},

            # --- 7. ENT (THT) SPECIALISTS (IDs 700+) ---
            {"id": 700, "name": "Dr. Hani Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Hermina", "rating": 4.7, "price": 175000, "image": get_avatar("Dr. Hani Sp.THT", "female")},
            {"id": 701, "name": "Dr. Rahmat Sp.THT", "specialty": "ENT Specialist", "hospital": "RS THT Proklamasi", "rating": 4.9, "price": 300000, "image": get_avatar("Dr. Rahmat Sp.THT")},
            {"id": 702, "name": "Dr. Susan Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Evasari", "rating": 4.8, "price": 250000, "image": get_avatar("Dr. Susan Sp.THT", "female")},
            {"id": 703, "name": "Dr. Tommy Sp.THT", "specialty": "ENT Specialist", "hospital": "RS SS Medika", "rating": 4.6, "price": 200000, "image": get_avatar("Dr. Tommy Sp.THT")},
            {"id": 704, "name": "Dr. Uli Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Mitra Jatinegara", "rating": 4.7, "price": 220000, "image": get_avatar("Dr. Uli Sp.THT", "female")},
            {"id": 705, "name": "Dr. Vicky Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Kartika", "rating": 4.5, "price": 180000, "image": get_avatar("Dr. Vicky Sp.THT")},
            {"id": 706, "name": "Dr. Wawan Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Prikasih", "rating": 4.8, "price": 260000, "image": get_avatar("Dr. Wawan Sp.THT")},
            {"id": 707, "name": "Dr. Xena Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Yadika", "rating": 4.6, "price": 210000, "image": get_avatar("Dr. Xena Sp.THT", "female")},
            {"id": 708, "name": "Dr. Yanto Sp.THT", "specialty": "ENT Specialist", "hospital": "RS Tebet", "rating": 4.7, "price": 230000, "image": get_avatar("Dr. Yanto Sp.THT")},
            {"id": 709, "name": "Dr. Zara Sp.THT", "specialty": "ENT Specialist", "hospital": "RS MRCCC", "rating": 4.9, "price": 320000, "image": get_avatar("Dr. Zara Sp.THT", "female")},

            # --- 8. PEDIATRICIANS (IDs 800+) ---
            {"id": 800, "name": "Dr. Anak Agung Sp.A", "specialty": "Pediatrician", "hospital": "RS Bunda Menteng", "rating": 4.9, "price": 350000, "image": get_avatar("Dr. Anak Agung Sp.A")},
            {"id": 801, "name": "Dr. Melati Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Grand Family", "rating": 4.8, "price": 300000, "image": get_avatar("Dr. Melati Sp.A", "female")},
            {"id": 802, "name": "Dr. Candra Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Hermina", "rating": 4.7, "price": 280000, "image": get_avatar("Dr. Candra Sp.A")},
            {"id": 803, "name": "Dr. Dian Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Evasari", "rating": 4.8, "price": 290000, "image": get_avatar("Dr. Dian Sp.A", "female")},
            {"id": 804, "name": "Dr. Frans Sp.A", "specialty": "Pediatrician", "hospital": "RSIA YPK", "rating": 4.6, "price": 250000, "image": get_avatar("Dr. Frans Sp.A")},
            {"id": 805, "name": "Dr. Galuh Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Kemang", "rating": 4.9, "price": 330000, "image": get_avatar("Dr. Galuh Sp.A", "female")},
            {"id": 806, "name": "Dr. Haris Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Tambak", "rating": 4.7, "price": 270000, "image": get_avatar("Dr. Haris Sp.A")},
            {"id": 807, "name": "Dr. Indah Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Brawijaya", "rating": 4.8, "price": 310000, "image": get_avatar("Dr. Indah Sp.A", "female")},
            {"id": 808, "name": "Dr. Johan Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Sammarie", "rating": 4.6, "price": 260000, "image": get_avatar("Dr. Johan Sp.A")},
            {"id": 809, "name": "Dr. Kartini Sp.A", "specialty": "Pediatrician", "hospital": "RSIA Asih", "rating": 4.7, "price": 285000, "image": get_avatar("Dr. Kartini Sp.A", "female")},

            # --- 9. DENTISTS (IDs 900+) ---
            {"id": 900, "name": "Drg. Lita", "specialty": "Dentist", "hospital": "Dental City", "rating": 4.8, "price": 400000, "image": get_avatar("Drg. Lita", "female")},
            {"id": 901, "name": "Drg. Made", "specialty": "Dentist", "hospital": "Bali Dental", "rating": 4.9, "price": 450000, "image": get_avatar("Drg. Made")},
            {"id": 902, "name": "Drg. Nurul", "specialty": "Dentist", "hospital": "Audy Dental", "rating": 4.7, "price": 350000, "image": get_avatar("Drg. Nurul", "female")},
            {"id": 903, "name": "Drg. Oki", "specialty": "Dentist", "hospital": "O-Smile", "rating": 4.6, "price": 300000, "image": get_avatar("Drg. Oki")},
            {"id": 904, "name": "Drg. Paula", "specialty": "Dentist", "hospital": "Pals Dental", "rating": 4.8, "price": 380000, "image": get_avatar("Drg. Paula", "female")},
            {"id": 905, "name": "Drg. Qinan", "specialty": "Dentist", "hospital": "Q-Dental", "rating": 4.7, "price": 320000, "image": get_avatar("Drg. Qinan", "female")},
            {"id": 906, "name": "Drg. Reza", "specialty": "Dentist", "hospital": "R-Dental", "rating": 4.9, "price": 420000, "image": get_avatar("Drg. Reza")},
            {"id": 907, "name": "Drg. Sinta", "specialty": "Dentist", "hospital": "S-Dental", "rating": 4.5, "price": 280000, "image": get_avatar("Drg. Sinta", "female")},
            {"id": 908, "name": "Drg. Tio", "specialty": "Dentist", "hospital": "T-Dental", "rating": 4.6, "price": 310000, "image": get_avatar("Drg. Tio")},
            {"id": 909, "name": "Drg. Umar", "specialty": "Dentist", "hospital": "U-Dental", "rating": 4.8, "price": 360000, "image": get_avatar("Drg. Umar")},

            # --- 10. PSYCHIATRISTS (IDs 1000+) ---
            {"id": 1000, "name": "Dr. Vira Sp.KJ", "specialty": "Psychiatrist", "hospital": "RSJ Dharmawangsa", "rating": 4.9, "price": 500000, "image": get_avatar("Dr. Vira Sp.KJ", "female")},
            {"id": 1001, "name": "Dr. Wira Sp.KJ", "specialty": "Psychiatrist", "hospital": "RSJ Grogol", "rating": 4.8, "price": 350000, "image": get_avatar("Dr. Wira Sp.KJ")},
            {"id": 1002, "name": "Dr. Xander Sp.KJ", "specialty": "Psychiatrist", "hospital": "Klinik Anggrek", "rating": 4.7, "price": 400000, "image": get_avatar("Dr. Xander Sp.KJ")},
            {"id": 1003, "name": "Dr. Yola Sp.KJ", "specialty": "Psychiatrist", "hospital": "RS Omni Alam Sutera", "rating": 4.8, "price": 450000, "image": get_avatar("Dr. Yola Sp.KJ", "female")},
            {"id": 1004, "name": "Dr. Zaki Sp.KJ", "specialty": "Psychiatrist", "hospital": "RS Pondok Indah Bintaro", "rating": 4.9, "price": 550000, "image": get_avatar("Dr. Zaki Sp.KJ")},
            {"id": 1005, "name": "Dr. Andre Sp.KJ", "specialty": "Psychiatrist", "hospital": "Siloam Lippo", "rating": 4.6, "price": 380000, "image": get_avatar("Dr. Andre Sp.KJ")},
            {"id": 1006, "name": "Dr. Bella Sp.KJ", "specialty": "Psychiatrist", "hospital": "Mayapada Kuningan", "rating": 4.7, "price": 420000, "image": get_avatar("Dr. Bella Sp.KJ", "female")},
            {"id": 1007, "name": "Dr. Citra Sp.KJ", "specialty": "Psychiatrist", "hospital": "RSCM Kencana", "rating": 4.9, "price": 480000, "image": get_avatar("Dr. Citra Sp.KJ", "female")},
            {"id": 1008, "name": "Dr. Dedi Sp.KJ", "specialty": "Psychiatrist", "hospital": "RS Carolus", "rating": 4.5, "price": 350000, "image": get_avatar("Dr. Dedi Sp.KJ")},
            {"id": 1009, "name": "Dr. Eni Sp.KJ", "specialty": "Psychiatrist", "hospital": "RS Fatmawati", "rating": 4.7, "price": 370000, "image": get_avatar("Dr. Eni Sp.KJ", "female")},

            # --- 11. PULMONOLOGISTS (IDs 1100+) ---
            {"id": 1100, "name": "Dr. Lina Sp.P", "specialty": "Pulmonologist", "hospital": "RS Persahabatan", "rating": 4.9, "price": 250000, "image": get_avatar("Dr. Lina Sp.P", "female")},
            {"id": 1101, "name": "Dr. Burhan Sp.P", "specialty": "Pulmonologist", "hospital": "RSPI Sulianti", "rating": 4.8, "price": 280000, "image": get_avatar("Dr. Burhan Sp.P")},
            {"id": 1102, "name": "Dr. Agus Sp.P", "specialty": "Pulmonologist", "hospital": "RS Pertamina", "rating": 4.7, "price": 240000, "image": get_avatar("Dr. Agus Sp.P")},
            {"id": 1103, "name": "Dr. Erlina Sp.P", "specialty": "Pulmonologist", "hospital": "RS Persahabatan", "rating": 5.0, "price": 300000, "image": get_avatar("Dr. Erlina Sp.P", "female")},
            {"id": 1104, "name": "Dr. Faisal Sp.P", "specialty": "Pulmonologist", "hospital": "RS Columbia", "rating": 4.6, "price": 220000, "image": get_avatar("Dr. Faisal Sp.P")},
            {"id": 1105, "name": "Dr. Gita Sp.P", "specialty": "Pulmonologist", "hospital": "RS Antam", "rating": 4.8, "price": 260000, "image": get_avatar("Dr. Gita Sp.P", "female")},
            {"id": 1106, "name": "Dr. Heru Sp.P", "specialty": "Pulmonologist", "hospital": "RS Polri", "rating": 4.5, "price": 200000, "image": get_avatar("Dr. Heru Sp.P")},
            {"id": 1107, "name": "Dr. Indah Sp.P", "specialty": "Pulmonologist", "hospital": "RS Haji", "rating": 4.7, "price": 230000, "image": get_avatar("Dr. Indah Sp.P", "female")},
            {"id": 1108, "name": "Dr. Joni Sp.P", "specialty": "Pulmonologist", "hospital": "RS UKI", "rating": 4.6, "price": 210000, "image": get_avatar("Dr. Joni Sp.P")},
            {"id": 1109, "name": "Dr. Kiki Sp.P", "specialty": "Pulmonologist", "hospital": "RS Hermina", "rating": 4.8, "price": 270000, "image": get_avatar("Dr. Kiki Sp.P", "female")},

            # --- 12. OPHTHALMOLOGISTS (IDs 1200+) ---
            {"id": 1200, "name": "Dr. Maya Sp.M", "specialty": "Ophthalmologist", "hospital": "JEC Eye Hospital", "rating": 4.9, "price": 350000, "image": get_avatar("Dr. Maya Sp.M", "female")},
            {"id": 1201, "name": "Dr. Hadi Sp.M", "specialty": "Ophthalmologist", "hospital": "KMN EyeCare", "rating": 4.8, "price": 300000, "image": get_avatar("Dr. Hadi Sp.M")},
            {"id": 1202, "name": "Dr. Susi Sp.M", "specialty": "Ophthalmologist", "hospital": "Cicendo Eye Hospital", "rating": 4.9, "price": 250000, "image": get_avatar("Dr. Susi Sp.M", "female")},
            {"id": 1203, "name": "Dr. Budi Sp.M", "specialty": "Ophthalmologist", "hospital": "RS Aini", "rating": 4.7, "price": 280000, "image": get_avatar("Dr. Budi Sp.M")},
            {"id": 1204, "name": "Dr. Citra Sp.M", "specialty": "Ophthalmologist", "hospital": "Siloam Eye", "rating": 4.8, "price": 320000, "image": get_avatar("Dr. Citra Sp.M", "female")},
            {"id": 1205, "name": "Dr. Doni Sp.M", "specialty": "Ophthalmologist", "hospital": "SMEC", "rating": 4.6, "price": 200000, "image": get_avatar("Dr. Doni Sp.M")},
            {"id": 1206, "name": "Dr. Eka Sp.M", "specialty": "Ophthalmologist", "hospital": "VIO Optical", "rating": 4.7, "price": 220000, "image": get_avatar("Dr. Eka Sp.M", "female")},
            {"id": 1207, "name": "Dr. Feri Sp.M", "specialty": "Ophthalmologist", "hospital": "RS Fatmawati", "rating": 4.5, "price": 180000, "image": get_avatar("Dr. Feri Sp.M")},
            {"id": 1208, "name": "Dr. Gina Sp.M", "specialty": "Ophthalmologist", "hospital": "RS Premier", "rating": 4.8, "price": 290000, "image": get_avatar("Dr. Gina Sp.M", "female")},
            {"id": 1209, "name": "Dr. Hari Sp.M", "specialty": "Ophthalmologist", "hospital": "JEC Menteng", "rating": 4.9, "price": 400000, "image": get_avatar("Dr. Hari Sp.M")},

            # --- 13. UROLOGISTS (IDs 1300+) ---
            {"id": 1300, "name": "Dr. Ponco Sp.U", "specialty": "Urologist", "hospital": "RS Asri Urologi", "rating": 4.9, "price": 400000, "image": get_avatar("Dr. Ponco Sp.U")},
            {"id": 1301, "name": "Dr. Rainy Sp.U", "specialty": "Urologist", "hospital": "RSCM Kencana", "rating": 4.8, "price": 350000, "image": get_avatar("Dr. Rainy Sp.U", "female")},
            {"id": 1302, "name": "Dr. Irfan Sp.U", "specialty": "Urologist", "hospital": "RS Bunda", "rating": 4.7, "price": 300000, "image": get_avatar("Dr. Irfan Sp.U")},
            {"id": 1303, "name": "Dr. Chaidir Sp.U", "specialty": "Urologist", "hospital": "RS Siloam", "rating": 4.9, "price": 380000, "image": get_avatar("Dr. Chaidir Sp.U")},
            {"id": 1304, "name": "Dr. Nur Sp.U", "specialty": "Urologist", "hospital": "RS Fatmawati", "rating": 4.6, "price": 250000, "image": get_avatar("Dr. Nur Sp.U", "female")},
            {"id": 1305, "name": "Dr. Agus Sp.U", "specialty": "Urologist", "hospital": "RS Persahabatan", "rating": 4.7, "price": 280000, "image": get_avatar("Dr. Agus Sp.U")},
            {"id": 1306, "name": "Dr. Bambang Sp.U", "specialty": "Urologist", "hospital": "RS Dharmais", "rating": 4.8, "price": 320000, "image": get_avatar("Dr. Bambang Sp.U")},
            {"id": 1307, "name": "Dr. Cici Sp.U", "specialty": "Urologist", "hospital": "RS Omni", "rating": 4.5, "price": 240000, "image": get_avatar("Dr. Cici Sp.U", "female")},
            {"id": 1308, "name": "Dr. Didi Sp.U", "specialty": "Urologist", "hospital": "RS Pelni", "rating": 4.6, "price": 260000, "image": get_avatar("Dr. Didi Sp.U")},
            {"id": 1309, "name": "Dr. Eddy Sp.U", "specialty": "Urologist", "hospital": "RS Mayapada", "rating": 4.9, "price": 420000, "image": get_avatar("Dr. Eddy Sp.U")},
        ],

        # 4. MEDICINES
        "medicines": [
            # Pain & Fever
            {"id": 1, "name": "Sumatriptan", "dosage": "50mg", "instruction": "Take 1 tablet at onset of migraine.", "times_per_day": 1, "default_times": ["09:00"]},
            {"id": 2, "name": "Paracetamol", "dosage": "500mg", "instruction": "Take 1-2 tablets every 6 hours for pain/fever.", "times_per_day": 3, "default_times": ["08:00", "14:00", "20:00"]},
            {"id": 7, "name": "Ibuprofen", "dosage": "400mg", "instruction": "Take 1 tablet every 8 hours after food.", "times_per_day": 3, "default_times": ["07:00", "15:00", "23:00"]},
            {"id": 6, "name": "Diclofenac Sodium", "dosage": "50mg", "instruction": "Take 1 tablet twice daily after food for joint pain.", "times_per_day": 2, "default_times": ["08:00", "20:00"]},
            {"id": 22, "name": "Mefenamic Acid", "dosage": "500mg", "instruction": "Take 1 tablet every 8 hours for tooth pain.", "times_per_day": 3, "default_times": ["07:00", "15:00", "23:00"]},
            {"id": 28, "name": "Gabapentin", "dosage": "300mg", "instruction": "Take 1 tablet at night for nerve pain.", "times_per_day": 1, "default_times": ["21:00"]},

            # Chronic & Cardio
            {"id": 3, "name": "Amlodipine", "dosage": "5mg", "instruction": "Take 1 tablet daily for BP.", "times_per_day": 1, "default_times": ["08:00"]},
            {"id": 11, "name": "Aspirin", "dosage": "81mg", "instruction": "EMERGENCY: Chew tablet immediately. Call Ambulance.", "times_per_day": 0, "default_times": []},
            {"id": 15, "name": "Simvastatin", "dosage": "20mg", "instruction": "Take 1 tablet at night for cholesterol.", "times_per_day": 1, "default_times": ["21:00"]},
            {"id": 24, "name": "Nitroglycerin", "dosage": "0.4mg", "instruction": "Place under tongue for chest pain.", "times_per_day": 0, "default_times": []},
            {"id": 25, "name": "Beta Blocker (Bisoprolol)", "dosage": "5mg", "instruction": "Take 1 tablet daily in the morning.", "times_per_day": 1, "default_times": ["08:00"]},
            
            # Respiratory
            {"id": 5, "name": "Pseudoephedrine", "dosage": "30mg", "instruction": "Take 1 tablet every 6 hours for congestion.", "times_per_day": 3, "default_times": ["08:00", "14:00", "20:00"]},
            {"id": 16, "name": "Salbutamol Inhaler", "dosage": "100mcg", "instruction": "2 puffs every 4-6 hours as needed.", "times_per_day": 4, "default_times": ["08:00", "12:00", "16:00", "20:00"]},
            {"id": 29, "name": "Oseltamivir", "dosage": "75mg", "instruction": "Take 1 tablet twice daily for 5 days.", "times_per_day": 2, "default_times": ["08:00", "20:00"]},
            
            # Digestive
            {"id": 4, "name": "Antacid Susp", "dosage": "10ml", "instruction": "Take 1 spoon 3 times a day before meals.", "times_per_day": 3, "default_times": ["07:00", "13:00", "19:00"]},
            {"id": 13, "name": "Oral Rehydration Salts", "dosage": "Sachet", "instruction": "Dissolve in 200ml water. Drink frequently.", "times_per_day": 4, "default_times": ["08:00", "12:00", "16:00", "20:00"]},
            {"id": 27, "name": "Hyoscine Butylbromide", "dosage": "10mg", "instruction": "Take 1 tablet for cramps as needed.", "times_per_day": 3, "default_times": ["08:00", "14:00", "20:00"]},
            
            # Skin
            {"id": 8, "name": "Hydrocortisone Cream", "dosage": "1%", "instruction": "Apply thin layer twice daily to rash.", "times_per_day": 2, "default_times": ["09:00", "21:00"]},
            {"id": 17, "name": "Benzoyl Peroxide", "dosage": "5%", "instruction": "Apply to acne spots once daily.", "times_per_day": 1, "default_times": ["21:00"]},
            {"id": 18, "name": "Ketoconazole Cream", "dosage": "2%", "instruction": "Apply to infected area twice daily.", "times_per_day": 2, "default_times": ["08:00", "20:00"]},

            # Infection / Antibiotics
            {"id": 20, "name": "Ciprofloxacin", "dosage": "500mg", "instruction": "Take 1 tablet every 12 hours (Antibiotic).", "times_per_day": 2, "default_times": ["08:00", "20:00"]},
            {"id": 26, "name": "Amoxicillin", "dosage": "500mg", "instruction": "Take 1 tablet every 8 hours. Finish course.", "times_per_day": 3, "default_times": ["07:00", "15:00", "23:00"]},
            {"id": 30, "name": "Artemisinin Combination", "dosage": "Tablet", "instruction": "Follow specific malaria protocol.", "times_per_day": 2, "default_times": ["08:00", "20:00"]},

            # Mental Health
            {"id": 21, "name": "Sertraline", "dosage": "50mg", "instruction": "Take 1 tablet daily in the morning.", "times_per_day": 1, "default_times": ["07:00"]},
            {"id": 31, "name": "Melatonin", "dosage": "3mg", "instruction": "Take 1 tablet 30 mins before sleep.", "times_per_day": 1, "default_times": ["22:00"]},

            # Dental / Eyes / Others
            {"id": 23, "name": "Chlorhexidine Mouthwash", "dosage": "15ml", "instruction": "Rinse twice daily.", "times_per_day": 2, "default_times": ["08:00", "20:00"]},
            {"id": 32, "name": "Chloramphenicol Eye Drops", "dosage": "0.5%", "instruction": "1 drop in affected eye every 4 hours.", "times_per_day": 4, "default_times": ["08:00", "12:00", "16:00", "20:00"]},
            {"id": 33, "name": "Artificial Tears", "dosage": "Drops", "instruction": "Apply as needed for dry eyes.", "times_per_day": 4, "default_times": ["09:00", "13:00", "17:00", "21:00"]},
            {"id": 9, "name": "Cetirizine", "dosage": "10mg", "instruction": "Take 1 tablet daily for allergies.", "times_per_day": 1, "default_times": ["21:00"]},
            {"id": 10, "name": "Oxymetazoline Spray", "dosage": "0.05%", "instruction": "Spray twice daily.", "times_per_day": 2, "default_times": ["08:00", "20:00"]},
            {"id": 12, "name": "Hospital Admission", "dosage": "N/A", "instruction": "Requires immediate hospital evaluation.", "times_per_day": 0, "default_times": []},
            {"id": 14, "name": "Betahistine", "dosage": "6mg", "instruction": "Take 1 tablet 3 times daily for vertigo.", "times_per_day": 3, "default_times": ["07:00", "13:00", "19:00"]},
            {"id": 19, "name": "Metformin", "dosage": "500mg", "instruction": "Take 1 tablet with dinner.", "times_per_day": 1, "default_times": ["19:00"]},
        ]
    }

    # Load existing users and chats to preserve them
    existing_users = []
    existing_chats = []
    
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                current_db = json.load(f)
                existing_users = current_db.get('users', [])
                existing_chats = current_db.get('chat_sessions', [])
        except:
            pass

    # Construct final DB
    data = {
        "users": existing_users,
        "chat_sessions": existing_chats,
        "medical_knowledge": medical_knowledge
    }
    
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[SUCCESS] Database Force Updated with {len(medical_knowledge['doctors'])} Doctors and {len(medical_knowledge['diseases'])} Diseases.")

if __name__ == "__main__":
    create_database()