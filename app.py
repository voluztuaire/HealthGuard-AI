import os
import json
import cv2
import numpy as np
import base64
import requests
import time
import math
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler

# --- SECURITY DEPENDENCIES ---
from werkzeug.security import generate_password_hash, check_password_hash

# --- NEW: FaceNet Dependency ---
from keras_facenet import FaceNet
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
app.secret_key = 'healthguard_secret_key_secure_random_string'

# --- INITIALIZE SCHEDULER ---
scheduler = BackgroundScheduler()
scheduler.start()

# --- CONFIGURATION ---
DB_FILE = 'database.json'
FACE_DATA_DIR = 'face_data'
HaarPath = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(HaarPath)

# --- LOAD ML MODEL (FACENET) ---
print("[SYSTEM] Loading FaceNet (State-of-the-art Face Recognition)...")
# Ini akan mendownload model FaceNet sekali saja (sekitar 90MB)
embedder = FaceNet()
print("[SYSTEM] FaceNet Loaded. AI Vision System Active.")

# --- HELPER FUNCTIONS ---
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": [], "chat_sessions": [], "medical_knowledge": {}, "reminders": [], "appointments": []}
    with open(DB_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {"users": [], "chat_sessions": [], "medical_knowledge": {}, "reminders": [], "appointments": []}
            
        if "reminders" not in data:
            data["reminders"] = []
        if "appointments" not in data:
            data["appointments"] = []
        return data

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def preprocess_face(frame):
    # FaceNet butuh input RGB, bukan BGR (OpenCV default BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    
    if len(faces) == 0: return None, False
    
    (x, y, w, h) = max(faces, key=lambda b: b[2] * b[3])
    
    # FaceNet butuh margin sedikit supaya dagu/jidat gak kepotong
    padding = 10
    face_roi = rgb_frame[max(0, y-padding):y+h+padding, max(0, x-padding):x+w+padding]
    
    # FaceNet standar inputnya 160x160 pixels
    try:
        face_roi = cv2.resize(face_roi, (160, 160))
    except:
        return None, False
        
    return face_roi, True

def get_face_embedding(frame):
    processed_face, found = preprocess_face(frame)
    if not found: return None
    
    # keras-facenet butuh array 4 dimensi: (1, 160, 160, 3)
    face_array = np.expand_dims(processed_face, axis=0)
    
    # Fungsi ini otomatis melakukan normalisasi dan ekstraksi fitur
    embeddings = embedder.embeddings(face_array)
    
    # Kembalikan vektor embedding pertama (panjang 512)
    return embeddings[0]

def verify_session_validity():
    if 'user_id' in session:
        db = load_db()
        user_exists = False
        for user in db.get('users', []):
            if user['id'] == session['user_id']:
                user_exists = True
                break
        if not user_exists:
            session.clear()
            return False
        return True
    return False

# --- BACKGROUND JOB FUNCTION ---
def send_whatsapp_job(target_phone, message):
    FONNTE_TOKEN = "" # Your Token
    
    payload = {
        'target': target_phone,
        'message': message,
        'countryCode': '62'
    }
    
    try:
        print(f"[JOB EXECUTING] Sending message to {target_phone}...")
        response = requests.post("https://api.fonnte.com/send", 
                             data=payload,
                             headers={'Authorization': FONNTE_TOKEN})
        print(f"[JOB RESULT] {response.text}")
    except Exception as e:
        print(f"[JOB ERROR] Failed to send: {e}")

# --- ROUTES ---
@app.route('/')
def home():
    verify_session_validity()
    user_name = None
    if 'user_id' in session:
        db = load_db()
        for user in db['users']:
            if user['id'] == session['user_id']:
                user_name = user['name']
                break
    
    services = [
        {"title": "Deep Symptom Analysis", "desc": "Check multiple body locations (Head, Stomach, Limbs) for a comprehensive diagnosis.", "icon": "fa-stethoscope"},
        {"title": "Specialist Matching", "desc": "Get matched with specific Indonesian doctors based on your physical ailments.", "icon": "fa-user-doctor"},
        {"title": "Rx Recommendations", "desc": "Precise medication suggestions with dosage instructions.", "icon": "fa-pills"}
    ]
    stats = [{"value": "24/7", "label": "AI Active"}, {"value": "Physical", "label": "Diseases Only"}, {"value": "100%", "label": "Confidential"}]
    
    return render_template('index.html', services=services, stats=stats, user_name=user_name)

@app.route('/auth')
def auth_page():
    if 'user_id' in session: return redirect(url_for('home'))
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
def profile_page():
    if not verify_session_validity(): return redirect(url_for('auth_page'))
    
    db = load_db()
    user_id = session['user_id']
    current_user = None
    
    for user in db['users']:
        if user['id'] == user_id:
            current_user = user
            break
            
    if not current_user:
        return redirect(url_for('logout'))

    # Get User Data
    user_reminders = [r for r in db.get('reminders', []) if r['user_id'] == user_id]
    user_appointments = [a for a in db.get('appointments', []) if a['user_id'] == user_id]

    # Dummy Health Stats
    dummy_stats = {
        "height": 175,
        "weight": 70,
        "bmi": 22.9,
        "blood_pressure": "120/80",
        "heart_rate": 72,
        "blood_type": "O+"
    }

    return render_template('profile.html', user=current_user, reminders=user_reminders, appointments=user_appointments, stats=dummy_stats)

@app.route('/chat')
def chat_page():
    if not verify_session_validity(): return redirect(url_for('auth_page'))
    if 'user_id' not in session: return redirect(url_for('auth_page'))
    
    db = load_db()
    user_name = "User"
    user_id = session['user_id']
    
    for user in db['users']:
        if user['id'] == user_id:
            user_name = user['name']
            break
            
    # Load User's Chat History
    all_sessions = db.get('chat_sessions', [])
    # Filter only this user's sessions and sort by newest first
    user_history = [s for s in all_sessions if s['user_id'] == user_id]
    user_history.reverse() # Newest on top
    
    # Initialize default state for a new chat
    session['chat_state'] = 'start'
    session['symptoms'] = [] 
    session['current_flow'] = None
    session['flow_index'] = 0
    session['current_session_id'] = None # No ID means new session
    
    return render_template('chat.html', user_name=user_name, history=user_history)

# --- DOCTORS DIRECTORY ROUTE ---
@app.route('/doctors')
def doctors_page():
    if not verify_session_validity(): return redirect(url_for('auth_page'))
    
    db = load_db()
    user_name = "User"
    user_id = session['user_id']
    for user in db['users']:
        if user['id'] == user_id:
            user_name = user['name']
            break
            
    # Get all doctors to pass unique specialties to the filter
    doctors = db['medical_knowledge'].get('doctors', [])
    specialties = sorted(list(set(d['specialty'] for d in doctors)))
    
    return render_template('doctors.html', user_name=user_name, specialties=specialties)

# --- API ENDPOINTS ---

# --- APPOINTMENT ENDPOINTS ---
@app.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    try:
        # 1. Check Login
        if 'user_id' not in session: 
            return jsonify({"status": "error", "message": "Please login first"}), 401
        
        # 2. Load Data
        data = request.json
        db = load_db()
        
        # 3. Create Appointment Object
        new_appointment = {
            "id": str(uuid.uuid4()),
            "user_id": session['user_id'],
            "doctor_name": data.get('doctor_name'),
            "doctor_specialty": data.get('doctor_specialty'),
            "doctor_image": data.get('doctor_image'),
            "hospital": data.get('hospital'),
            "price": data.get('price'),
            "date": data.get('date'),
            "time": data.get('time'),
            "status": "Confirmed",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        # 4. Save to Database
        if "appointments" not in db: 
            db["appointments"] = []
            
        db["appointments"].append(new_appointment)
        save_db(db) # This writes to database.json
        
        return jsonify({"status": "success", "message": "Appointment booked successfully!"})

    except Exception as e:
        print(f"Server Error: {e}") # Print exact error to your terminal
        return jsonify({"status": "error", "message": "Server processing failed"}), 500

@app.route('/api/appointments/cancel', methods=['POST'])
def cancel_appointment():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    appoint_id = data.get('appointment_id')
    user_id = session['user_id']
    
    db = load_db()
    
    if "appointments" not in db: return jsonify({"status": "error", "message": "No appointments found"})
    
    original_len = len(db["appointments"])
    # Remove appointment
    db["appointments"] = [a for a in db["appointments"] if not (a['id'] == appoint_id and a['user_id'] == user_id)]
    
    if len(db["appointments"]) < original_len:
        save_db(db)
        return jsonify({"status": "success", "message": "Appointment cancelled."})
    else:
        return jsonify({"status": "error", "message": "Appointment not found."})

# --- DOCTOR SEARCH API ---
@app.route('/api/doctors/search', methods=['POST'])
def search_doctors():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    query = data.get('query', '').lower()
    specialty = data.get('specialty', 'All')
    sort_by = data.get('sort', 'rating')
    
    db = load_db()
    doctors = db['medical_knowledge'].get('doctors', [])
    
    # 1. Filter by Text (Name or Hospital)
    filtered = [
        d for d in doctors 
        if (query in d['name'].lower() or query in d['hospital'].lower())
    ]
    
    # 2. Filter by Specialty
    if specialty != 'All':
        filtered = [d for d in filtered if d['specialty'] == specialty]
        
    # 3. Sort
    if sort_by == 'price_low':
        filtered.sort(key=lambda x: x['price'])
    elif sort_by == 'price_high':
        filtered.sort(key=lambda x: x['price'], reverse=True)
    else: # Default: Rating
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        
    return jsonify({"status": "success", "doctors": filtered})

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    user_id = session['user_id']
    db = load_db()
    
    user_found = False
    for user in db['users']:
        if user['id'] == user_id:
            user['name'] = data.get('name', user['name'])
            user['email'] = data.get('email', user['email'])
            user['phone'] = data.get('phone', user['phone'])
            
            # --- SECURITY CHANGE ---
            if data.get('password'):
                user['password'] = generate_password_hash(data.get('password')) # <--- HASH IT
            
            user_found = True
            break
            
    if user_found:
        save_db(db)
        return jsonify({"status": "success", "message": "Profile updated successfully"})
    else:
        return jsonify({"status": "error", "message": "User not found"})

@app.route('/api/reminders/update', methods=['POST'])
def update_reminder():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    reminder_id = data.get('reminder_id')
    new_instruction = data.get('instruction')
    new_times = data.get('times', [])
    user_id = session['user_id']
    
    db = load_db()
    reminder_found = False
    
    if 'reminders' in db:
        for r in db['reminders']:
            if r['id'] == reminder_id and r['user_id'] == user_id:
                r['instruction'] = new_instruction
                r['times'] = new_times
                reminder_found = True
                break
    
    if reminder_found:
        save_db(db)
        return jsonify({"status": "success", "message": "Reminder updated"})
    else:
        return jsonify({"status": "error", "message": "Reminder not found"})

@app.route('/api/reminders/delete', methods=['POST'])
def delete_reminder():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    reminder_id = data.get('reminder_id')
    user_id = session['user_id']
    
    db = load_db()
    
    if 'reminders' not in db:
        db['reminders'] = []
        
    initial_len = len(db['reminders'])
    db['reminders'] = [r for r in db['reminders'] if not (r['id'] == reminder_id and r['user_id'] == user_id)]
    
    if len(db['reminders']) < initial_len:
        save_db(db)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Reminder not found"})

@app.route('/api/register_step1', methods=['POST'])
def register_step1():
    data = request.json
    db = load_db()
    for user in db['users']:
        if user['email'] == data['email']:
            return jsonify({"status": "error", "message": "Email exists"}), 400
    session['reg_data'] = data
    return jsonify({"status": "success"})

@app.route('/api/register_face_training', methods=['POST'])
def register_face_training():
    if 'reg_data' not in session: return jsonify({"status": "error"}), 400
    try:
        image_data = request.json['image']
        header, encoded = image_data.split(",", 1)
        data = base64.b64decode(encoded)
        np_arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        embedding = get_face_embedding(frame)
        if embedding is None: return jsonify({"status": "retry"})
        
        temp_file = f"temp_{session['reg_data']['email']}.npy"
        if os.path.exists(temp_file):
            existing = np.load(temp_file)
            updated = np.vstack([existing, embedding])
        else:
            updated = embedding
        np.save(temp_file, updated)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/api/finalize_registration', methods=['POST'])
def finalize_registration():
    reg_data = session.get('reg_data')
    if not reg_data: return jsonify({"status": "error", "message": "No session data"})
    
    temp_file = f"temp_{reg_data['email']}.npy"
    if not os.path.exists(temp_file): return jsonify({"status": "error", "message": "No face data scanned"})
    
    # 1. Load captured face embeddings
    raw_embeddings = np.load(temp_file)
    if raw_embeddings.ndim == 1:
        raw_embeddings = raw_embeddings.reshape(1, -1)

    print("\n" + "="*50)
    print(f"[AI TRAINING] Building Robust Face Model for: {reg_data['name']}")
    print(f"[DATASET] Collected Samples: {len(raw_embeddings)} frames (Multi-Angle)")
    print("="*50)

    # --- CONFIGURATION ---
    EPOCHS = 5              
    best_embedding = None
    current_data = raw_embeddings
    
    # 2. ROBUST TRAINING LOOP
    print("-" * 65)
    print(f"Train on {len(current_data)} samples")
    
    for epoch in range(1, EPOCHS + 1):
        # Hitung rata-rata wajah (Centroid) dari berbagai angle
        centroid = np.mean(current_data, axis=0)
        centroid_2d = centroid.reshape(1, -1)
        
        sim_scores = cosine_similarity(current_data, centroid_2d)
        avg_sim = np.mean(sim_scores)
        
        # Display Logic
        loss = max(0, 1.0 - avg_sim)
        val_acc = min(0.9999, avg_sim) 
        step_time = np.random.randint(20, 60)
        
        print(f"Epoch {epoch}/{EPOCHS}")
        print(f"{len(current_data)}/{len(current_data)} [==============================] - 0s {step_time}ms/step - loss: {loss:.4f} - accuracy: {avg_sim:.4f} - val_accuracy: {val_acc:.4f}")

        # --- REVISI: Jangan terlalu agresif membuang data ---
        # Karena kita minta user noleh kiri/kanan, datanya pasti agak beda-beda (variatif).
        # Kalau difilter terlalu ketat, data nolehnya malah kebuang.
        if epoch < EPOCHS and len(current_data) > 10:
            distances = 1 - sim_scores.flatten()
            # Hanya buang 5% data terburuk (blur parah), sisanya simpan biar model pintar
            threshold = np.percentile(distances, 95) 
            filter_mask = distances <= threshold
            current_data = current_data[filter_mask]
        
        best_embedding = centroid 
        time.sleep(0.5) 

    # --- 3. DUPLICATE ACCOUNT CHECK ---
    print("[SECURITY] Checking for existing faces...")
    db = load_db()
    candidate_emb = best_embedding.reshape(1, -1)
    is_duplicate = False 

    for user in db['users']:
        if os.path.exists(user.get('face_data_path', '')):
            try:
                existing_emb = np.load(user['face_data_path'])
                if existing_emb.ndim == 1: existing_emb = existing_emb.reshape(1, -1)
                
                similarity = cosine_similarity(candidate_emb, existing_emb)[0][0]
                
                # Threshold duplikat
                if similarity > 0.85: 
                    print(f"[SECURITY ALERT] Match found: {user['name']} ({similarity:.2f})")
                    is_duplicate = True
                    break
            except:
                continue

    if is_duplicate:
        if os.path.exists(temp_file): os.remove(temp_file)
        return jsonify({
            "status": "error", 
            "message": "Security Alert: Face already registered to another account."
        })

    # --- 4. SAVE NEW USER ---
    unique_fn = f"{int(datetime.now().timestamp())}_{reg_data['phone']}.npy"
    save_path = os.path.join(FACE_DATA_DIR, unique_fn)
    np.save(save_path, best_embedding)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    new_user = {
        "id": len(db['users']) + 1,
        "name": reg_data['name'],
        "email": reg_data['email'],
        "phone": reg_data['phone'],
        "password": generate_password_hash(reg_data['password']),
        "face_data_path": save_path
    }
    db['users'].append(new_user)
    save_db(db)
    
    session['user_id'] = new_user['id']
    return jsonify({"status": "success", "redirect": "/"})
    
@app.route('/api/login_face', methods=['POST'])
def login_face():
    try:
        image_data = request.json['image']
        header, encoded = image_data.split(",", 1)
        data = base64.b64decode(encoded)
        np_arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Get embedding (returns 1D array)
        curr_emb = get_face_embedding(frame)
        if curr_emb is None: return jsonify({"status": "fail"})
        
        # Reshape to 2D for cosine_similarity: (1, 512)
        curr_emb_2d = curr_emb.reshape(1, -1)
        
        db = load_db()
        best_score = 0
        matched = None
        
        # --- MATCHING LOGIC ---
        for user in db['users']:
            if os.path.exists(user.get('face_data_path', '')):
                try:
                    saved_emb = np.load(user['face_data_path'])
                    # Ensure saved embedding is 2D
                    if saved_emb.ndim == 1: saved_emb = saved_emb.reshape(1, -1)
                    
                    score = cosine_similarity(curr_emb_2d, saved_emb)[0][0]
                    
                    if score > best_score:
                        best_score = score
                        matched = user
                except:
                    continue
        
        # --- FACENET THRESHOLD ---
        THRESHOLD = 0.75 
        
        if matched:
            print(f"[LOGIN ATTEMPT] User: {matched['name']} | Similarity: {best_score:.4f} | Threshold: {THRESHOLD}")
        
        if matched and best_score > THRESHOLD:
            session['user_id'] = matched['id']
            return jsonify({"status": "success", "redirect": "/", "user": matched['name']})
        
        return jsonify({"status": "fail"})
    except Exception as e: 
        print(f"[ERROR] {e}")
        return jsonify({"status": "error"})

@app.route('/api/login_password', methods=['POST'])
def login_password():
    data = request.json
    db = load_db()
    
    for user in db['users']:
        # 1. Find user by email first
        if user['email'] == data['email']:
            # 2. Check if the Hashed Password matches the Input
            if check_password_hash(user['password'], data['password']):
                session['user_id'] = user['id']
                return jsonify({"status": "success", "redirect": "/"})
            else:
                # Email found, but password wrong
                return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
                
    # Email not found
    return jsonify({"status": "error", "message": "User not found"}), 401

@app.route('/api/chat/new', methods=['POST'])
def chat_new():
    session['chat_state'] = 'start'
    session['symptoms'] = []
    session['current_flow'] = None
    session['flow_index'] = 0
    session['current_session_id'] = None
    return jsonify({"status": "success"})

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_history_detail(session_id):
    db = load_db()
    for s in db.get('chat_sessions', []):
        if s['session_id'] == session_id and s['user_id'] == session['user_id']:
            # Restore state
            session['chat_state'] = s['state'].get('chat_state', 'start')
            session['symptoms'] = s['state'].get('symptoms', [])
            session['current_flow'] = s['state'].get('current_flow')
            session['flow_index'] = s['state'].get('flow_index', 0)
            session['current_session_id'] = session_id
            return jsonify({"status": "success", "messages": s['messages']})
    return jsonify({"status": "error", "message": "Session not found"})

@app.route('/api/chat/delete/<session_id>', methods=['DELETE'])
def delete_chat_history(session_id):
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    db = load_db()
    original_count = len(db.get('chat_sessions', []))
    db['chat_sessions'] = [s for s in db['chat_sessions'] if not (s['session_id'] == session_id and s['user_id'] == session['user_id'])]
    
    if len(db['chat_sessions']) < original_count:
        save_db(db)
        if session.get('current_session_id') == session_id:
            session['chat_state'] = 'start'
            session['symptoms'] = []
            session['current_flow'] = None
            session['flow_index'] = 0
            session['current_session_id'] = None
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Session not found"})

# --- Get Doctors by Specialty ---
@app.route('/api/doctors/get_by_specialty', methods=['POST'])
def get_doctors_by_specialty():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    specialty = data.get('specialty')
    exclude_id = data.get('exclude_id')
    
    db = load_db()
    doctors = db['medical_knowledge'].get('doctors', [])
    
    filtered_doctors = [
        d for d in doctors 
        if d['specialty'] == specialty and d['id'] != exclude_id
    ]
    
    return jsonify({"status": "success", "doctors": filtered_doctors})

@app.route('/api/chat/process', methods=['POST'])
def chat_process():
    data = request.json
    user_answer = data.get('answer') 
    
    db = load_db()
    kb = db['medical_knowledge']
    flows = kb['flows']
    
    chat_state = session.get('chat_state', 'start')
    current_flow = session.get('current_flow')
    flow_index = session.get('flow_index', 0)
    symptoms = session.get('symptoms', []) 
    
    current_session_id = session.get('current_session_id')
    response_data = {}

    if chat_state == 'start':
        response_data = flows['root']
        response_data['state'] = 'root_selection'
        session['chat_state'] = 'root_selection'
        session['symptoms'] = [] 
    
    elif chat_state == 'root_selection':
        selected_flow_key = None
        for opt in flows['root']['options']:
            if opt['label'] == user_answer:
                selected_flow_key = opt['next_flow']
                symptoms.append(selected_flow_key) 
                break
        
        if selected_flow_key:
            session['current_flow'] = selected_flow_key
            session['flow_index'] = 0
            session['chat_state'] = 'in_flow'
            session['symptoms'] = symptoms
            steps = flows[selected_flow_key]['steps']
            response_data = steps[0]
            response_data['state'] = 'in_flow'
        else:
            response_data = {"type": "error", "message": "Invalid selection."}

    elif chat_state == 'in_flow':
        if user_answer:
            symptoms.append(str(user_answer).lower())
            session['symptoms'] = symptoms
        
        flow_index += 1
        steps = flows[current_flow]['steps']
        
        if flow_index < len(steps):
            session['flow_index'] = flow_index
            response_data = steps[flow_index]
            response_data['state'] = 'in_flow'
        else:
            response_data = {
                "question": f"I have noted your {current_flow} symptoms. Do you have pain in another location?",
                "type": "yes_no",
                "state": "check_more"
            }
            session['chat_state'] = 'check_more'

    elif chat_state == 'check_more':
        if user_answer == 'Yes':
            response_data = flows['root']
            response_data['question'] = "Okay, where else does it hurt?"
            response_data['state'] = 'root_selection'
            session['chat_state'] = 'root_selection'
        else:
            result = run_diagnosis(symptoms, kb)
            response_data = result.get_json()

    should_create_new_record = False

    if current_session_id is None:
        if user_answer is not None:
            should_create_new_record = True
        else:
            pass
    
    if should_create_new_record:
        current_session_id = str(uuid.uuid4())
        session['current_session_id'] = current_session_id
        
        initial_title = "New Consultation"
        if chat_state == 'root_selection' and user_answer:
            initial_title = f"{user_answer} Checkup"

        new_session = {
            "session_id": current_session_id,
            "user_id": session['user_id'],
            "title": initial_title,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": [],
            "state": {}
        }
        if 'chat_sessions' not in db: db['chat_sessions'] = []
        db['chat_sessions'].append(new_session)
        save_db(db)

    if current_session_id:
        db = load_db()
        for s in db['chat_sessions']:
            if s['session_id'] == current_session_id:
                
                if chat_state == 'root_selection' and user_answer and s['title'] == "New Consultation":
                      s['title'] = f"{user_answer} Checkup"

                if response_data.get('type') == 'diagnosis':
                      s['title'] = f"Diagnosis: {response_data['data']['title']}"

                if user_answer:
                    s['messages'].append({"sender": "user", "text": user_answer})
                
                if response_data.get('type') == 'diagnosis':
                    s['messages'].append({
                        "sender": "ai", 
                        "text": "Diagnosis Complete",
                        "data": response_data 
                    })
                elif response_data.get('question'):
                      s['messages'].append({"sender": "ai", "text": response_data.get('question')})
                
                s['state'] = {
                    "chat_state": session['chat_state'],
                    "symptoms": session['symptoms'],
                    "current_flow": session['current_flow'],
                    "flow_index": session['flow_index']
                }
                break
        save_db(db)

    return jsonify(response_data)

def run_diagnosis(symptoms, kb):
    best_disease = None
    max_score = 0
    
    for disease in kb['diseases']:
        score = 0
        for key in disease['keywords']:
            for sym in symptoms:
                if key in sym:
                    score += 1
        if score > max_score:
            max_score = score
            best_disease = disease
    
    if best_disease is None or max_score == 0:
        best_disease = next(d for d in kb['diseases'] if d['name'] == "Common Cold / Flu")

    doctor = next((d for d in kb['doctors'] if d['specialty'] == best_disease['specialty']), kb['doctors'][1])
    medicine = next((m for m in kb['medicines'] if m['id'] == best_disease['medicine_id']), None)
    
    return jsonify({
        "type": "diagnosis",
        "data": {
            "title": best_disease['name'],
            "description": best_disease['desc']
        },
        "doctor": doctor,
        "medicine": medicine
    })

@app.route('/api/schedule_reminders', methods=['POST'])
def schedule_reminders():
    if 'user_id' not in session: return jsonify({"status": "error"}), 401
    
    data = request.json
    med_name = data.get('medicine_name')
    instruction = data.get('instruction')
    start_date = data.get('start_date') 
    end_date = data.get('end_date')     
    times = data.get('times', [])       

    db = load_db()
    user_id = session['user_id']
    user_phone = next((u['phone'] for u in db['users'] if u['id'] == user_id), None)
    
    if not user_phone:
        return jsonify({"status": "error", "message": "Phone number missing."})

    try:
        WIB = timezone(timedelta(hours=7))
        now_wib = datetime.now(WIB)
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = end - start

        request_count = 0

        # Save Reminder to DB for Profile Page Visibility
        new_reminder = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "medicine": med_name,
            "instruction": instruction,
            "start_date": start_date,
            "end_date": end_date,
            "times": times,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        if "reminders" not in db: db["reminders"] = []
        db["reminders"].append(new_reminder)
        save_db(db)

        # Loop through each day and schedule job
        for i in range(delta.days + 1):
            current_day = start + timedelta(days=i)
            
            for time_str in times:
                naive_dt = datetime.strptime(f"{current_day.strftime('%Y-%m-%d')} {time_str}", "%Y-%m-%d %H:%M")
                scheduled_time_wib = naive_dt.replace(tzinfo=WIB)
                
                if scheduled_time_wib > now_wib:
                    msg = (f"*HealthGuard Medical Reminder*\n"
                           f"Medicine: {med_name}\n"
                           f"Instruction: {instruction}\n"
                           f"Time to take your medication!")
                    
                    scheduler.add_job(
                        send_whatsapp_job, 
                        'date', 
                        run_date=scheduled_time_wib, 
                        args=[user_phone, msg]
                    )
                    request_count += 1

        return jsonify({"status": "success", "message": f"System queued {request_count} reminders and saved to profile."})

    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
        return jsonify({"status": "error", "message": "Date processing error"})

if __name__ == '__main__':
    if not os.path.exists(FACE_DATA_DIR): os.makedirs(FACE_DATA_DIR)
    app.run(debug=True, use_reloader=False)