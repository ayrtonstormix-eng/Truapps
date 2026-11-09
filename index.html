<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Truapps</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.13/dist/hls.min.js"></script>
</head>
<body class="bg-black text-white font-sans">
<div id="root"></div>

<script>
  // ===== CONFIGURATION =====
  // Adresse du serveur. En ligne, mettez l'adresse HTTPS de votre API (ex. https://api.truapps.com).
  const API_URL = "http://localhost:8000";
  const WS_URL = API_URL.replace(/^http/, "ws");
  const PAYPAL_URL = "https://www.paypal.com/ncp/payment/WUA2AMNBHLDPS";
  const SUBSCRIPTION_PRICE = 10;

  const h = React.createElement;
  const { useState, useEffect, useRef } = React;

  // ----- Lecteur vidéo HLS -----
  function VideoPlayer({ src }) {
    const ref = useRef(null);
    useEffect(() => {
      const v = ref.current;
      if (!v || !src) return;
      if (v.canPlayType("application/vnd.apple.mpegurl")) {
        v.src = src;
        return;
      }
      if (window.Hls && Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(src);
        hls.attachMedia(v);
        return () => hls.destroy();
      }
    }, [src]);
    return h("video", { ref, controls: true, playsInline: true, className: "w-full h-full object-contain bg-black" });
  }

  // ----- Fil vertical type TikTok -----
  function Feed({ token }) {
    const [videos, setVideos] = useState([]);
    const [liked, setLiked] = useState({});
    const [error, setError] = useState("");

    useEffect(() => {
      fetch(API_URL + "/api/feed", { headers: { Authorization: "Bearer " + token } })
        .then(r => { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(data => setVideos(Array.isArray(data) ? data : []))
        .catch(e => setError("Impossible de charger le fil : " + e.message));
    }, [token]);

    async function toggleLike(id) {
      const next = !liked[id];
      setLiked(p => ({ ...p, [id]: next })); // mise à jour optimiste
      try {
        const r = await fetch(API_URL + "/api/recommendations/interact", {
          method: "POST",
          headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
          body: JSON.stringify({ video_id: id, interaction: next ? "LIKE" : "UNLIKE" })
        });
        if (!r.ok) throw new Error("HTTP " + r.status);
      } catch (e) {
        setLiked(p => ({ ...p, [id]: !next })); // annulation si le serveur refuse
        setError("Le « j'aime » n'a pas été enregistré.");
      }
    }

    return h("div", { className: "flex justify-center" },
      h("div", { className: "w-full max-w-md h-[80vh] bg-zinc-950 rounded-2xl border border-zinc-800 overflow-y-scroll snap-y snap-mandatory" },
        error && h("p", { className: "p-3 text-sm text-red-400" }, error),
        videos.length === 0 && !error && h("p", { className: "p-6 text-zinc-400" }, "Aucune vidéo pour le moment."),
        videos.map(v =>
          h("div", { key: v.id, className: "relative w-full h-full snap-start flex items-center justify-center bg-black" },
            v.hls_url
              ? h(VideoPlayer, { src: v.hls_url })
              : h("span", { className: "text-zinc-600 text-xs" }, "Vidéo indisponible"),
            h("div", { className: "absolute bottom-0 inset-x-0 p-5 bg-gradient-to-t from-black/90 to-transparent flex justify-between items-end" },
              h("div", null,
                h("h3", { className: "font-bold" }, v.user || "@createur"),
                h("p", { className: "text-sm text-zinc-300" }, v.description)
              ),
              h("button", {
                onClick: () => toggleLike(v.id),
                className: "p-3 bg-zinc-800 rounded-full transition active:scale-90"
              }, liked[v.id] ? "❤️" : "🤍")
            )
          )
        )
      )
    );
  }

  // ----- Discussion privée en temps réel -----
  function Chat({ token }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [to, setTo] = useState("");
    const [status, setStatus] = useState("connexion…");
    const ws = useRef(null);

    useEffect(() => {
      const sock = new WebSocket(WS_URL + "/ws/chat");
      ws.current = sock;
      sock.onopen = () => {
        // Le jeton part dans le premier message, jamais dans l'adresse
        sock.send(JSON.stringify({ type: "auth", token }));
        setStatus("connecté");
      };
      sock.onmessage = e => {
        try { setMessages(p => [...p, JSON.parse(e.data)]); } catch (_) {}
      };
      sock.onerror = () => setStatus("erreur de connexion");
      sock.onclose = () => setStatus("déconnecté");
      return () => sock.close();
    }, [token]);

    function send(e) {
      e.preventDefault();
      const sock = ws.current;
      if (!input.trim() || !to.trim() || !sock || sock.readyState !== WebSocket.OPEN) return;
      sock.send(JSON.stringify({ type: "message", receiver: to.trim(), message: input.trim() }));
      setInput("");
    }

    return h("div", { className: "w-full max-w-md mx-auto h-[70vh] flex flex-col bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden" },
      h("div", { className: "p-3 bg-zinc-800 font-bold flex justify-between text-sm" },
        h("span", null, "Messages privés"),
        h("span", { className: "text-zinc-400 font-normal" }, status)
      ),
      h("input", {
        value: to, onChange: e => setTo(e.target.value), placeholder: "Destinataire (ex. @pseudo)",
        className: "p-2 bg-zinc-950 text-sm border-b border-zinc-800 focus:outline-none"
      }),
      h("div", { className: "flex-1 overflow-y-auto p-3 space-y-2 bg-zinc-950" },
        messages.map((m, i) =>
          h("div", { key: i, className: "flex flex-col " + (m.mine ? "items-end" : "items-start") },
            h("div", { className: "p-2 rounded-lg text-sm max-w-[80%] " + (m.mine ? "bg-red-600" : "bg-zinc-800") },
              (m.sender ? m.sender + " : " : "") + (m.message || "")
            )
          )
        )
      ),
      h("form", { onSubmit: send, className: "p-2 flex gap-2 bg-zinc-900 border-t border-zinc-800" },
        h("input", {
          value: input, onChange: e => setInput(e.target.value),
          className: "flex-1 bg-zinc-950 rounded p-2 text-sm border border-zinc-700 focus:outline-none"
        }),
        h("button", { type: "submit", className: "bg-red-600 px-4 rounded text-sm font-bold" }, "Envoyer")
      )
    );
  }

  // ----- Application principale -----
  function App() {
    const [session, setSession] = useState(null); // { token, username, subscribed }
    const [tab, setTab] = useState("feed");
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");

    async function login(e) {
      e.preventDefault();
      setError("");
      try {
        const r = await fetch(API_URL + "/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email.trim() })
        });
        if (!r.ok) throw new Error("HTTP " + r.status);
        setSession(await r.json());
      } catch (err) {
        setError("Connexion impossible : " + err.message);
      }
    }

    if (!session) {
      return h("form", { onSubmit: login, className: "max-w-sm mx-auto mt-16 p-6 bg-zinc-900 rounded-2xl space-y-4" },
        h("h2", { className: "text-xl font-bold" }, "Connexion"),
        h("input", {
          type: "email", value: email, onChange: e => setEmail(e.target.value),
          placeholder: "E-mail", className: "w-full p-2 rounded bg-zinc-800"
        }),
        error && h("p", { className: "text-sm text-red-400" }, error),
        h("button", { type: "submit", className: "w-full p-2 rounded bg-red-600 font-bold" }, "Entrer")
      );
    }

    const tabBtn = (id, label) => h("button", {
      onClick: () => setTab(id),
      className: "px-3 py-1 rounded text-sm " + (tab === id ? "bg-red-600" : "bg-zinc-800")
    }, label);

    return h("div", { className: "min-h-screen" },
      h("header", { className: "flex justify-between items-center px-6 py-4 border-b border-zinc-800" },
        h("span", { className: "font-black tracking-wider" }, "TRUAPPS"),
        h("div", { className: "flex gap-2" },
          tabBtn("feed", "Fil"),
          tabBtn("chat", "Messages"),
          h("button", { onClick: () => setSession(null), className: "px-3 py-1 rounded text-sm border border-zinc-700" }, "Quitter")
        )
      ),
      h("main", { className: "p-4" },
        !session.subscribed && h("div", { className: "max-w-md mx-auto mb-4 p-3 bg-zinc-900 rounded-xl text-sm flex justify-between items-center gap-3" },
          h("span", null, "Abonnement : " + SUBSCRIPTION_PRICE + " $ / mois"),
          h("a", { href: PAYPAL_URL, target: "_blank", rel: "noopener noreferrer", className: "px-3 py-1 rounded bg-yellow-500 text-black font-bold" }, "Payer")
        ),
        tab === "feed" ? h(Feed, { token: session.token }) : h(Chat, { token: session.token })
      )
    );
  }

  ReactDOM.createRoot(document.getElementById("root")).render(h(App));
</script>
</body>
</html>
