import json
import random
import string
import nltk
import os
import unicodedata
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class NeuralChatbot:
    def __init__(self):
        # Configurar la ruta de datos de NLTK
        self.nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
        if not os.path.exists(self.nltk_data_path):
            os.makedirs(self.nltk_data_path)
        nltk.data.path.append(self.nltk_data_path)

        # Inicializar componentes NLP
        self.stemmer = PorterStemmer()
        self.vectorizer = CountVectorizer()

        # Descargar recursos necesarios de NLTK
        try:
            # Descargar solo los recursos esenciales
            nltk.download('punkt', download_dir=self.nltk_data_path, quiet=True)
            nltk.download('stopwords', download_dir=self.nltk_data_path, quiet=True)

            # Configurar stopwords en español
            try:
                self.stop_words = set(stopwords.words('spanish'))
            except LookupError:
                print("Descargando datos de idioma español...")
                nltk.download('spanish', download_dir=self.nltk_data_path, quiet=True)
                self.stop_words = set(stopwords.words('spanish'))

        except Exception as e:
            print(f"Error al inicializar recursos NLTK: {e}")
            print(f"Ruta de datos NLTK: {self.nltk_data_path}")
            self.stop_words = set()

        # Cargar base de conocimientos
        try:
            with open('intents.json', 'r', encoding='utf-8') as file:
                self.intents = json.load(file)

            # Preparar patrones para vectorización con normalización
            all_patterns = []
            for intent in self.intents['intents']:
                processed_patterns = [self.word_normalization(pattern) for pattern in intent['patterns']]
                all_patterns.extend(processed_patterns)
            self.vectorizer.fit(all_patterns)

        except Exception as e:
            print(f"Error al inicializar el chatbot: {e}")
            self.intents = {"intents": []}

    def word_normalization(self, words):
        """Normalización de texto con manejo de acentos"""
        try:
            # Normalizar el texto
            texto_normalizado = unicodedata.normalize('NFD', words)

            # Eliminar caracteres especiales y acentos
            texto_sin_acentos = re.sub(r'[\u0300-\u036f]', '', texto_normalizado)

            # Eliminar signos especiales pero mantener estructura de palabras
            texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sin_acentos)

            return texto_limpio.lower()
        except Exception as e:
            print(f"Error en normalización de palabras: {e}")
            return words

    def preprocess_text(self, text):
        """Preprocesamiento de texto con normalización mejorada"""
        try:
            # Aplicar normalización de palabras
            text = self.word_normalization(text.lower())

            # Tokenización y stemming
            tokens = word_tokenize(text)
            tokens = [self.stemmer.stem(token) for token in tokens]

            return ' '.join(tokens)
        except Exception as e:
            print(f"Error en preprocesamiento: {e}")
            return text.lower()

    def calculate_similarity(self, text1, text2):
        """Cálculo de similitud usando CountVectorizer"""
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
        """Obtener respuesta con mejor manejo de errores y umbral de confianza"""
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