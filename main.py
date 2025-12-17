<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Faesh</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,sans-serif;background:#0e0e11;color:#fff;display:flex;flex-direction:column;height:100vh}
    header{padding:12px 16px;background:#12121a;border-bottom:1px solid #1f1f2e;font-weight:700}
    #chat{flex:1;padding:16px;overflow-y:auto;display:flex;flex-direction:column;gap:10px}
    .message{max-width:75%;padding:10px 14px;border-radius:14px;line-height:1.4;font-size:14px;word-wrap:break-word;white-space:pre-wrap}
    .user{align-self:flex-end;background:#3b82f6;color:#fff}
    .bot{align-self:flex-start;background:#1f2937;color:#e5e7eb}
    footer{padding:10px;background:#12121a;border-top:1px solid #1f1f2e;display:flex;flex-direction:column;gap:8px}
    .controls{display:flex;gap:6px;align-items:center}
    textarea{flex:1;resize:none;padding:10px;border-radius:8px;border:none;outline:none;background:#1f2937;color:#fff;font-size:14px;height:44px}
    button{padding:10px 14px;border-radius:8px;border:none;cursor:pointer;background:#3b82f6;color:#fff;font-weight:700}
    button.secondary{background:#374151}
    input[type="range"]{width:100%}
    .label{font-size:12px;color:#9ca3af}
  </style>
</head>

<body>
  <header>Faesh</header>
  <div id="chat"></div>

  <footer>
    <div class="label">Roast level</div>
    <input id="roastLevel" type="range" min="0" max="3" step="1" value="1" />

    <div class="controls">
      <input id="imageInput" type="file" accept="image/*" hidden />
      <input id="fileInput" type="file" hidden />

      <button class="secondary" id="imageBtn">🖼️</button>
      <button class="secondary" id="fileBtn">📎</button>

      <textarea id="input" placeholder="Say something to Faesh..."></textarea>
      <button id="sendBtn">Send</button>
    </div>
  </footer>

  <script>
    console.log("Faesh frontend loaded cleanly");

    const API_BASE = "https://faesh.onrender.com";

    const chatEl = document.getElementById("chat");
    const inputEl = document.getElementById("input");
    const roastEl = document.getElementById("roastLevel");

    const imageInput = document.getElementById("imageInput");
    const fileInput  = document.getElementById("fileInput");
    const imageBtn   = document.getElementById("imageBtn");
    const fileBtn    = document.getElementById("fileBtn");
    const sendBtn    = document.getElementById("sendBtn");

    let messages = [];

    function addMessage(role, text) {
      const div = document.createElement("div");
      div.className = `message ${role}`;
      div.textContent = text;
      chatEl.appendChild(div);
      chatEl.scrollTop = chatEl.scrollHeight;
    }

    async function sendMessage() {
      const text = inputEl.value.trim();
      if (!text) return;

      inputEl.value = "";
      addMessage("user", text);
      messages.push({ role: "user", content: text });

      try {
        const res = await fetch(`${API_BASE}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            messages,
            roast_level: parseInt(roastEl.value, 10),
          }),
        });

        const data = await res.json();

        if (data.reply) {
          addMessage("bot", data.reply);
          messages.push({ role: "assistant", content: data.reply });
        } else {
          addMessage("bot", data.error ? `Error: ${data.error}` : "Faesh didn’t respond.");
        }
      } catch (err) {
        console.error(err);
        addMessage("bot", "Error reaching Faesh.");
      }
    }

    async function sendVision(file) {
      addMessage("user", `🖼️ Uploaded: ${file.name}`);

      const fd = new FormData();
      fd.append("image", file);
      fd.append("prompt", "Analyze this outfit/concept and give honest fashion feedback.");
      fd.append("roast_level", String(parseInt(roastEl.value, 10)));

      try {
        const res = await fetch(`${API_BASE}/vision`, { method: "POST", body: fd });
        const data = await res.json();
        addMessage("bot", data.reply || "Vision upload worked, but no reply returned.");
      } catch (err) {
        console.error(err);
        addMessage("bot", "Vision upload failed.");
      }
    }

    async function sendFile(file) {
      addMessage("user", `📎 Uploaded: ${file.name}`);

      const fd = new FormData();
      fd.append("file", file);
      fd.append("purpose", "Summarize this file and suggest improvements.");

      try {
        const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: fd });
        const data = await res.json();
        addMessage("bot", data.reply || "File upload worked, but no reply returned.");
      } catch (err) {
        console.error(err);
        addMessage("bot", "File upload failed.");
      }
    }

    // UI bindings
    sendBtn.addEventListener("click", sendMessage);
    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    imageBtn.addEventListener("click", () => imageInput.click());
    fileBtn.addEventListener("click", () => fileInput.click());

    imageInput.addEventListener("change", () => {
      const f = imageInput.files && imageInput.files[0];
      imageInput.value = "";
      if (f) sendVision(f);
    });

    fileInput.addEventListener("change", () => {
      const f = fileInput.files && fileInput.files[0];
      fileInput.value = "";
      if (f) sendFile(f);
    });
  </script>
</body>
</html>
