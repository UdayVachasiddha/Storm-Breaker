document.addEventListener("DOMContentLoaded", () => {
    // Buttons & UI elements
    const btnTrain = document.getElementById("btn-train");
    const btnSimulate = document.getElementById("btn-simulate");
    const loader = document.getElementById(" प्रशिक्षण-loader") || document.getElementById("training-loader");
    const statusDot = document.getElementById("model-status-dot");
    const statusText = document.getElementById("model-status-text");
    const livePulse = document.getElementById("live-pulse");
    
    // Metrics
    const valAcc = document.getElementById("val-accuracy");
    const valFpr = document.getElementById("val-fpr");
    const cmTn = document.getElementById("cm-tn");
    const cmFp = document.getElementById("cm-fp");
    const cmFn = document.getElementById("cm-fn");
    const cmTp = document.getElementById("cm-tp");
    
    // Table
    const valPassed = document.getElementById("stat-passed");
    const valDropped = document.getElementById("stat-dropped");
    const streamBody = document.getElementById("traffic-stream-body");
    const cmLiveTag = document.getElementById("cm-live-tag");
    
    let isTraining = false;
    let isSimulating = false;
    let eventSource = null;
    let passedCount = 0;
    let droppedCount = 0;

    // Live Matrix Counters
    let liveTn = 0, liveFp = 0, liveFn = 0, liveTp = 0;
    
    /**
     * Train API Integration
     */
    btnTrain.addEventListener("click", async () => {
        btnTrain.blur(); // Remove focus to prevent pywhatkit keyboard interference
        if (isTraining || isSimulating) return;
        
        // Update UI
        isTraining = true;
        btnTrain.disabled = true;
        btnSimulate.disabled = true;
        loader.classList.remove("hidden");
        
        statusDot.className = "status-dot offline";
        statusText.innerText = "Training Pipeline...";
        statusText.style.color = "var(--primary)";
        
        try {
            const res = await fetch("/api/train", { method: "POST" });
            const data = await res.json();
            
            if (data.status === "success") {
                // Update Metrics visually
                animateValueUI(valAcc, data.accuracy * 100, "%");
                animateValueUI(valFpr, data.fpr * 100, "%", 4);
                
                cmTn.innerText = data.confusion_matrix.tn.toLocaleString();
                cmFp.innerText = data.confusion_matrix.fp.toLocaleString();
                cmFn.innerText = data.confusion_matrix.fn.toLocaleString();
                cmTp.innerText = data.confusion_matrix.tp.toLocaleString();
                
                // Unlock Simulation
                btnSimulate.disabled = false;
                
                // Status
                statusDot.className = "status-dot online";
                statusText.innerText = "Engine Online & Ready";
                statusText.style.color = "var(--success)";
            }
        } catch (error) {
            console.error(error);
            statusText.innerText = "Training Failed";
            statusText.style.color = "var(--danger)";
        } finally {
            isTraining = false;
            btnTrain.disabled = false;
            loader.classList.add("hidden");
        }
    });
    
    /**
     * Live Simulation Stream Integration (SSE)
     */
    btnSimulate.addEventListener("click", () => {
        btnSimulate.blur(); // Remove focus to prevent pywhatkit keyboard interference
        if (isSimulating) {
            // Stop Simulation
            if(eventSource) eventSource.close();
            stopSimulationUI();
            return;
        }
        
        // Start Simulation
        isSimulating = true;
        btnTrain.disabled = true;
        btnSimulate.innerText = "Halt Scrubbing Shield";
        btnSimulate.classList.remove("secondary-btn");
        btnSimulate.classList.add("primary-btn");
        livePulse.classList.remove("hidden");
        
        // Reset table
        streamBody.innerHTML = "";
        passedCount = 0;
        droppedCount = 0;
        liveTn = 0; liveFp = 0; liveFn = 0; liveTp = 0;
        
        valPassed.innerText = "0";
        valDropped.innerText = "0";
        cmTn.innerText = "0";
        cmFp.innerText = "0";
        cmFn.innerText = "0";
        cmTp.innerText = "0";
        valAcc.innerText = "0.00%";
        valFpr.innerText = "0.0000%";
        
        cmLiveTag.classList.remove("hidden");
        
        // Check Node Filter & WhatsApp Values
        const nodeFilter = document.getElementById("node-filter").value;
        const whatsappToggle = document.getElementById("whatsapp-toggle").checked;
        
        // Open SSE connection with the filter parameters
        eventSource = new EventSource(`/api/simulate?target_node=${nodeFilter}&whatsapp=${whatsappToggle}`);
        
        eventSource.onmessage = function(event) {
            const rawData = JSON.parse(event.data);
            
            if (rawData.status === "done" || rawData.error) {
                if (rawData.error) console.error(rawData.error);
                eventSource.close();
                stopSimulationUI();
                return;
            }
            
            appendRowWithAnimation(rawData);
        };
        
        eventSource.onerror = function(err) {
            console.error("SSE Error:", err);
            eventSource.close();
            stopSimulationUI();
        };
    });
    
    function stopSimulationUI() {
        isSimulating = false;
        btnTrain.disabled = false;
        btnSimulate.innerText = "Deploy eBPF Scrubbing Shield";
        btnSimulate.classList.remove("primary-btn");
        btnSimulate.classList.add("secondary-btn");
        livePulse.classList.add("hidden");
        // We keep the Live tag visible so people know the metrics are from the LAST run.
    }
    
    /**
     * Appends a row visually mirroring true edge-logging speeds
     */
    function appendRowWithAnimation(pkt) {
        const tableContainer = document.querySelector(".table-container");
        const tr = document.createElement("tr");
        tr.className = 'new-row';
        
        let actualClass = pkt.actual_label === 1 ? 'actual-ddos' : 'actual-norm';
        let actualText = pkt.actual_label === 1 ? 'DDoS' : 'Norm';
        
        let actionClass = pkt.predicted === 1 ? 'action-dropped' : 'action-passed';
        let actionText = pkt.predicted === 1 ? 'DROPPED' : 'PASSED';
        
        // Custom CSS class for Anycast Nodes
        const nodeLabel = pkt.node;
        let nodeClass = 'node-bom';
        if (nodeLabel.includes('FRA')) nodeClass = 'node-fra';
        if (nodeLabel.includes('TYO')) nodeClass = 'node-tyo';
        if (nodeLabel.includes('SGP')) nodeClass = 'node-sgp';
        
        tr.innerHTML = `
            <td>#${String(pkt.id).padStart(3, '0')}</td>
            <td><span class="node-badge ${nodeClass}">${nodeLabel}</span></td>
            <td>${pkt.packet_size.toFixed(1)}</td>
            <td>${pkt.inter_arrival_time.toFixed(1)}</td>
            <td>${pkt.variance.toFixed(2)}</td>
            <td class="${actualClass}">${actualText}</td>
            <td><span class="badge ${actionClass}">${actionText}</span></td>
        `;
        
        // Append at the bottom — all traffic accumulates, no rows are dropped
        streamBody.appendChild(tr);
        
        // Auto-scroll the container so the latest packet is always visible
        tableContainer.scrollTop = tableContainer.scrollHeight;
        
        // Update stats
        if (pkt.predicted === 1) {
            droppedCount++;
            valDropped.innerText = droppedCount;
        } else {
            passedCount++;
            valPassed.innerText = passedCount;
        }

        // --- LIVE CONFUSION MATRIX LOGIC ---
        // actual_label: 0=Norm, 1=DDoS | predicted: 0=Norm, 1=DDoS
        if (pkt.actual_label === 0 && pkt.predicted === 0) {
            liveTn++;
            cmTn.innerText = liveTn.toLocaleString();
        } else if (pkt.actual_label === 0 && pkt.predicted === 1) {
            liveFp++;
            cmFp.innerText = liveFp.toLocaleString();
        } else if (pkt.actual_label === 1 && pkt.predicted === 0) {
            liveFn++;
            cmFn.innerText = liveFn.toLocaleString();
        } else if (pkt.actual_label === 1 && pkt.predicted === 1) {
            liveTp++;
            cmTp.innerText = liveTp.toLocaleString();
        }

        // --- LIVE CARD UPDATES ---
        const total = liveTn + liveFp + liveFn + liveTp;
        if (total > 0) {
            const acc = ((liveTn + liveTp) / total) * 100;
            const fpr = (liveFp / (liveFp + liveTn)) * 100 || 0;
            
            valAcc.innerText = acc.toFixed(2) + "%";
            valFpr.innerText = fpr.toFixed(4) + "%";
        }
    }
    
    /**
     * Counter Animation for Metrics
     */
    function animateValueUI(obj, targetValue, suffix, decimals=2, duration=1000) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            const currentVal = progress * targetValue;
            obj.innerHTML = currentVal.toFixed(decimals) + suffix;
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = targetValue.toFixed(decimals) + suffix;
            }
        };
        window.requestAnimationFrame(step);
    }
});
