# What is Prompt Engineering
The quality of responses from generative AI assistants not only depends on the language model used, but on the types of prompts users provide. Prompts are ways we tell an application what we want it to do. You can get the most useful completions by being explicit about the kind of response you want. Take this example, "Summarize the key considerations for adopting Copilot described in this document for a corporate executive. Format the summary as no more than six bullet points with a professional tone." Users of generative AI can achieve better results when you submit clear, specific prompts.

Prompt Engineering is the practice of designing and refining inputs to guide AI models toward producing desired outputs. Tokenization: The process of converting text into smaller units, called tokens, that a model can understand and process. Instruction-Tuned LLMs: Large Language Models (LLMs) that have been fine-tuned with specific instructions to improve their response accuracy and relevance.  We can think of this as a 2-step process:

- designing the initial prompt for a given model and objective
- refining the prompt iteratively to improve the quality of the response



![A screenshot of the considerations for improving a copilot response that corresponds with the numbered list below.](../media/writing-prompts.png)

Prompt Engineering Involves Constructing prompts to:
- Maximize relevancy and accuracy of completions
- Specify formatting and style of completions
- Provide conversational context
- Mitigate bias and improve fairness

<a href="http://www.youtube.com/watch?feature=player_embedded&v=vGdyePbGNaE
" target="_blank"><img src="https://img.youtube.com/vi/vGdyePbGNaE/1.jpg" 
alt="Bias in AI" width="240" height="180" border="10" /></a>


## Prompt Engineering Techniques

Below is a list of five different prompt engineering techniques that are used to generate useful results. A short description is provided here, but if you click on the name of the technique, it will lead you to a page with more information and examples.

#### Zero-Shot

This method involves providing the AI with a task without any prior examples, relying solely on the detailed description of what is needed, under the assumption that the AI has no prior knowledge of the task. [More Details](https://www.promptingguide.ai/techniques/zeroshot)

#### One-Shot
One example is provided along with the prompt. This helps the AI understand the expected context or format. [More Details](https://www.analyticsvidhya.com/blog/2024/07/one-shot-prompting/)

#### Few-Shot
A few examples (usually between 2 to 5) are given to help the AI understand the pattern or style of the desired response. [More Details](https://www.promptingguide.ai/techniques/fewshot)

#### Prompt Chaining 
Complex tasks are broken down into smaller prompts, and the outputs are chained together to form a final comprehensive response. [More Details](https://www.promptingguide.ai/techniques/prompt_chaining)


## Techniques for Improving the Response
Consider the following ways you can improve the response a generative AI assistant provides:

1. Start with a specific goal for what you want the assistant to do
2. Provide a source to ground the response in a specific scope of information
3. Add context to maximize response appropriateness and relevance
4. Set clear expectations for the response
5. Iterate based on previous prompts and responses to refine the result

In most cases, an agent doesn't just send your prompt as-is to the language model. Usually, your prompt is augmented with:
- A *system message* that sets conditions and constraints for the language model behavior. For example, "You're a helpful assistant that responds in a cheerful, friendly manner." These system messages determine constraints and styles for the model's responses.
- The conversation history for the current session, including past prompts and responses. The history enables you to refine the response iteratively while maintaining the context of the conversation.
- The current prompt – potentially optimized by the agent to reword it appropriately for the model or to add more grounding data to scope the response.

The term *prompt engineering* describes the process of prompt improvement. Both developers who design applications and consumers who use those applications can improve the quality of responses from generative AI by considering prompt engineering. 


## Exercise 
[Comparing Prompts and LLMs](../lesson2/exercises/comparing-llms.md)