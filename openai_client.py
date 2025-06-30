import openai


class OpenAIClient:
    def __init__(self, api_key: str, system_prompt: str):
        self.client = openai.Completion(api_key=api_key)
        self.system_prompt = system_prompt

    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-o2",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message['content'] if response.choices else ""