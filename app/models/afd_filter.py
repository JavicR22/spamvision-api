import re
from collections import Counter

class PrefilterAFDwithScoreRobust:
    def __init__(self, pattern_file=None):
        # Estados
        self.inicio = 'q0'
        self.spam_state = 'q5'
        self.nospam_state = 'q6'

        # Transiciones (deterministas)
        self.trans = {
            'q0': {'A': 'q1', 'B': 'q2', 'C': 'q3', 'D': 'q4'},
            'q1': {'A': 'q2', 'B': 'q2', 'C': 'q3', 'D': 'q4'},
            'q2': {'A': 'q2', 'B': 'q2', 'C': 'q3', 'D': 'q4'},
            'q3': {'A': 'q5', 'B': 'q3', 'C': 'q5', 'D': 'q5'},
            'q4': {'A': 'q5', 'B': 'q4', 'C': 'q5', 'D': 'q5'},
            'q5': {'A': 'q5', 'B': 'q5', 'C': 'q5', 'D': 'q5'},
            'q6': {'A': 'q6', 'B': 'q6', 'C': 'q6', 'D': 'q6'}
        }

        # Cargar patrones externos si hay, si no usar defaults
        if pattern_file:
            self.patterns = self.load_patterns(pattern_file)
        else:
            self.patterns = self.default_patterns()

        # Bigramas/frases importantes (puedes mover esto a archivo también)
        self.bigrams = [
            (r'ha ganado', 'A'),
            (r'premio garantizado', 'A'),
            (r'mensaje de texto', 'D'),
            (r'env[ií]e un mensaje', 'D'),
            (r'env[ií]e su n[úu]mero', 'D'),
            (r'Participa en el','A'),
            (r'entra a tu', 'A')
        ]

        # Regex de tokenización: incluye underscores y números
        self.token_re = re.compile(r"[A-Za-z\u00C0-\u017F0-9_]+", re.UNICODE)

        # Pesos y umbral
        self.weights = {'A': 2.5, 'C': 3.0, 'D': 2.0, 'B': -0.5}
        self.threshold_spam = 3.0

        # Regex útiles pre-tokenizado
        # URL completa (http/https), enlaces short (wa.me), dominios con TLDs comunes
        self.re_url = re.compile(r'https?://\S+|www\.\S+|\b(?:\w[\w-]*\.)+(?:com|co|me|ac|net|org|gov)\b', re.IGNORECASE)
        self.re_whatsapp = re.compile(r'wa\.me/\d+|\bwhatsapp\b', re.IGNORECASE)
        # Números con separadores (330,000 or 330.000) → normalizar
        self.re_currency = re.compile(r'(\d{1,3}(?:[.,]\d{3})+(?:[.,]\d{2})?|\d{6,})')

    def default_patterns(self):
        return {
            'A': [r'premio', r'ganad[oa]s?', r'gana', r'gratis', r'efectivo', r'oferta', r'promoci[oó]n', r'salario', r'oportunidad', r'ingresos?'],
            'B': [r'\b(hola|gracias|buen|reuni[oó]n|familia|compra|pedido|mañana|tarde|buenos|no|por|favor|hola,?)\b'],
            'C': [r'\b3\d{2,}\b', r'\b\d{7,}\b', r'https?://', r'\bwww\.', r'\.co\b', r'\.com\b', r'\.me\b', r'wa\.me'],
            'D': [r'llame', r'env[ií]e', r'ahora', r'mensaje', r'movil', r'móvil', r'tel[eé]fono', r'número', r'contact', r'contactame', r'whatsap', r'whatsapp']
        }

    def load_patterns(self, path):
        """
        Lee archivo tipo:
        A: premio|gana|gratis
        B: \b(hola|gracias)\b
        ...
        Devuelve diccionario {'A':[pat1,pat2], ...}
        Normaliza claves a mayúscula y valida cada regex.
        """
        patterns = {}
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    key, regexes = line.split(':', 1)
                    key = key.strip().upper()
                    regex_list = [r.strip() for r in regexes.split('|') if r.strip()]
                    # validar cada regex
                    for r_exp in regex_list:
                        re.compile(r_exp)
                    patterns[key] = regex_list
                except re.error as e:
                    # imprime info y continúa con el resto
                    print(f"⚠️ Error regex en línea {i}: '{line}'  → {e}")
                except Exception as e:
                    print(f"⚠️ Error leyendo línea {i}: '{line}'  → {e}")
        # Asegurar que A,B,C,D existan; si faltan, completar con defaults
        defaults = self.default_patterns()
        for k in ['A','B','C','D']:
            if k not in patterns or not patterns[k]:
                patterns[k] = defaults[k]
        return patterns

    def map_token(self, token):
        """
        Mapear token a categoría A/B/C/D.
        Si token es marca de frase '__X_PHRASE__' extrae X.
        """
        if '_PHRASE' in token:
            m = re.search(r'__([A-Z])_PHRASE__', token)
            if m:
                return m.group(1)
        # comprobar patrones cargados
        for cat, pats in self.patterns.items():
            for p in pats:
                if re.search(p, token, re.IGNORECASE):
                    return cat
        return 'B'

    def process(self, text, debug=False):
        estado = self.inicio
        text_low = text.lower()

        # 1) Normalizar números con separadores (330,000 -> 330000)
        text_low = self.re_currency.sub(lambda m: m.group(0).replace('.', '').replace(',', ''), text_low)

        # 2) Marcar URLs/dominios/wa.me como C antes de tokenizar
        # Primero marcas enlaces completos
        text_low = self.re_url.sub('__C_PHRASE__', text_low)
        # marcas explicitamente WA links
        text_low = self.re_whatsapp.sub('__C_PHRASE__', text_low)

        # 3) Marcar bigramas (frases) si existen
        for pat, cat in self.bigrams:
            text_low = re.sub(pat, f'__{cat}_PHRASE__', text_low, flags=re.IGNORECASE)

        # 4) Tokenizar
        tokens = self.token_re.findall(text_low)
        counts = Counter()
        history = []

        # 5) Recorrer tokens
        for t in tokens:
            cat = self.map_token(t)
            counts[cat] += 1
            prev = estado
            estado = self.trans.get(estado, {}).get(cat, estado)
            history.append((t, cat, prev, estado))

            # Stop early if absorbente
            if estado in (self.spam_state, self.nospam_state):
                break

        # 6) Scoring
        score = sum(self.weights.get(k, 0.0) * v for k, v in counts.items())

        if debug:
            print("Texto (preprocesado):", text_low)
            print("Tokens:", tokens)
            for h in history:
                print(f" token='{h[0]}' cat={h[1]} {h[2]} -> {h[3]}")
            print("Counts:", dict(counts))
            print("Score:", score)
            print("Estado final (AFD):", estado)

        # 7) Decisión (priorizar AFD si llegó a absorbente)
        if estado == self.spam_state:
            return "SPAM"
        if estado == self.nospam_state:
            return "NO-SPAM"
        # Si AFD no resolvió, usar score
        if score >= self.threshold_spam:
            return "SPAM"
        return "NO-SPAM"