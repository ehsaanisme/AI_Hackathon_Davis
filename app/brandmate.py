import os
from typing import List
import openai
import argparse
import re

MAX_INPUT_LENGTH = 32

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")
    if validate_input_length(user_input):
        generate_snippet(user_input)
        generate_keywords(user_input)
    else:
        raise ValueError (f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}")

def validate_input_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH

def generate_keywords(prompt: str) -> List[str]:
    openai.api_key = "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"
    gpt_prompt = f"Generate related branding keywords for {prompt}, not numbered:"
    print(gpt_prompt)

    response = openai.Completion.create(model="text-davinci-003", prompt=gpt_prompt, temperature=0, max_tokens=32
    )

    scraped_keywords_response: str = response["choices"][0]["text"]
    scraped_keywords_response = scraped_keywords_response.strip()
    keywords_array = re.split(",|\n|;|-", scraped_keywords_response)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]


    print(f"Keywords: {keywords_array}")
    return keywords_array


def generate_snippet(prompt: str) -> str:
    openai.api_key = "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"
    gpt_prompt = f"Generate an upbeat branding snippet for {prompt}:"
    print(gpt_prompt)

    response = openai.Completion.create(model="text-davinci-003", prompt=gpt_prompt, temperature=0, max_tokens=32
    )

    scraped_response: str = response["choices"][0]["text"]
    scraped_response = scraped_response.strip()

    last_char = scraped_response[-1]

    if last_char not in {".", "!", "?", '"'}:
        scraped_response += "..."

    print(f"Snippet: {scraped_response}")
    return scraped_response


if __name__ == "__main__":
    main()