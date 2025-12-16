// gemini.service.js
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

// Zod Schemas
const ingredientSchema = z.object({
  name: z.string(),
  quantity: z.string(),
});

const recipeSchema = z.object({
  recipe_name: z.string(),
  prep_time_minutes: z.number().optional(),
  ingredients: z.array(ingredientSchema),
  instructions: z.array(z.string()),
});

export const extractRecipe = async (text) => {
  const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY,
  });

  const prompt = `Extract a recipe from this text:\n\n${text}`;

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: prompt,
    generationConfig: {
      responseMimeType: "application/json",
      responseJsonSchema: zodToJsonSchema(recipeSchema),
    },
  
  });

  // Parse and return the JSON
  return JSON.parse(response.response.text());
};
