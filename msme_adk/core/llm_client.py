import os, json, requests
from dotenv import load_dotenv
load_dotenv()

LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'gemini').lower()

class LLMClient:
    def __init__(self):
        self.provider = LLM_PROVIDER
        if self.provider == 'gemini':
            self.api_key = os.getenv('GEMINI_API_KEY')
            self.base = os.getenv('GEMINI_API_BASE', 'https://generativelanguage.googleapis.com/v1beta2')
            self.model = os.getenv('GEMINI_MODEL', 'models/text-bison-001')
            if not self.api_key:
                print('[LLMClient] WARNING: GEMINI_API_KEY not set; LLM calls will fail if invoked.')
        else:
            self.api_key = os.getenv('LLM_API_KEY')
            self.base = os.getenv('LLM_API_BASE', 'https://api.openai.com/v1')
            self.model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
            if not self.api_key:
                print('[LLMClient] WARNING: LLM_API_KEY not set; LLM calls will fail if invoked.')

    def complete(self, prompt: str, max_tokens: int = 512, temperature: float = 0.1) -> str:
        if self.provider == 'gemini':
            return self._call_gemini(prompt, max_tokens, temperature)
        else:
            return self._call_openai_compatible(prompt, max_tokens, temperature)

    def _call_gemini(self, prompt: str, max_tokens: int, temperature: float):
        url = f"{self.base}/{self.model}:generate"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        body = {
            'prompt': {'text': prompt},
            'temperature': temperature,
            'maxOutputTokens': max_tokens
        }
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f'Gemini API error: {resp.status_code} {resp.text}')
        data = resp.json()
        candidates = data.get('candidates') or data.get('outputs') or []
        if candidates and isinstance(candidates, list):
            first = candidates[0]
            for k in ('output', 'content', 'text'):
                if k in first:
                    return first[k]
            return json.dumps(first)
        if 'output' in data:
            return data['output']
        return json.dumps(data)

    def _call_openai_compatible(self, prompt: str, max_tokens: int, temperature: float):
        url = f"{self.base}/chat/completions"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        body = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f'OpenAI API error: {resp.status_code} {resp.text}')
        data = resp.json()
        if 'choices' in data and len(data['choices']) > 0:
            msg = data['choices'][0].get('message') or data['choices'][0]
            if isinstance(msg, dict):
                return msg.get('content') or msg.get('text') or json.dumps(msg)
            return str(msg)
        return json.dumps(data)
