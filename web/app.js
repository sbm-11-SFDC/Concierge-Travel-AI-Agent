// @ts-nocheck
 (() => {
   const AGENT_URL = "http://localhost:8005/agent/task";
   const TIMEOUT_MS = 60000;

   const $form = document.getElementById("tripForm");
   const $input = document.getElementById("query");
   const $status = document.getElementById("status");
   const $result = document.getElementById("result");

   const params = new URLSearchParams(window.location.search);
   if (params.has("trip") && !$input.value) {
     $input.value = params.get("trip");
   }

   function showStatus(text) {
     $status.textContent = text || "";
   }

   function showResult(obj) {
     if (!obj) {
       $result.textContent = "";
       return;
     }
     try {
       if (typeof obj === "string") {
         $result.textContent = obj;
       } else {
         $result.textContent = JSON.stringify(obj, null, 2);
       }
     } catch (e) {
       $result.textContent = String(obj);
     }
   }

   async function postToAgent(query) {
     const controller = new AbortController();
     const id = setTimeout(() => controller.abort(), TIMEOUT_MS);

     const payload = {
       task_id: `T-web-${Date.now()}`,
       payload: { query: query }
     };

     try {
       showStatus("Thinking... contacting agent");
       showResult("");
       const resp = await fetch(AGENT_URL, {
         method: "POST",
         headers: { "Content-Type": "application/json" },
         body: JSON.stringify(payload),
         signal: controller.signal,
         credentials: "omit"
       });

       clearTimeout(id);

       const contentType = resp.headers.get("content-type") || "";
       if (contentType.includes("application/json")) {
         const data = await resp.json();
         showResult(data.plan ?? JSON.stringify(data, null, 2));
         showStatus(`Agent responded (status ${resp.status})`);
       } else {
         const text = await resp.text();
         showResult(text);
         showStatus(`Agent responded (status ${resp.status})`);
       }

     } catch (err) {
       clearTimeout(id);
       if (err.name === "AbortError") {
         showStatus("Request timed out after 30s.");
         showResult("The agent took too long to respond.");
       } else {
         showStatus("Request failed.");
         showResult(err.message || String(err));
       }
     }
   }

   if ($form) {
     $form.addEventListener("submit", (ev) => {
       ev.preventDefault();
       const q = $input.value.trim();
       if (!q) {
         showStatus("Please enter a trip request.");
         return;
       }
       postToAgent(q);
     });
   }

   if (params.has("auto") && $input.value) {
     postToAgent($input.value);
   }

 })();