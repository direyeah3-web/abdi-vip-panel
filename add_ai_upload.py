import shutil

shutil.copy('server.js', 'server.js.backup_ai_upload')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

old = "app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"

new = """// ===== AI UPLOAD ENDPOINT =====
const multer = require('multer');
const upload = multer({
    storage: multer.memoryStorage(),
    limits: { fileSize: 20 * 1024 * 1024 } // 20MB
});

app.post('/api/ai/upload', auth, upload.single('file'), async (req, res) => {
    try {
        if (!req.file) return res.status(400).json({ success: false, error: 'File ma jiro' });

        const file = req.file;
        const mime = file.mimetype;
        const base64 = file.buffer.toString('base64');

        // Kaliya sawirrada & videos-ka yar-yar
        if (!mime.startsWith('image/') && !mime.startsWith('video/') && !mime.startsWith('text/') && mime !== 'application/pdf') {
            return res.status(400).json({ success: false, error: 'Nooca file-ka lama aqbalo' });
        }

        res.json({
            success: true,
            filename: file.originalname,
            mimetype: mime,
            size: file.size,
            data: base64,
            preview: mime.startsWith('image/') ? `data:${mime};base64,${base64}` : null
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// POST /api/ai/chat-with-file — file + message
app.post('/api/ai/chat-with-file', auth, upload.single('file'), async (req, res) => {
    try {
        const { message } = req.body;
        const file = req.file;
        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) return res.status(400).json({ success: false, error: 'GEMINI_API_KEY ma jiro' });
        if (!file && !message) return res.status(400).json({ success: false, error: 'Message ama file waa loo baahan yahay' });

        const { GoogleGenerativeAI } = require('@google/generative-ai');
        const genAI = new GoogleGenerativeAI(apiKey);

        const userRole = req.user && req.user.role ? req.user.role : 'user';
        const isAdmin = userRole === 'admin';
        const systemPrompt = isAdmin
            ? "Waxaad tahay ABDI VIP PANEL AI Assistant — kaaliye admin ah. Waxaad ka jawaabtaa sawirrada, videos-ka, iyo file-yada. Jawaabahaagu waa in ay cad yihiin, degdeg ah, oo faa'iido leh. Isticmaal emoji-ga si dabiici ah."
            : "Waxaad tahay ABDI VIP PANEL AI Assistant — kaaliye user ah. Waxaad ka jawaabtaa sawirrada, videos-ka, iyo file-yada. Jawaabahaagu waa in ay cad yihiin, degdeg ah. Isticmaal emoji-ga si dabiici ah.";

        const models = ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-2.5-flash', 'gemini-1.5-flash'];
        let response = null;
        let lastError = null;

        for (const modelName of models) {
            try {
                const model = genAI.getGenerativeModel({
                    model: modelName,
                    systemInstruction: systemPrompt,
                    generationConfig: { maxOutputTokens: 2048, temperature: 0.7 }
                });

                const parts = [];
                if (file) {
                    parts.push({
                        inlineData: {
                            mimeType: file.mimetype,
                            data: file.buffer.toString('base64')
                        }
                    });
                }
                if (message) parts.push({ text: message });
                else parts.push({ text: 'Falanqee file-kan.' });

                const result = await model.generateContent(parts);
                response = result.response.text();
                console.log('✅ AI file model:', modelName);
                break;
            } catch (err) {
                lastError = err;
                console.log('❌ Model', modelName, 'failed:', err.message.substring(0, 80));
                continue;
            }
        }

        if (!response) {
            return res.status(503).json({ success: false, error: 'AI server-ka mashquul. Fadlan 10 daqiiqo kadib dib u tijaabi. 😭' });
        }

        res.json({ success: true, response: response });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

app.listen(PORT, () => console.log('ABDI VIP PANEL running on port ' + PORT));"""

if old in c:
    c = c.replace(old, new, 1)
    print("1. AI upload endpoint: OK")
else:
    print("1. AI upload endpoint: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_upload")
