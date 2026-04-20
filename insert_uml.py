import shutil
from docx import Document
from docx.shared import Pt

def add_plantuml_after_text(doc, search_text, uml_code, title):
    for i, p in enumerate(doc.paragraphs):
        if search_text in p.text:
            if i + 1 < len(doc.paragraphs):
                target_p = doc.paragraphs[i+1]
                
                title_p = target_p.insert_paragraph_before(title)
                for run in title_p.runs:
                    run.bold = True
                    run.italic = True
                    
                code_p = target_p.insert_paragraph_before(uml_code)
                for run in code_p.runs:
                    run.font.name = 'Courier New'
                    run.font.size = Pt(10)
                # Fallback to Normal if No Spacing isn't available
                try:
                    code_p.style = doc.styles['No Spacing']
                except:
                    code_p.style = doc.styles['Normal']
            return

def main():
    try:
        shutil.copy("Project_Report_Super_Expanded.docx", "Project_Report_Final.docx")
    except Exception as e:
        print("Copy failed:", e)
        return

    doc = Document("Project_Report_Final.docx")

    uc_plantuml = """
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Administrator" as Admin
actor "System Process" as Sys
actor "Simulated Attacker" as Attacker

rectangle "DDoS Mitigation Pipeline" {
  usecase "Train Hybrid ML Pipeline" as UC1
  usecase "Deploy Edge Scrubbing Shield" as UC2
  usecase "Simulate Volume Anomalies" as UC3
  usecase "Execute Live Stream (SSE)" as UC4
  usecase "Predict Packet Status" as UC5
  usecase "Dispatch Notification (WhatsApp)" as UC6
}

Admin --> UC1
Admin --> UC2
Attacker --> UC3
Sys --> UC4
Sys --> UC5
Sys --> UC6

UC2 ..> UC4 : <<includes>>
UC4 ..> UC5 : <<includes>>
UC5 ..> UC6 : <<extends>> (if drops > 15)
@enduml
"""
    # Insert in Analysis -> Use Cases (After the words "explicitly mapped actor parameters")
    add_plantuml_after_text(doc, "explicitly mapped actor parameters", uc_plantuml, "Figure 1.1: System Use Case Diagram (PlantUML)")

    comp_plantuml = """
@startuml
node "Client Browser" {
  component "DOM (script.js)" as UI
}

node "FastAPI Backend" {
  component "Server (server.py)" as Server
  component "SSE Generator" as Gen
}

node "ML Inference Engine" {
  component "RandomForest" as RFC
  component "StandardScaler" as Scaler
}

database "Local Storage" {
  artifact "Parquet Datasets" as Parquet
}

UI <--> Server : HTTP POST (/api/train)
UI <-- Gen : Server-Sent Events

Server --> RFC : fit()
Server --> Scaler : fit_transform()
Gen --> Scaler : transform()
Gen --> RFC : predict()
RFC <-- Parquet : Load Dataset
@enduml
"""
    # Insert in Design -> Structural Layers (After "Document Object Method variables locally.")
    add_plantuml_after_text(doc, "Document Object Method variables locally", comp_plantuml, "Figure 1.2: Component & Architecture Diagram (PlantUML)")

    seq_plantuml = """
@startuml
actor Admin
participant "script.js" as UI
participant "FastAPI" as API
participant "ML Logic" as ML
participant "PyWhatKit" as Alert

Admin -> UI: Click "Deploy Shield"
UI -> API: GET /api/simulate
activate API

API -> API: Start Async Generator Loop
loop Continuous Simulated Flow (150 packets/tick)
    API -> ML: generate_hybrid_stream()
    ML --> API: botnet + player packets
    
    API -> ML: transform(metrics)
    ML --> API: scaled parameters
    
    API -> ML: predict(scaled)
    ML --> API: 0 (Pass) or 1 (Drop)
    
    API -> UI: yield EventSource JSON
    UI -> UI: Append DOM Element Live
    
    alt If drops >= 15
        API -> Alert: trigger WhatsApp notification
        Alert --> API: Success
    end
end
deactivate API
@enduml
"""
    # Insert in Design -> Behavioural Models (After "accurately providing detailed interface displays securely successfully visually completely representing exact dynamic structural performance indicators perfectly accurately.")
    add_plantuml_after_text(doc, "representing exact dynamic structural performance indicators perfectly accurately", seq_plantuml, "Figure 1.3: Asynchronous Sequence Diagram (PlantUML)")

    try:
        doc.save("Project_Report_Final.docx")
        print("Successfully injected UML diagrams into Project_Report_Final.docx")
    except Exception as e:
        print("Save failed:", e)

if __name__ == "__main__":
    main()
