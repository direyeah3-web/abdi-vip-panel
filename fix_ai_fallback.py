import shutil
import re

shutil.copy('server.js', 'server.js.backup_ai_fallback')

with open('server.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Raadi endpoint-ka AI
pattern = r"app\.post\('/api/ai/chat'.*?\n\}\);"
match = re.search(pattern, c, re.DOTALL)

new_ai = """app.post('/api/ai/chat', auth, async (req, res) => {
    try {
        const { message, history } = req.body;
        if (!message) return res.status(400).json({ success: false, error: 'Message waa loo baahan yahay' });

        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) return res.status(400).json({ success: false, error: 'GEMINI_API_KEY ma jiro' });

        const { GoogleGenerativeAI } = require('@google/generative-ai');
        const genAI = new GoogleGenerativeAI(apiKey);

        const systemPrompt = "Waxaad tahay ABDI VIP PANEL AI Assistant — ChatGPT/DeepSeek u eg. Waxaad ku hadashaa Soomaali iyo Ingiriisi. Jawaabahaagu waa in ay cad yihiin, buuxa yihiin, oo faa'iido leh — laakiin DEGDEG ah. Qoraalka waa in uu gaaban yahay, laakiin macne buuxa. Isticmaal emoji-ga si dabiici ah (😊🔥💯✨🚀💻👍). Su'aalaha code-ka, business-ka, general knowledge — dhammaan ka jawaab. Haddii user-ku su'aal weydiiyo oo panel-ka ku saabsan, isticmaal xogta panel-ka. Ka fogow buuq. Haddii su'aashu sharci-darro tahay, si fudud u diid oo soo jeedi beddel sharci ah.";

        // Fallback models — isku day mid kasta
        const models = ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-2.5-flash', 'gemini-1.5-flash'];
        let lastError = null;
        let response = null;

        for (const modelName of models) {
            try {
                const model = genAI.getGenerativeModel({
                    model: modelName,
                    systemInstruction: systemPrompt,
                    generationConfig: {
                        maxOutputTokens: 2048,
                        temperature: 0.7,
                        topP: 0.95
                    }
                });

                const chat = model.startChat({
                    history: (history || []).map(h => ({
                        role: h.role === 'user' ? 'user' : 'model',
                        parts: [{ text: h.text }]
                    }))
                });

                const result = await chat.sendMessage(message);
                response = result.response.text();
                console.log('✅ AI model:', modelName);
                break;
            } catch (err) {
                lastError = err;
                console.log('❌ Model', modelName, 'failed:', err.message.substring(0, 80));
                // Haddii 503, isku day model kale
                continue;
            }
        }

        if (!response) {
            return res.status(503).json({
                success: false,
                error: 'AI server-ka mashquul. Fadlan 10 daqiiqo kadib dib u tijaabi. 😭'
            });
        }

        res.json({ success: true, response: response });
    } catch (err) {
        console.error('AI error:', err);
        res.status(500).json({ success: false, error: err.message });
    }
});"""

if match:
    c = c[:match.start()] + new_ai + c[match.end():]
    print("1. AI fallback: OK")
else:
    print("1. AI fallback: LAMA HELIN")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Backup: server.js.backup_ai_fallback")
