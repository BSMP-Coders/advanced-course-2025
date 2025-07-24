# Large Language Models

The main capability of a Large Language Model is generating a text from scratch, starting from a textual input, written in natural language.
But what kind of textual input and output? The input of a large language model is known as a *prompt*, while the output is known as a *completion*, term that refers to the model mechanism of generating the next token to complete the current input.

Today, importantly, developers don't need to train models from scratch. To build a generative AI application, you can use pretrained models. Some language models 
are open-source and publicly available. Others are offered in proprietary catalogs. Different models exist today which mostly differ by the specific data used to train them, or by how they implement attention within their architectures. 

## How Do Large Language Models Work
Large Language Models receive a text as input and generate a text as output. However, being statistical models, they work much better with numbers than text sequences. That’s why every input to the model is processed by a tokenizer, before being used by the core model. A token is a chunk of text – consisting of a variable number of characters, so the tokenizer's main task is splitting the input into an array of tokens. Then, each token is mapped with a token index, which is the integer encoding of the original text chunk.

![Tokenizer](../media/tokenizer-example.png)

## Understand different types of LLMs

LLMs can have multiple categorizations based on their architecture, training data, and use case. Understanding these differences will help our startup select the right model for the scenario, and understand how to test, iterate, and improve performance.

There are many different types of LLM models, your choice of model depends on what you aim to use them for, your data, how much you're ready to pay and more.

Depending on if you aim to use the models for text, audio, video, image generation and so on, you might opt for a different type of model.

- **Audio and speech recognition**. For this purpose, Whisper-type models are a great choice as they're general-purpose and aimed at speech recognition. It's trained on diverse audio and can perform multilingual speech recognition. Learn more about [Whisper type models here](https://platform.openai.com/docs/models/whisper?WT.mc_id=academic-105485-koreyst).

- **Image generation**. For image generation, DALL-E and Midjourney are two very well-known choices. DALL-E is offered by Azure OpenAI. [Read more about DALL-E here](https://platform.openai.com/docs/models/dall-e?WT.mc_id=academic-105485-koreyst) and also in Chapter 9 of this curriculum.

- **Text generation**. Most models are trained on text generation and you have a large variety of choices from GPT-3.5 to GPT-4. They come at different costs with GPT-4 being the most expensive. It's worth looking into the [Azure OpenAI playground](https://oai.azure.com/portal/playground?WT.mc_id=academic-105485-koreyst) to evaluate which models best fit your needs in terms of capability and cost.

- **Multi-modality**. If you're looking to handle multiple types of data in input and output, you might want to look into models like [gpt-4 turbo with vision or gpt-4o](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#gpt-4-and-gpt-4-turbo-models?WT.mc_id=academic-105485-koreyst) - the latest releases of OpenAI models - which are capable to combine natural language processing to visual understanding, enabling interactions through multi-modal interfaces.

Selecting a model means you get some basic capabilities, that might not be enough however. Often you have company specific data that you somehow need to tell the LLM about. There are a few different choices on how to approach that, more on that in the upcoming sections.


## Large and small language models
In general, language models can be considered in two categories: *Large Language Models* (LLMs) and *Small Language models* (SLMs).

|Large Language Models (LLMs)|Small Language Models (SLMs)|
|-|-|
|LLMs are trained with vast quantities of text that represent a wide range of general subject matter – typically by sourcing data from the Internet and other generally available publications.| SLMs are trained with smaller, more subject-focused datasets|
|When trained, LLMs have many billions (even trillions) of parameters (weights that can be applied to vector embeddings to calculate predicted token sequences).|Typically have fewer parameters than LLMs.|
|Able to exhibit comprehensive language generation capabilities in a wide range of conversational contexts.|This focused vocabulary makes them effective in specific conversational topics, but less effective at more general language generation.|
|Their large size can impact their performance and make them difficult to deploy locally on devices and computers.|The smaller size of SLMs can provide more options for deployment, including local deployment to devices and on-premises computers; and makes them faster and easier to fine-tune.|
|Fine-tuning the model with more data to customize its subject expertise can be time-consuming, and expensive in terms of the compute power required to perform the extra training.|Fine-tuning can potentially be less time-consuming and expensive.|

## Exercise 
[Learn more about Tokenization](../lesson2/exercises/tokenization.md)