import json
import random
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
try:
    nltk.download('punkt')
    nltk.download('punkt_tab')
except Exception as e:
    print(f"Error descargando recursos NLTK: {e}")
class BloodTypeBot:
    def __init__(self):
        # Inicializar componentes NLP
        self.stemmer = PorterStemmer()
        self.vectorizer = CountVectorizer()

        # Cargar base de conocimientos
        try:
            with open('intents.json', 'r', encoding='utf-8') as file:
                self.intents = json.load(file)

            # Preparar patrones para vectorización
            all_patterns = []
            for intent in self.intents['intents']:
                all_patterns.extend(intent['patterns'])
            self.vectorizer.fit(all_patterns)

        except Exception as e:
            print(f"Error al inicializar el chatbot: {e}")
            self.intents = {"intents": []}

    def preprocess_text(self, text):
        """Preprocesamiento mejorado de texto"""
        try:
            # Convertir a minúsculas y remover puntuación
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))

            # Tokenización y stemming
            tokens = word_tokenize(text)
            tokens = [self.stemmer.stem(token) for token in tokens]

            return ' '.join(tokens)
        except Exception as e:
            print(f"Error en preprocesamiento: {e}")
            return text.lower()

    def calculate_similarity(self, text1, text2):
        """Cálculo de similitud mejorado usando CountVectorizer"""
        try:
            # Preprocesar textos
            text1 = self.preprocess_text(text1)
            text2 = self.preprocess_text(text2)

            # Vectorizar
            vectors = self.vectorizer.transform([text1, text2]).toarray()

            # Calcular similitud coseno
            dot_product = np.dot(vectors[0], vectors[1])
            norm1 = np.linalg.norm(vectors[0])
            norm2 = np.linalg.norm(vectors[1])

            if norm1 == 0 or norm2 == 0:
                return 0

            return dot_product / (norm1 * norm2)

        except Exception as e:
            print(f"Error al calcular similitud: {e}")
            return 0

    def get_response(self, user_input):
        """Obtener respuesta mejorada con mejor manejo de errores y umbral de confianza"""
        try:
            best_score = 0
            best_intent = None

            # Encontrar el intent más similar
            for intent in self.intents['intents']:
                for pattern in intent['patterns']:
                    similarity = self.calculate_similarity(user_input, pattern)

                    if similarity > best_score:
                        best_score = similarity
                        best_intent = intent

            # Umbral de confianza mejorado y respuestas más naturales            
            if best_score > 0.3:  # Umbral más estricto para mejor precisión
                return random.choice(best_intent['responses'])
            elif best_score > 0.1:  # Respuesta para similitud baja
                return "Entiendo que tu pregunta está relacionada con temas médicos, pero ¿podrías reformularla? Como asistente especializado en sangre, quiero asegurarme de darte la información más precisa."
            else:  # Respuesta para cuando no hay coincidencia
                return "Lo siento, como asistente médico especializado en temas de sangre, no puedo responder esa pregunta. ¿Te gustaría saber algo específico sobre tipos de sangre, donaciones o transfusiones?"

        except Exception as e:
            print(f"Error en el chatbot: {e}")
            return "Ha ocurrido un error en mi sistema. Por favor, intenta reformular tu pregunta sobre temas relacionados con la sangre y transfusiones."
