import shutil

shutil.copy('server.js', 'server.js.backup_ai')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// ===== AI ASSISTANT ENDPOINT =====
const { GoogleGenerativeAI } = require('@google/generative-ai');

app.post('/api/ai/chat', auth, async (req, res) => {
    try {
        const { message, history } = req.body;
        if (!message) return res.status(400).json({ success: false, error: 'Message waa loo baahan yahay' });

        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) return res.status(400).json({ success: false, error: 'GEMINI_API_KEY ma jiro' });

        const genAI = new GoogleGenerativeAI(apiKey);
        const model = genAI.getGenerativeModel({
            model: 'gemini-1.5-flash',
            systemInstruction: 'Waxaad tahay ABDI VIP PANEL Assistant — kaaliye caqli badan oo ku hadla Soomaali iyo Ingiriisi. Waxaad ka caawinaysaa users-ka panel-ka: license, referrals, dashboard, iwm. Jawaabaha waa in ay gaaban yihiin, cad yihiin, oo faa\'iido leh. Ha bixin talooyin sharci-darro ah.'
        });

        const chat = model.startChat({
            history: (history || []).map(h => ({
                role: h.role === 'user' ? 'user' : 'model',
                parts: [{ text: h.text }]
            }))
        });

        const result = await chat.sendMessage(message);
        const response = result.response.text();

        res.json({ success: true, response: response });
    } catch (err) {
        console.error('AI error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. AI endpoint: OK")
else:
    print("1. AI endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai")
