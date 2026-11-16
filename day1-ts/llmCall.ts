import { GoogleGenAI } from "@google/genai";

const MODEL = "gemini-3.5-flash";
const SYSTEM_PROMPT =
  "You are a URA tax officer helping a small-business owner in Kampala " +
  "who has no tax background. " +
  "Answer in short, plain language and avoid jargon. " +
  "Do not state fees, penalties or deadlines unless you are certain of them. " +
  "End by advising the person to confirm the details with URA.";
const QUESTION = "What is TIN registration and do I need it for my shop?";

const ai = new GoogleGenAI({});

async function main(): Promise<void> {
    const response = await ai.models.generateContent({
        model: MODEL,
        contents: QUESTION,
        config: { systemInstruction: SYSTEM_PROMPT, temperature: 1.5}
    });

    console.log(response.text);

    const usage = response.usageMetadata;
    console.log('promptTokenCount: ', usage?.promptTokenCount);
    console.log('candidatesTokenCount: ', usage?.candidatesTokenCount);
    console.log('thoughtsTokenCount: ', usage?.thoughtsTokenCount);
    console.log('totalTokenCount: ', usage?.totalTokenCount);
}

main();