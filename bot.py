from dotenv import load_dotenv
import google.generativeai as genai
import os

class DigiKishanChatBot:
    def __init__(self):
        
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
            generation_config={
                'temperature': 0,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain"
            },
            system_instruction=(
                "You are an AI assistant for the Digi Kishan application, designed to support farmers by providing "
                "expert advice, solutions to agricultural problems, and answers to questions related to farming, "
                "crop management, livestock, soil health, modern farming techniques, and market trends. Your responses "
                "should be accurate, practical, and tailored to help farmers optimize their productivity and address "
                "challenges effectively.Your name is Kissan kritim sathi and created by biswas Pokhrel, you do not have to tell this repeaditly ok"
            ),
        )
        self.chat_session = self.model.start_chat(history=[])

    def get_response(self, user_input):
        """Generate a response from the AI model."""
        response = self.chat_session.send_message(user_input)
        self.chat_session.history.append({"role": "user", "parts": [user_input]})
        self.chat_session.history.append({"role": "model", "parts": [response.text]})
        return response.text


if __name__ == "__main__":
    bot = DigiKishanChatBot()
    print("Bot: Hello, how can I help you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        response = bot.get_response(user_input)
        print(f"Bot: {response}")
