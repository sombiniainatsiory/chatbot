from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import json

# Charger les variables d'environnement
import environ
env =  environ.Env()
# Configurer Google Generative AI
genai.configure(api_key='AIzaSyBNYk2LInNEfTA8og-bvNJfKHbys4cGiXs')
messages=[
   {
      "role": "user",
      "parts": [
        "Bonjour\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Bonjour !  Merci de vous présenter.  Avant de commencer, pourriez-vous me décrire le poste pour lequel vous souhaitez un entretien simulé ?  Plus vous serez précis, mieux je pourrai me mettre dans la peau du recruteur adéquat.  N'hésitez pas à décrire les responsabilités, les compétences requises, le contexte et l'environnement de travail idéal.\n",
      ],
    },
 
  ]
# Configuration du modèle
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
   system_instruction="je suis un chatbot qui simule un entretien d'embauche, dans la premiere interaction l'utilisateur va devoir descrire le poste pour laaquelle il ou elle aimerait avoir. Puis je donne un sinal de debut de similation et je commence. Je me mets à la place d'un recruteur qui varie selon le poste pour laquelle on postule et je pose les questions les plus frequentes et les questions piege.\nPuis je donne une note sur 10 par rapport aux reponses. L'entretien dois etre très humain et pas trot interrogatoire. ",
)

class ChatbotView(APIView):
    def post(self, request):
        # Vérifiez que le contenu est JSON
        if not request.content_type == "application/json":
            return Response(
                {"error": "Le type de contenu doit être 'application/json'."},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        
        # Récupérer et traiter le message
        user_message = request.data.get("message")
        if not user_message:
            return Response(
                {"error": "Message non fourni."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Simuler une réponse du chatbot
        chat_session = model.start_chat(history=messages)
        response = chat_session.send_message(user_message)
        formatted_response = response.text.replace('*', '')
       
        
        return Response(formatted_response, status=status.HTTP_200_OK, content_type="text/plain")
