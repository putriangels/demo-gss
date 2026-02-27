import streamlit as st

# ==============================
# TOOL: BMI Calculator
# ==============================

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


# ==============================
# AI AGENT DOCTOR
# ==============================

class AdvancedAIAgentDoctor:
    def __init__(self):
        self.knowledge_base = {
            "diabetes": ["gula darah tinggi", "sering haus", "sering kencing"],
            "flu": ["demam", "batuk", "pilek"],
            "obesitas": ["bmi tinggi", "kelelahan", "nyeri sendi"]
        }
        self.experience = []
        self.logs = []

    # Perception
    def perceive(self, patient_data):
        self.logs.append("🔎 Agent menerima data pasien.")
        return patient_data

    # Reasoning
    def reason(self, patient_data):
        patient_symptoms = patient_data.get("symptoms", [])
        possible_diseases = []

        for disease, symptoms in self.knowledge_base.items():
            if any(symptom in patient_symptoms for symptom in symptoms):
                possible_diseases.append(disease)

        if possible_diseases:
            self.logs.append(f"🧠 Kemungkinan penyakit: {', '.join(possible_diseases)}")
        else:
            self.logs.append("🧠 Tidak terdeteksi penyakit spesifik")

        return possible_diseases

    # Planning
    def plan(self, possible_diseases):
        plan_steps = []

        for disease in possible_diseases:
            if disease == "diabetes":
                plan_steps.append("Tes HbA1c")
            elif disease == "flu":
                plan_steps.append("Cek suhu & observasi")
            elif disease == "obesitas":
                plan_steps.append("Hitung BMI")

        if not plan_steps:
            plan_steps.append("Pemeriksaan umum")

        self.logs.append(f"📋 Rencana tindakan: {', '.join(plan_steps)}")
        return plan_steps

    # Action + Tool Calling
    def act(self, plan_steps, patient_data):
        results = []

        for step in plan_steps:
            if step == "Hitung BMI":
                weight = patient_data.get("weight", 70)
                height = patient_data.get("height", 170)

                bmi = calculate_bmi(weight, height)

                if bmi >= 25:
                    diagnosis = f"BMI {bmi} → Pasien obesitas"
                else:
                    diagnosis = f"BMI {bmi} → Berat badan normal"

                results.append(diagnosis)
            else:
                results.append(step)

        self.logs.append(f"⚡ Eksekusi tindakan: {', '.join(results)}")
        return results

    # Learning
    def learn(self, feedback):
        self.experience.append(feedback)
        self.logs.append(f"📚 Belajar dari feedback: {feedback}")

    # Adaptation
    def adapt(self):
        if "salah diagnosa" in self.experience:
            if "kelelahan" not in self.knowledge_base["diabetes"]:
                self.knowledge_base["diabetes"].append("kelelahan")
                self.logs.append("🔁 Agent menambahkan gejala 'kelelahan' ke diabetes")
        else:
            self.logs.append("✅ Tidak perlu adaptasi")

    # Full Run
    def run_case(self, patient_data, feedback=None):
        self.logs = []

        self.perceive(patient_data)
        diseases = self.reason(patient_data)
        plan = self.plan(diseases)
        result = self.act(plan, patient_data)

        if feedback:
            self.learn(feedback)
            self.adapt()

        return result, self.logs


# ==============================
# STREAMLIT UI
# ==============================

st.set_page_config(page_title="AI Agent Doctor", layout="centered")

st.title("🩺 Agentic AI Doctor Demo")
st.write("Simulasi AI Agent dengan Tool Calling + Learning + Adaptation")

agent = AdvancedAIAgentDoctor()

# Input Form
symptoms_input = st.text_input(
    "Masukkan gejala (pisahkan dengan koma)",
    placeholder="demam, batuk"
)

weight = st.number_input("Berat badan (kg)", min_value=30, max_value=200, value=70)
height = st.number_input("Tinggi badan (cm)", min_value=120, max_value=220, value=170)

feedback = st.selectbox(
    "Feedback dokter (opsional)",
    ["Tidak ada", "diagnosa benar", "salah diagnosa"]
)

if st.button("Jalankan Agent"):
    symptoms = [s.strip().lower() for s in symptoms_input.split(",") if s]

    patient_data = {
        "symptoms": symptoms,
        "weight": weight,
        "height": height
    }

    fb = None if feedback == "Tidak ada" else feedback

    result, logs = agent.run_case(patient_data, fb)

    st.subheader("📊 Hasil Diagnosis / Tindakan")
    for r in result:
        st.success(r)

    st.subheader("🧠 Proses Berpikir Agent")
    for log in logs:
        st.write(log)