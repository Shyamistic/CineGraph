Source: https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing
Title: Agent Platform Pricing | Google Cloud
Fetched: 2026-08-31T12:16:41.737Z

Gemini 3.7 Flash, Gemini 3.6 Flash, and CodeMender using these models are offered with introductory pricing of $0.75 / $3.75 per 1M tokens input / output through December 31, 2026. Starting January 1, 2027, standard pricing of $1.5 / $7.5 per 1M tokens input / output will apply.

## Cost of building and deploying AI models in Agent Platform

Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

You're charged only for requests that return a 200 response code. Requests returning any other response codes, such as 4xx and 5xx codes, aren't charged for the input or output.

This page covers pricing for Generative AI on Agent Platform. For all other Agent Platform pricing including ML Platform and MLOps services please refer to [Agent Platform pricing page](https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing).

Flexible Savings Plans (FSPs) are spend-based committed use discounts that help you save money on your usage across eligible products on Google Cloud. For more information about how FSPs work and eligible products, see [Flexible Savings Plans](https://docs.cloud.google.com/docs/cuds-flexible-savings-plans).

# Google models

## Gemini 3

Standard ModelPriorityFlex/Batch

| Model | Type | Region | Price (/1M tokens)<br><= 200K input tokens | Price (/1M tokens)<br>\> 200K input tokens | Price (/1M tokens)<br><= 200K cached input tokens | Price (/1M tokens)<br>\> 200K cached input tokens |
| Gemini 3.1 Pro Preview | Input (text, image, video, audio) | Global | $2.00 | $4.00 | $0.20 | $0.40 |
|  | Text output (response and reasoning) | Global | $12.00 | $18.00 | N/A | N/A |
| Gemini 3.7 Flash \*<br>through December 31, 2026 | Input (text, image, video, audio) | Global | $0.75 | $0.75 | $0.075 | $0.075 |
|  |  | Non-global | $0.825 | $0.825 | $0.0825 | $0.0825 |
|  | Text output (response and reasoning) | Global | $3.75 | $3.75 | N/A | N/A |
|  |  | Non-global | $4.125 | $4.125 | N/A | N/A |
| Gemini 3.7 Flash<br>starting January 1, 2027 | Input (text, image, video, audio) | Global | $1.50 | $1.50 | $0.15 | $0.15 |
|  |  | Non-global | $1.65 | $1.65 | $0.165 | $0.165 |
|  | Text output (response and reasoning) | Global | $7.50 | $7.50 | N/A | N/A |
|  |  | Non-global | $8.25 | $8.25 | N/A | N/A |
| Gemini 3.6 Flash \*<br>through December 31, 2026 | Input (text, image, video, audio) | Global | $0.75 | $0.75 | $0.075 | $0.075 |
|  |  | Non-global | $0.825 | $0.825 | $0.0825 | $0.0825 |
|  | Text output (response and reasoning) | Global | $3.75 | $3.75 | N/A | N/A |
|  |  | Non-global | $4.125 | $4.125 | N/A | N/A |
| Gemini 3.6 Flash<br>starting January 1, 2027 | Input (text, image, video, audio) | Global | $1.50 | $1.50 | $0.15 | $0.15 |
|  |  | Non-global | $1.65 | $1.65 | $0.165 | $0.165 |
|  | Text output (response and reasoning) | Global | $7.50 | $7.50 | N/A | N/A |
|  |  | Non-global | $8.25 | $8.25 | N/A | N/A |
| Gemini 3 Flash Preview | Input (text, image, video) | Global | $0.50 | $0.50 | $0.05 | $0.05 |
|  | Input (audio) | Global | $1.00 | $1.00 | $0.10 | $0.10 |
|  | Text output (response and reasoning) | Global | $3.00 | $3.00 | N/A | N/A |
| Gemini 3.5 Flash | Input (text, image, video, audio) | Global | $1.50 | $1.50 | $0.15 | $0.15 |
|  |  | Non-global\* | $1.65 | $1.65 | $0.165 | $0.165 |
|  | Text output (response and reasoning) | Global | $9.00 | $9.00 | N/A | N/A |
|  |  | Non-global\* | $9.90 | $9.90 | N/A | N/A |
| Gemini 3.5 Flash-Lite | Input (text, image, video, audio) | Global | $0.30 | $0.30 | $0.03 | $0.03 |
|  |  | Non-global\* | $0.33 | $0.33 | $0.033 | $0.033 |
|  | Text output (response and reasoning) | Global | $2.50 | $2.50 | N/A | N/A |
|  |  | Non-global\* | $2.75 | $2.75 | N/A | N/A |
| Gemini 3.1 Flash-Lite | Input (text, image, video) | Global | $0.25 | $0.25 | $0.025 | $0.025 |
|  |  | Non-global\* | $0.275 | $0.275 | $0.0275 | $0.0275 |
|  | Input (audio) | Global | $0.50 | $0.50 | $0.05 | $0.05 |
|  |  | Non-global\* | $0.55 | $0.55 | $0.055 | $0.055 |
|  | Text output (response and reasoning) | Global | $1.50 | $1.50 | N/A | N/A |
|  |  | Non-global\* | $1.65 | $1.65 | N/A | N/A |
| Gemini 3.1 Flash-Lite Image (Nano Banana 2 Lite) | Input (text, image, video) | Global | $0.25 | N/A | $0.025 | N/A |
|  | Text output (response and reasoning) | Global | $1.50 | N/A | N/A | N/A |
|  | Image Output\*\*\*\* | Global | $30.00 | N/A | N/A | N/A |
| Gemini 3.1 Flash Image (Nano Banana 2) | Input (text, image, video) | Global | $0.50 | N/A | $0.05 | N/A |
|  | Text output (response and reasoning) | Global | $3.00 | N/A | N/A | N/A |
|  | Image Output\*\*\* | Global | $60.00 | N/A | N/A | N/A |
| Gemini 3 Pro Image (Nano Banana Pro) | Input (text, image) | Global | - | N/A | $0.20 | N/A |
|  | Text output (response and reasoning) | Global | $12.00 | N/A | N/A | N/A |
|  | Image Output\*\* | Global | - | N/A | N/A | N/A |

\\* Promotional pricing provided through 50% credits back on net spend on select models within a given period.

| Model | Type | Region | Price (/1M tokens)<br><= 200K input tokens with Priority | Price (/1M tokens)<br>\> 200K input tokens with Priority | Price (/1M tokens)<br><= 200K cached input tokens with Priority | Price (/1M tokens)<br>\> 200K cached input tokens with Priority |
| Gemini 3.1 Pro Preview | Input (text, image, video, audio) | Global | $3.60 | $7.20 | $0.36 | $0.72 |
|  | Text output (response and reasoning) | Global | $21.60 | $32.40 | N/A | N/A |
| Gemini 3.7 Flash \*<br>through December 31, 2026 | Input (text, image, video, audio) | Global | $1.35 | $1.35 | $0.135 | $0.135 |
|  |  | Non-global | $1.485 | $1.485 | $0.1485 | $0.1485 |
|  | Text output (response and reasoning) | Global | $6.75 | $6.75 | N/A | N/A |
|  |  | Non-global | $7.425 | $7.425 | N/A | N/A |
| Gemini 3.7 Flash<br>starting January 1, 2027 | Input (text, image, video, audio) | Global | $2.70 | $2.70 | $0.27 | $0.27 |
|  |  | Non-global | $2.97 | $2.97 | $0.297 | $0.297 |
|  | Text output (response and reasoning) | Global | $13.50 | $13.50 | N/A | N/A |
|  |  | Non-global | $14.85 | $14.85 | N/A | N/A |
| Gemini 3.6 Flash \*<br>through December 31, 2026 | Input (text, image, video, audio) | Global | $1.35 | $1.35 | $0.135 | $0.135 |
|  |  | Non-global | $1.485 | $1.485 | $0.1485 | $0.1485 |
|  | Text output (response and reasoning) | Global | $6.75 | $6.75 | N/A | N/A |
|  |  | Non-global | $7.425 | $7.425 | N/A | N/A |
| Gemini 3.6 Flash<br>starting January 1, 2027 | Input (text, image, video, audio) | Global | $2.70 | $2.70 | $0.27 | $0.27 |
|  |  | Non-global | $2.97 | $2.97 | $0.297 | $0.297 |
|  | Text output (response and reasoning) | Global | $13.50 | $13.50 | N/A | N/A |
|  |  | Non-global | $14.85 | $14.85 | N/A | N/A |
| Gemini 3 Flash Preview | Input (text, image, video) | Global | $0.90 | $0.90 | $0.09 | $0.09 |
|  | Input (audio) | Global | $1.80 | $1.80 | $0.18 | $0.18 |
|  | Text output (response and reasoning) | Global | $5.40 | $5.40 | N/A | N/A |
| Gemini 3.5 Flash | Input (text, image, video, audio) | Global | $2.70 | $2.70 | $0.27 | $0.27 |
|  |  | Non-global\* | $2.97 | $2.97 | $0.297 | $0.297 |
|  | Text output (response and reasoning) | Global | $16.20 | $16.20 | N/A | N/A |
|  |  | Non-global\* | $17.82 | $17.82 | N/A | N/A |
| Gemini 3.5 Flash-Lite | Input (text, image, video, audio) | Global | $0.54 | $0.54 | $0.054 | $0.054 |
|  |  | Non-global\* | $0.594 | $0.594 | $0.0594 | $0.0594 |
|  | Text output (response and reasoning) | Global | $4.50 | $4.50 | N/A | N/A |
|  |  | Non-global\* | $4.95 | $4.95 | N/A | N/A |
| Gemini 3.1 Flash-Lite | Input (text, image, video) | Global | $0.45 | $0.45 | $0.045 | $0.045 |
|  |  | Non-global\* | $0.495 | $0.495 | $0.0495 | $0.0495 |
|  | Input (audio) | Global | $0.90 | $0.90 | $0.09 | $0.09 |
|  |  | Non-global\* | $0.99 | $0.99 | $0.099 | $0.099 |
|  | Text output (response and reasoning) | Global | $2.70 | $2.70 | N/A | N/A |
|  |  | Non-global\* | $2.97 | $2.97 | N/A | N/A |
| Gemini 3.1 Flash-Lite Image (Nano Banana 2 Lite) | Input (text, image, video) | Global | N/A | N/A | N/A | N/A |
|  | Text output (response and reasoning) | Global | N/A | N/A | N/A | N/A |
|  | Image Output\*\*\*\* | Global | N/A | N/A | N/A | N/A |
| Gemini 3.1 Flash Image (Nano Banana 2) | Input (text, image, video) | Global | N/A | N/A | N/A | N/A |
|  | Text output (response and reasoning) | Global | N/A | N/A | N/A | N/A |
|  | Image Output\*\*\* | Global | N/A | N/A | N/A | N/A |
| Gemini 3 Pro Image (Nano Banana Pro) | Input (text, image, video, audio) | Global | N/A | N/A | N/A | N/A |
|  | Text output (response and reasoning) | Global | N/A | N/A | N/A | N/A |
|  | Image Output\*\* | Global | N/A | N/A | N/A | N/A |

\\* Promotional pricing provided through 50% credits back on net spend on select models within a given period.

| Model | Type | Region | Price (/1M tokens)<br><= 200K input tokens with Flex/Batch | Price (/1M tokens)<br>\> 200K input tokens with Flex/Batch | Price (/1M tokens)<br><= 200K cached input tokens with Flex/Batch | Price (/1M tokens)<br>\> 200K cached input tokens with Flex/Batch |
| Gemini 3.1 Pro Preview | Input (text, image, video, audio) | Global | $1.00 | $2.00 | N/A | N/A |
|  | Text output (response and reasoning) | Global | $6.00 | $9.00 | N/A | N/A |
| Gemini 3.7 Flash \*<br>through December 31, 2026 | Input (text, image, video, audio) | Global | $0.375 | $0.375 | $0.0375 | $0.0375 |
|  |  | Non-global | $0.4125 | $0.4125 | $0.04125 | $0.04125 |
|  | Text output (response and reasoning) | Global | $1.875 | $1.875 | N/A | N/A |
|  |  | Non-global | $2.0625 | $2.0625 | N/A | N/A |
| Gemini 3.7 Flash<br>starting January 1, 2027 | Input (text, image, video, audio) | Global | $0.75 | $0.75 | $0.075 | $0.075 |
|  |  | Non-global | $0.825 | $0.825 | $0.0825 | $0.0825 |
|  | Text output (response and reasoning) | Global | $3.75 | $3.75 | N/A | N/A |
|  |  | Non-global | $4.125 | $4.125 | N/A | N/A |
| Gemini 3.6 Flash \*<br>through December 31, 2026 | Input (text, image, video, audio) | Global | $0.375 | $0.375 | $0.0375 | $0.0375 |
|  |  | Non-global | $0.4125 | $0.4125 | $0.04125 | $0.04125 |
|  | Text output (response and reasoning) | Global | $1.875 | $1.875 | N/A | N/A |
|  |  | Non-global | $2.0625 | $2.0625 | N/A | N/A |
| Gemini 3.6 Flash<br>starting January 1, 2027 | Input (text, image, video, audio) | Global | $0.75 | $0.75 | $0.075 | $0.075 |
|  |  | Non-global | $0.825 | $0.825 | $0.0825 | $0.0825 |
|  | Text output (response and reasoning) | Global | $3.75 | $3.75 | N/A | N/A |
|  |  | Non-global | $4.125 | $4.125 | N/A | N/A |
| Gemini 3 Flash Preview | Input (text, image, video) | Global | $0.25 | $0.25 | N/A | N/A |
|  | Input (audio) | Global | $0.50 | $0.50 | N/A | N/A |
|  | Text output (response and reasoning) | Global | $1.50 | $1.50 | N/A | N/A |
| Gemini 3.5 Flash | Input (text, image, video, audio) | Global (Batch) | $0.75 | $0.75 | $0.075 | $0.075 |
|  |  | Global (Flex) | $0.75 | $0.75 | $0.075 | $0.075 |
|  |  | Non-global\* | $0.825 | $0.825 | $0.0825 | $0.0825 |
|  | Text output (response and reasoning) | Global | $4.50 | $4.50 | N/A | N/A |
|  |  | Non-global\* | $4.95 | $4.95 | N/A | N/A |
| Gemini 3.5 Flash-Lite | Input (text, image, video, audio) | Global | $0.15 | $0.15 | $0.015 | $0.015 |
|  |  | Non-global\* | $0.165 | $0.165 | $0.0165 | $0.0165 |
|  | Text output (response and reasoning) | Global | $1.25 | $1.25 | N/A | N/A |
|  |  | Non-global\* | $1.375 | $1.375 | N/A | N/A |
| Gemini 3.1 Flash-Lite | Input (text, image, video) | Global | $0.125 | $0.125 | $0.0125 | $0.0125 |
|  |  | Non-global\* | $0.1375 | $0.1375 | $0.01375 | $0.01375 |
|  | Input (audio) | Global | $0.25 | $0.25 | $0.025 | $0.025 |
|  |  | Non-global\* | $0.275 | $0.275 | $0.0275 | $0.0275 |
|  | Text output (response and reasoning) | Global | $0.75 | $0.75 | N/A | N/A |
|  |  | Non-global\* | $0.825 | $0.825 | N/A | N/A |
| Gemini 3.1 Flash-Lite Image (Nano Banana 2 Lite) | Input (text, image, video) | Global | $0.125 | N/A | $0.0125 | N/A |
|  | Text output (response and reasoning) | Global | $0.75 | N/A | N/A | N/A |
|  | Image Output\*\*\*\* | Global | $15.00 | N/A | N/A | N/A |
| Gemini 3.1 Flash Image (Nano Banana 2) | Input (text, image, video) | Global | $0.25 | N/A | $0.025 | N/A |
|  | Text output (response and reasoning) | Global | $1.50 | N/A | N/A | N/A |
|  | Image Output\*\*\* | Global | $30.00 | N/A | N/A | N/A |
| Gemini 3 Pro Image (Nano Banana Pro) | Input (text, image) | Global | $1.00 | N/A | $0.10 | N/A |
|  | Text output (response and reasoning) | Global | $6.00 | N/A | N/A | N/A |
|  | Image Output\*\*\* | Global | $60.00 | N/A | N/A | N/A |

\\* Promotional pricing provided through 50% credits back on net spend on select models within a given period.

Pricing with grounding

| Feature | Usage | Price (USD) |
| Grounding with Google Search & Web Grounding for Enterprise | Includes 5,000 Grounding Queries per month at no charge, aggregated across all Gemini 3 models.<br>Grounding Queries exceeding those limits are billed at **$14 per 1,000 Grounding Queries**. Please contact your account team if you require more than 1 million Grounding Prompts per day.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to a Google web index (each a “ **Grounding Query**”) . You will be charged for each individual Grounding Query performed. Billing will start January 5, 2026. <br>Input tokens provided by Grounding with Google Search or Web Grounding for Enterprise are not charged.<br>Customers may decide not to display Search Suggestions with Grounded Results in their Customer Applications at standard pricing for under 1 million Grounding Prompts per day. | 0 count to 5,000 count<br>$0.00 (Free)<br>5,000 count and above<br>$14.00 |
| Grounding with Google Maps | Includes 5,000 search queries per month at no charge, aggregated across all Gemini 3 models.<br>Maps queries exceeding those limits are billed at $14 per 1,000 queries. A customer-submitted request to Gemini may result in one or more queries to Google Maps. You will be charged for each individual query performed. Billing will start January 5, 2026<br>Input tokens provided by Google Maps are not charged. | 0 count to 5,000 count<br>$0.00 (Free)<br>5,000 count and above<br>$14.00 |
| Grounding with your data | $2.50 per 1,000 prompts. | $2.50 |
| Computer Use Tool | Pricing is based on the total number of input tokens sent to the model and resulting output tokens generated. Token prices are based on the [respective model used](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing#googlemodels).<br>Starting with Gemini 3.5, function declarations are included in the input token count.<br>For additional detail, see [documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/computer-use). |  |

\\* For non-global endpoints, pricing will go into effect for the Generally available Gemini 3 and later families of models on July 1, 2026. Before July 1, 2026, Global endpoint pricing applies to Non-global endpoints.

\\* If a query input context is longer than 200K tokens, all tokens (input and output) are charged at long context rates.

\\* Tuned model endpoint will be 1.5 times of the base model.

\\*\\* Gemini 3 Pro Image charges 560 tokens per input image, with output image costs scaling by resolution: 1120 tokens ($0.134) for 1K and 2K (roughly 1MP and 4MP), and 2000 tokens ($0.24) for 4K (roughly 16MP).

\\*\\*\\* Gemini 3.1 Flash Image charges 1120 tokens per input image, with output image costs scaling by resolution: 747 tokens ($0.045) for 512 (roughly 0.25MP), 1120 tokens ($0.067) for 1K (roughly 1MP), 1680 tokens ($0.101) for 2K (roughly 4MP), and 2,520 tokens ($0.15) for 4K (roughly 16MP).

\\*\\*\\*\\* Gemini 3.1 Flash-Lite Image charges 1120 tokens per input image, and 1120 tokens ($0.034) for 1K (roughly 1MP) output images

## Gemini 2.5

StandardPriorityFlex/Batch

| Model | Type | Token Price <= 200K tokens | Price > 200K tokens | Price <= 200K cached input tokens | Price > 200K cached input tokens |
| Gemini 2.5 Pro | Input (text, image, video, audio) | $1.25 | $2.50 | $0.125 | $0.25 |
|  | Text output (response and reasoning) | $10.00 | $15.00 | N/A | N/A |
| Gemini 2.5 Pro<br>Computer Use-Preview | Input (text, image, video, audio) | $1.25 | $2.50 | N/A | N/A |
|  | Text output (response and reasoning) | $10.00 | $15.00 | N/A | N/A |
| Gemini 2.5 Flash | Input (text, image, video) | $0.30 | $0.30 | $0.03 | $0.03 |
|  | Audio Input | $1.00 | $0.30 | $0.10 | $0.10 |
|  | Text output (response and reasoning) | $2.50 | $2.50 | N/A | N/A |
| Gemini 2.5 Flash Image | Input (text, image)\*\*\* | - | N/A | N/A | N/A |
|  | Text output (response and reasoning) | $2.50 | N/A | N/A | N/A |
|  | Image output\*\*\* | - | N/A | N/A | N/A |
| Gemini 2.5 Flash Live API | Input text | $0.50 | $0.50 | N/A | N/A |
|  | Input (video, image) | $3.00 | $3.00 | N/A | N/A |
|  | Audio Input | $3.00 | $3.00 | N/A | N/A |
|  | Text output | $2.00 | $2.00 | N/A | N/A |
|  | 1M output audio tokens | $12.00 | $12.00 | N/A | N/A |
| Gemini 2.5 Flash Lite | Input (text, image, video) | $0.10 | $0.10 | $0.01 | $0.01 |
|  | Audio Input | $0.30 | $0.30 | $0.03 | $0.03 |
|  | Text output (response and reasoning) | $0.40 | $0.40 | N/A | N/A |

| Model | Type | Price (/1M tokens) <= 200K input tokens with Priority | Price (/1M tokens) > 200K input tokens with Priority | Price (/1M tokens) <= 200K cached input tokens with Priority | Price (/1M tokens) > 200K cached input tokens with Priority |
| Gemini 2.5 Pro | Input (text, image, video, audio) | $2.25 | $4.50 | $0.225 | $0.45 |
|  | Text output (response and reasoning) | $18.00 | $27.00 | N/A | N/A |
| Gemini 2.5 Pro<br>Computer Use-Preview | Input (text, image, video, audio) | N/A | N/A | N/A | N/A |
|  | Text output (response and reasoning) | N/A | N/A | N/A | N/A |
| Gemini 2.5 Flash | Input (text, image, video) | $0.54 | $0.54 | $0.054 | $0.054 |
|  | Audio Input | $1.80 | $1.80 | $0.18 | $0.18 |
|  | Text output (response and reasoning) | $4.50 | $4.50 | N/A | N/A |
| Gemini 2.5 Flash Image | Input (text, image)\*\*\* | N/A | N/A | N/A | N/A |
|  | Text output (response and reasoning) | N/A | N/A | N/A | N/A |
|  | Image output\*\*\* | N/A | N/A | N/A | N/A |
| Gemini 2.5 Flash Live API | 1M input text tokens | N/A | N/A | N/A | N/A |
|  | 1M input audio tokens | N/A | N/A | N/A | N/A |
|  | 1M input video/image tokens | N/A | N/A | N/A | N/A |
|  | 1M output text tokens | N/A | N/A | N/A | N/A |
|  | 1M output audio tokens | N/A | N/A | N/A | N/A |
| Gemini 2.5 Flash Lite | Input (text, image, video) | $0.18 | $0.18 | $0.018 | $0.018 |
|  | Audio Input | $0.54 | $0.54 | $0.054 | $0.054 |
|  | Text output (response and reasoning) | $0.72 | $0.72 | N/A | N/A |

| Model | Type | Price (/1M tokens) <= 200K input tokens with Flex/Batch | Price (/1M tokens) > 200K input tokens with Flex/Batch |
| Gemini 2.5 Pro | Input (text, image, video, audio) | $0.625 | $1.25 |
|  | Text output (response and reasoning) | $5.00 | $7.50 |
| Gemini 2.5 Pro<br>Computer Use-Preview | Input (text, image, video, audio) | N/A | N/A |
|  | Text output (response and reasoning) | N/A | N/A |
| Gemini 2.5 Flash | Input (text, image, video) | $0.15 | $0.15 |
|  | Audio Input | $0.50 | $0.50 |
|  | Text output (response and reasoning) | $1.25 | $1.25 |
| Gemini 2.5 Flash Image | Input (text, image, video)\*\*\* | $0.15 | N/A |
|  | Text output (response and reasoning) | $1.25 | N/A |
|  | Image output\*\*\* | $15.00 | N/A |
| Gemini 2.5 Flash Live API | 1M input text tokens | N/A | N/A |
|  | 1M input audio tokens | N/A | N/A |
|  | 1M input video/image tokens | N/A | N/A |
|  | 1M output text tokens | N/A | N/A |
|  | 1M output audio tokens | N/A | N/A |
| Gemini 2.5 Flash Lite | Input (text, image, video) | $0.05 | $0.05 |
|  | Audio Input | $0.05 | $0.05 |
|  | Text output (response and reasoning) | $0.20 | $0.20 |

Pricing with grounding

| Feature | Usage | Price (USD) |
| Grounding with Google Search | Gemini 2.0 Flash, 2.5 Flash and 2.5 Flash-Lite include a combined 1,500 Grounding Prompts per day at no additional charge. Gemini 2.5 Pro includes 10,000 Grounding Prompts per day at no additional charge.<br>Grounding Prompts exceeding those limits are billed at **$35 per 1,000 Grounding Prompts**. Please contact your account team if you require more than 1 million Grounding Prompts per day.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to a Google web  index (each a “ **Grounding Query**”)\*\*. Even if multiple Grounding Queries are sent, there is only one charge for a Grounding Prompt. | 0 count to 10,000 count<br>$0.00 (Free)<br>10,000 count and above<br>$35.00 |
| Web Grounding for enterprise | **$45 per 1,000 Grounding Prompts.** Please contact your account team if you require more than 1 million Grounding Prompts per day.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to a Google web index (each a “ **Grounding Query**”)\*\*. Even if multiple Grounding Queries are sent, there is only one charge for a Grounding Prompt. | $45.00 |
| Grounding with your data | $2.5 per 1,000 requests. | $2.50 |
| Grounding with Google Maps | **$25 per 1,000 grounded prompts.**<br>One grounded prompt is a request sent to Gemini that makes at least 1 query to Google Maps. | 0 count to 1,500 count<br>$0.00 (Free)<br>1,500 count and above<br>$25.00 |

\\* If a query input context is longer than 200K tokens, all tokens (input and output) are charged at long context rates.

\\* Tuned model endpoint has the same prediction price as the base model.

\\*\\* Grounding with Google Search and Web Grounding for Enterprise are billed only when a Grounding Prompt successfully returns sources (i.e., results containing at least one support URL from the web). Gemini model usage fees apply separately.

\\*\\*\\* A 1024x1024 image consumes 1290 tokens ($0.039 per 1K output image). Per image token count varies by image resolution. For more information on how to calculate tokens, you can refer to our [documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-understanding#image-requirements).

\\*\\*\\*\\* Computer Use billing uses the Gemini 2.5 Pro SKU, to split out Computer Use costs, apply billing tags. See more [here](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/add-labels-to-api-calls).

- **LiveAPI Session's Context Window billing explained**: You are charged per turn for all tokens present in the Session Context Window. The Session Context Window includes new tokens (current turn) + all accumulated tokens from previous turns. This means tokens from past turns are re-processed and accounted for in each new turn, up to your configured context window size. A "turn" is one user input and the model's response.
- **Proactive Audio Mode**: When enabled, input tokens are charged while LiveAPI is listening. Output tokens are only charged when the API responds.
- When audio to text transcription is enabled, all text tokens generated for transcription are charged at the text token output rate.

## Gemini 2.0

Gemini 2.0 is billed based on tokens. To calculate the number of input tokens in your request prior to sending the request, you can use the [SDK tokenizer](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/list-token) or the [countTokens API](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/get-token-count). If your request fails with a 400 or 500 error, you won't be charged for the tokens used.

Use the toggle in the pricing table to compare token-based pricing and modality-based pricing.

Token-based pricingModality-based pricing

| Model | Type | Price /1M tokens (USD) | Price /1M tokens (USD) with Batch API |
| Gemini 2.0 Flash | Input text | $0.15 | $0.075 |
|  | Input audio | $1.00 | $0.50 |
|  | Output text | $0.60 | $0.30 |
|  | Tuning training | $0.003 |  |
| Gemini 2.0 Flash Image Generation | Input tokens | $0.15 |  |
|  | Input audio tokens | $1.00 |  |
|  | Input video tokens | $0.15 |  |
|  | Output text tokens | $0.60 |  |
|  | Output image tokens | $30.00 |  |
| Gemini 2.0 Flash Live API | Input text tokens | $0.50 |  |
|  | Input audio tokens | $3.00 |  |
|  | Input video/image tokens | $3.00 |  |
|  | Output text tokens | $2.00 |  |
|  | Output audio tokens | $12.00 |  |
| Gemini 2.0 Flash Lite | Input tokens | $0.075 | $0.0375 |
|  | Input audio tokens | $0.075 | $0.0375 |
|  | Output text tokens | $0.30 | $0.15 |
|  | Tuning for training tokens | $0.001 |  |

\\* Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\\* Training tokens are calculated by the total number of tokens in your training dataset, multiplied by your number of epochs.

\\* PDFs are billed as image input, with one PDF page equivalent to one image.

\\* Tuned model endpoint has the same prediction price as the base model.

\\* Gemini 2.0 Flash Live API: 25 tokens per second of audio (input/output), 258 tokens per second of video (input). Grounding with Google Search remains free of charge while Gemini 2.0 Flash Live API is in Preview.

The below modality pricing is based on average use cases for reference only. Actual billing will only be based on tokens:

- 4 characters result in approximately 1 text token including white space.
- For an 1024x1024 image, it consumes 1290 tokens. Per image token count varies by image resolution. For more information on how to calculate tokens, you can refer to our [documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-understanding#image-requirements).
- Video input consumes 258 tokens per second at the sample rate of one frame per second. Video with audio bills for both video tokens and audio tokens.
- Audio input consumes 25 tokens per second without timestamp.

| Model | Type | Price (/1M tokens) (USD) | Price (/1M tokens) (USD) with Batch API |
| Gemini 2.0 Flash | Input text ($/M char) | $0.0375 | $0.01875 |
|  | Input image ($/image) | $0.0001935 | $0.00009675 |
|  | Input video ($/sec) | $0.0000387 | $0.00001935 |
|  | Input audio ($/sec) | $0.000025 | $0.0000125 |
|  | Output text ($/M char) | $0.15 | $0.075 |
| Gemini 2.0 Flash Image Generation | Input text ($/M char) | $0.0375 |  |
|  | Input image ($/image) | $0.0001935 |  |
|  | Input video ($/sec) | $0.0000387 |  |
|  | Input audio ($/sec) | $0.000025 |  |
|  | Output text ($/M char) | $0.15 |  |
|  | Output image image ($/image) | $0.04 |  |
| Gemini 2.0 Flash Lite | Input text ($/M char) | $0.01875 | $0.009375 |
|  | Input image ($/image) | $0.00009675 | $0.000048375 |
|  | Input video ($/sec) | $0.00001935 | $0.000009675 |
|  | Input audio ($/sec) | $0.000001875 | $0.000000938 |
|  | Output text ($/M char) | $0.075 | $0.0375 |

\\* Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\\* Training tokens are calculated by the total number of tokens in your training dataset, multiplied by your number of epochs.

\\* PDFs are billed as image input, with one PDF page equivalent to one image.

\\* Tuned model endpoint has the same prediction price as the base model.

\\* Gemini 2.0 Flash Live API: 25 tokens per second of audio (input/output), 258 tokens per second of video (input). Grounding with Google Search remains free of charge while Gemini 2.0 Flash Live API is in Preview.

Price with Grounding

| Feature | Usage | Price (USD) |
| Grounding with Google Search\*, \*\* | Gemini 2.0 Flash, 2.5 Flash and 2.5 Flash-Lite include a combined 1,500 Grounding Prompts per day at no additional charge. Gemini 2.5 Pro includes 10,000 Grounding Prompts per day at no additional charge.<br>Grounding Prompts exceeding those limits are billed at **$35 per 1,000 Grounding Prompts**. Please contact your account team if you require more than 1 million Grounding Prompts per day.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to a Google web  index (each a “ **Grounding Query**”)\*\*. Even if multiple Grounding Queries are sent, there is only one charge for a Grounding Prompt. | 0 count to 10,000 count<br>$0.00 (Free)<br>10,000 count and above<br>$35.00 |
| Web Grounding for enterprise\*, \*\* | **$45 per 1,000 Grounding Prompts.** Please contact your account team if you require more than 1 million Grounding Prompts per day.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to a Google web index (each a “ **Grounding Query**”)\*\*. Even if multiple Grounding Queries are sent, there is only one charge for a Grounding Prompt. | $45.00 |
| Grounding with your data\* | $2.5 per 1,000 requests. | $2.50 |
| Grounding with Google Maps\* | Gemini models include a number of daily grounded prompts at no extra cost:<br>- **Gemini Flash and Flash-Lite**: combined 1,500 grounded prompts per day.<br>- **Gemini Pro**: 10,000 grounded prompts per day.<br>Grounded prompts exceeding those limits are billed at $25 per 1,000 grounded prompts.<br>One grounded prompt is a request sent to Gemini that makes at least 1 query to Google Maps.<br>Please contact your account team if you require more than 1 million grounded prompts per day. | 0 count to 1,500 count<br>$0.00 (Free)<br>1,500 count and above<br>$25.00 |

\\* Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\\* Training tokens are calculated by the total number of tokens in your training dataset, multiplied by your number of epochs.

\\* PDFs are billed as image input, with one PDF page equivalent to one image.

\\* Tuned model endpoint has the same prediction price as the base model.

\\* Gemini 2.0 Flash Live API: 25 tokens per second of audio (input/output), 258 tokens per second of video (input). Grounding with Google Search remains free of charge while Gemini 2.0 Flash Live API is in Preview.

\\*\\* Grounding with Google Search and Web Grounding for Enterprise is billed only when a prompt successfully returns sources (i.e., results containing at least one support URL from the web). Gemini model usage fees apply separately.

- **LiveAPI Session's Context Window billing explained**: You are charged per turn for all tokens present in the Session Context Window. The Session Context Window includes new tokens (current turn) + all accumulated tokens from previous turns. This means tokens from past turns are re-processed and accounted for in each new turn, up to your configured context window size. A "turn" is one user input and the model's response.
- When audio to text transcription is enabled, all text tokens generated for transcription are charged at the text token output rate.

## Other Gemini models

All Gemini models other than Gemini 2.0 or Gemini 2.5 are billed based on modalities such as characters, images, video/audio seconds.

- Text input is charged by every 1,000 characters of input (prompt) and every 1,000 characters of output (response).
- Characters are counted by UTF-8 code points and white space is excluded from the count, resulting in approximately 4 characters per token.
- Prediction requests that lead to filtered responses are charged for the input only.
- At the end of each billing cycle, fractions of one cent ($0.01) are rounded to one cent. Media input is charged per image or per second (video).
- If your request fails with a 400 or 500 error, you won't be charged for the tokens used.

### Gemini 3.5 Transcribe

| Model | Feature | Description | Input Type & Price | Output Type & Price | Effective Blended Price |
| Gemini 3.5 Transcribe Live | Real-time streaming transcription | Sub-second latency streaming via Live API with automatic code-mixing. Only final committed tokens are billed. | **Audio Input**<br>$3.50 / 1M tokens | **Text Output**<br>$21.00 / 1M tokens | ~$0.009/audio-minute\* |
| Gemini 3.5 Transcribe | Synchronous audio file processing | Batch and synchronous processing for files up to 60 minutes via GenerateContent API. | **Audio Input**<br>$2.50 / 1M tokens | **Text Output**<br>$12.00 / 1M tokens | ~$0.005/audio-minute\* |

\*Estimated pricing is based on 25 audio tokens per second for audio input and 175 text tokens per minute of text output.

### Gemini 1.5

| Model | Feature | Type | Price ( =< 128K input tokens) | Price ( > 128K input tokens) |
| Gemini 1.5 Flash | Multimodal | Image Input | $0.00002 / 1 count | $0.00004 / 1 count |
|  |  | Video Input | $0.00002 / 1 count | $0.00004 / 1 count |
|  |  | Text Input | $0.00001875 / 1,000 count | $0.0000375 / 1,000 count |
|  |  | Audio Input | $0.000002 / 1 count | $0.000004 / 1 count |
|  |  | Text Output | $0.000075 / 1,000 count | $0.00015 / 1,000 count |
|  | Tuning\* | Training Token | $0.008 / 1,000 count |  |
| Gemini 1.5 Pro | Multimodal | Image Input | $0.00032875 / 1 count | $0.0006575 / 1 count |
|  |  | Video Input | $0.00032875 / 1 count | $0.0006575 / 1 count |
|  |  | Text Input | $0.0003125 / 1,000 count | $0.000625 / 1,000 count |
|  |  | Audio Input | $0.00003125 / 1 count | $0.0000625 / 1 count |
|  |  | Text Output | $0.00125 / 1,000 count | $0.0025 / 1,000 count |
|  | Tuning\* | Training Token | $0.08 / 1,000 count |  |
| Gemini 1.0 Pro | Multimodal | Image Input | $0.0025 / 1 count |
|  |  | Video Input | $0.002 / 1 count |  |
|  |  | Text Input | $0.000125 / 1,000 count |
|  |  | Text Output | $0.000375 / 1,000 count |  |

\\* Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\\* If a query context is longer than 128K, all tokens are charged at long context rates.

\\* Gemini models are available in batch mode at 50% discount.

\\* Gemini 1.0 Pro only support up to 32K context window.

\\* PDFs are billed as image input, with one PDF page equivalent to one image.

\\* Tuned model endpoint has the same prediction price as the base model.

\\*\\* Grounding with Google Search and Web Grounding for Enterprise is billed only when a prompt successfully returns sources (i.e., web results containing at least one support URL from the web). Gemini model usage fees apply separately.

Pricing with Grounding

| Feature | Price (USD) |
| Grounding with Google Search | **$35 per 1,000 Grounding Prompts**.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to Google web index (each a “ **Grounding Query**”)\*\*. Even if multiple Grounding Queries are sent, there is only one charge for a Grounding Prompt. |
| Web Grounding for enterprise | **$45 per 1,000 Grounding Prompts**.<br>A “ **Grounding Prompt**” is an End User prompt that Customer submits to Gemini for which Gemini makes one or more queries to Google web index (each a “ **Grounding Query**”)\*\*. Even if multiple Grounding Queries are sent, there is only one charge for a Grounding Prompt. |
| Grounding with your data | $2.5 per 1,000 requests starting June 16, 2025. |

\\*\\* Grounding with Google Search and Web Grounding for Enterprise is billed only when a prompt successfully returns sources (i.e., web results containing at least one support URL from the web). Gemini model usage fees apply separately.

### Imagen

With Imagen on Agent Platform, you can generate novel images and edit images based on text prompts you provide, or edit only parts of images using a mask area you define along with a host of other capabilities.

| Model | Feature | Description | Input | Output | Price / 1 count (USD) |
| Imagen 4 Ultra | Image generation | Generate an image | Text prompt | Image | $0.06 |
| Imagen 4 | Upscaling | Increase resolution of a generated image to 2K, 3K, and 4K | Image | Image | $0.06 |
| Imagen 4 | Image generation | Generate an image | Text prompt | Image | $0.04 |
| Imagen 4 Fast | Image generation | Generate an image | Text prompt | Image | $0.02 |
| Imagen 3 | Image generation | Generate an image<br>Edit an image<br>Customize an image | Text prompt | Image | $0.04 |
| Imagen 3 Fast | Image generation | Generate an image | Text prompt | Image | $0.02 |
| Imagen 2, Imagen 1 | Image generation | Generate an image | Text prompt | Image | $0.02 |
| Imagen 2, Imagen 1 | Image editing | Edit an image using mask free or mask approach | Image/Text prompt | Image | $0.02 |
| Imagen 1 | Upscaling | Increase resolution of a generated image to 2k and 4k | Image | Image | $0.003 |
| Imagen 1 | Fine-tuning | Enable a "subject" provided by the user to used in Imagen prompts (few shot training) | Subject(s) with text identifier and 4-8 images per subject | Fine-tuned model (after training with user provided subjects) | $ per node hour (Agent Platform custom training pricing) |
| Imagen | Visual Captioning | Generate a short or long text caption for an image | Image | Text caption | $0.0015 |
| Imagen | Visual Q&A | Provide an answer based on a question referencing an image | Image/Text prompt | Text answer | $0.0015 |
| Imagen | Product Recontext | Re-imagine products in a new scene | 1-3 Images of the same product and a text prompt describing desired scene | Image | $0.12 |
|  | Virtual Try-On | Create images of people wearing different clothes | 1 image of a person and 1 image of clothing | Image | $0.06 |

Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

### Veo

| Model | Feature | Description | Input | Output | Output Resolution | Price (USD) |
| Veo 3.1 | Video + Audio generation | Generate high-quality videos with synchronized speech/sound effects from a text prompt or reference image | Text/Image prompt | Video + Audio | 720p, 1080p | $0.40 / 1 count |
|  |  |  |  |  | 4k | $0.60 / 1 count |
|  | Video generation | Generate high-quality videos from a text prompt or reference image | Text/Image prompt | Video | 720p, 1080p | $0.20 / 1 count |
|  |  |  |  |  | 4k | $0.40 / 1 count |
| Veo 3.1 Fast | Video + Audio generation | Generate videos with synchronized speech/sound effects from a text prompt or reference image faster | Text/Image prompt | Video + Audio | 720p | $0.10 / 1 count |
|  |  |  |  |  | 1080p | $0.12 / 1 count |
|  |  |  |  |  | 4k | $0.30 / 1 count |
|  | Video generation | Generate videos from a text prompt or reference image faster | Text/Image prompt | Video | 720p | $0.08 / 1 count |
|  |  |  |  |  | 1080p | $0.10 / 1 count |
|  |  |  |  |  | 4k | $0.25 / 1 count |
| Veo 3.1 Lite | Video + Audio generation | Generate videos with synchronized speech/sound effects from a text prompt or reference image the fastest | Text/Image prompt | Video + Audio | 720p | $0.05 / 1 count |
|  |  |  |  |  | 1080p | $0.08 / 1 count |
|  | Video generation | Generate videos from a text prompt or reference image the fastest | Text/Image prompt | Video | 720p | $0.03 / 1 count |
|  |  |  |  |  | 1080p | $0.05 / 1 count |
| Veo 3 | Video + Audio generation | Generate high-quality videos with synchronized speech/sound effects from a text prompt or reference image | Text/Image prompt | Video + Audio | 720p, 1080p | $0.40 / 1 count |
|  | Video generation | Generate high-quality videos from a text prompt or reference image | Text/Image prompt | Video | 720p, 1080p | $0.20 / 1 count |
| Veo 3 Fast | Video + Audio generation | Generate videos with synchronized speech/sound effects from a text prompt or reference image faster | Text/Image prompt | Video + Audio | 720p | $0.10 / 1 count |
|  |  |  |  |  | 1080p | $0.12 / 1 count |
|  | Video generation | Generate videos from a text prompt or reference image faster | Text/Image prompt | Video | 720p | $0.08 / 1 count |
|  |  |  |  |  | 1080p | $0.10 / 1 count |
| Veo 2 | Video generation | Generate videos from a text prompt or reference image | Text/Image prompt | Video | 720p | $0.50 / 1 count |
|  | Advanced Controls | Generate videos through start and end frame interpolation, extend generated videos, and apply camera controls | Text/Image/Video prompt | Video | 720p | $0.50 / 1 count |

### Lyria

Lyria model family offers high-quality music generation that is ideal for sophisticated composition and detailed creative exploration where nuanced output is key.

| Model | Feature | Description | Input | Output | Price (USD) |
| Lyria 3 Pro | Full song music generation | Lyria 3 Pro creates full-length musical compositions from multimodal inputs such as text or images | Text, Image | Full song | $0.08 / 1 count |
| Lyria 3 | 30 second music clip generation | Lyria 3 generates high-fidelity, 30-second audio clips from text or image prompts | Text, Image | 30 second music clip | $0.04 / 1 count |
| Lyria 2 | Music generation | Generate music from a text prompt | Text prompt | Music | $0.06 / 1 count |

### Embedding costs

The Gemini API offers embedding models to generate embeddings for text, images, video, and other content.

| Model | Type | Region | Request Type | Price / 1,000 count (USD) |
| Gemini Embedding | Input | Global | Online requests | $0.00015 |
|  |  |  | Batch requests | $0.00012 |
|  | Output | Global | Online requests | No charge |
|  |  |  | Batch requests | No charge |
| Embeddings for Text (Excluding Gemini Embedding) | Input | Global | Online requests | $0.000025 |
|  |  |  | Batch requests | $0.00002 |
|  | Output | Global | Online requests | No charge |
|  |  |  | Batch requests | No charge |

### Gemini Omni

| Model | Type | Token Price /1M (USD) |
| Gemini Omni Flash, Gemini Omni 1.1 Flash | Input (text, image, video, audio)\* | $1.50 |
|  | Text output (response and reasoning) | $9.00 |
|  | Video Output\*\* | $17.50 |

\\* Gemini Omni Flash charges 1120 tokens per image, 32 tokens per audio second, and 5792 tokens per video second for inputs.

\\*\\* Gemini Omni Flash charges 1931 tokens per second of 360p video, 5792 tokens per second of 720p video, 8688 tokens per second of 1080p video, and 17376 tokens per second of 4k video for video outputs (with audio).

## Agents

| Model | Type | Price (/1M tokens) | Price (/M chached input tokens) |
| Gemini Deep Research Agent | Input (text) | $2 | $0.2 |
|  | Text output (response and reasoning) | $12 | N/A |

**Pricing with grounding**

| Feature | Usage | Price (USD) |
| Grounding with Google Web Search and Image Search, & Web Grounding for Enterprise\* | Includes 5,000 search queries per month at no charge, aggregated across all Gemini 3 models.<br>Search queries exceeding those limits are billed at $14 per 1,000 search queries. A customer-submitted request to Gemini may result in one or more queries to Google Search (or Web Grounding for Enterprise). You will be charged for each individual search query performed. Billing will start January 5, 2026.<br>Input tokens provided by Grounding with Google Search or Web Grounding for Enterprise are not charged.<br>Please contact your account team if you require more than 1 million grounded prompts per day.<br>Customers may decide not to display Search Suggestions with Grounded Results in their Customer Application interface at standard pricing. | 0 count to 5,000 count<br>$0.00 (Free)<br>5,000 count and above<br>$14.00 |
|  |  | $2.50 |

## CodeMender

The pricing for CodeMender is based on tokens and is determined by the model used.

| Model | Type | Model Price /1M tokens (USD) | CodeMender Price /1M tokens (USD) |
| Gemini 3.7 Flash | Input tokens | $1.50 | $1.50 |
|  | Cached tokens | $0.15 | $0.15 |
|  | Output tokens | $7.50 | $7.50 |
| Gemini 3.6 Flash | Input tokens | $1.50 | $1.50 |
|  | Cached tokens | $0.15 | $0.15 |
|  | Output tokens | $7.50 | $7.50 |
| Gemini 3.5 Flash | Input tokens | $1.50 | $1.50 |
|  | Cached tokens | $0.15 | $0.15 |
|  | Output tokens | $9.00 | $9.00 |
| Gemini 3.1 Pro | Input tokens | $2.00 | $2.00 |
|  | Cached tokens | $0.20 | $0.20 |
|  | Output tokens | $12.00 | $12.00 |

### Gemma

| Model | Type | Price (/1M tokens (USD) |
| Gemma 4 26B | Input | $0.15 |
|  | Output | $0.60 |
|  | Cache Hit | $0.015 |

### MultiModal Embeddings

| Model | Type | Description | Request Type | Price /1M tokens (USD) |
| Gemini Embedding 2 (Unified Multimodal, Preview) | Input text | Generate embeddings using text as input | Online requests | $0.20 |
|  |  |  | Batch requests | $0.10 |
|  | Input image | Generate embeddings using image as input | Online requests | $0.45 |
|  |  |  | Batch requests | $0.225 |
|  | Input video | Generate embeddings using video as input | Online requests | $12.00 |
|  |  |  | Batch requests | $6.00 |
|  | Input audio | Generate embeddings using audio as input | Online requests | $6.50 |
|  |  |  | Batch requests | $3.25 |

\*No charges for output tokens.

| Model | Feature | Description | Input | Output | Price (USD) |
| multimodalembedding | Embeddings for Multimodal: Text | Generate embeddings using text as an input | Text | Embeddings | $0.0002 / 1,000 count |
|  | Embeddings for Multimodal: Image | Generate embeddings using image as an input | Image | Embeddings | $0.0001 / 1 count |
|  | Embeddings for Multimodal: Video Plus | Video Plus | Video | Embeddings (up to 15 embeddings per min of video) | $0.002 / 1 count |
|  | Embeddings for Multimodal: Video Standard | Video Standard | Video | Embeddings (up to 8 embeddings per min of video) | $0.001 / 1 count |
|  | Embeddings for Multimodal: Video Essential | Video Essential | Video | Embeddings (up to 4 embeddings per min of video) | $0.0005 / 1 count |

| Open Source Model | Type | Request Type | Price /1M tokens (USD) |
| multilingual-e5-small | Input | Online requests | $0.015 |
|  | Output | Online requests | No charge |
|  | Batch Input | Batch requests | $0.0075 |
|  | Batch Output | Batch requests | No charge |
| multilingual-e5-large | Input | Online requests | $0.025 |
|  | Output | Online requests | No charge |
|  | Batch Input | Batch requests | $0.0125 |
|  | Batch Output | Batch requests | No charge |

Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

# Pricing for Agent Platform's code completion

Generative AI on Agent Platform charges by every 1,000 characters of input (prompt) and every 1,000 characters of output (response). Characters are counted by UTF-8 code points and white space is excluded from the count. During the Preview stage, charges are 100% discounted. Prediction requests that lead to filtered responses are charged for the input only. At the end of each billing cycle, fractions of one cent ($0.01) are rounded to one cent.

**Note:** Prediction pricing for tuned model endpoints are the same as for the base foundation model.

| Model | Type | Region | Request Type | Price /1k tokens (USD) |
| Codey for Code Completion | Input | Global | Online requests | $0.00025 |
|  | Output | Global | Online requests | $0.0005 |

Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

### Translation (Text)

Use the Agent Platform API and Translation LLM to translate text. LLM translations tend to be more fluent and human sounding than classic translation models, but have more limited language support [(Learn More)](https://cloud.google.com/vertex-ai/generative-ai/docs/translate/translate-text).

| Model | Method | Usage | Price Price /1M token (USD) |
| LLM | [Text translation](https://cloud.google.com/vertex-ai/generative-ai/docs/translate/translate-text)\* | The number of input characters per month | $10.00 |
|  |  | The number of output characters per month | $10.00 |
| Translation LLM 002 | [Text translation](https://cloud.google.com/vertex-ai/generative-ai/docs/models/translation-use-supervised-tuning)\* | The number of input characters per month | $20.00 |
|  |  | The number of output characters per month | $20.00 |

Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\*Price is per character processed by the model. For details about counted characters, see [Charged characters](https://cloud.google.com/translate/pricing#charged-characters)

### Context Cache Storage price for Explicit Caching

This table contains the pricing for Context Cache Storage based on Input (text, image, video, audio)

HourlyHourly

MonthlyMonthly

| Model | Price Tok/hr<= 200K input tokens | Price Tok/hr > 200K input tokens |
| Gemini 3.1 Pro | $0.0000045 | $0.0000045 |
| Gemini 3.6 Flash, Gemini 3.5 Flash, Gemini 3 Flash | $0.000001 | $0.000001 |
| Gemini 3.5 Flash Lite, Gemini 3.1 Flash Lite | $0.000001 | $0.000001 |
| Gemini 3 Pro | $0.0000045 | $0.0000045 |
| Gemini 2.5 Pro | $0.0000045 | $0.0000045 |
| Gemini 2.5 Flash | $0.000001 | $0.000001 |
| Gemini 2.5 Flash Lite | $0.000001 / 1 hour | $0.000001 |

Gemini 2.0 Models

Token-based pricingModality-based pricing

HourlyHourly

MonthlyMonthly

| Model | Type | Storage (M tok-hour) | Price /1 (USD) |
| Gemini 2.0 Flash | Input tokens | $0.000001 | $0.0375 |
|  | Input audio tokens | $0.000001 | $0.25 |
|  | Output text tokens | NA | NA |
| Gemini 2.0 Flash Lite | Input tokens | $0.000001 | $0.01875 |
|  | Input audio tokens | $0.000001 | $0.01875 |
|  | Output text tokens | NA | NA |

\\* Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\\* PDFs are billed as image input, with one PDF page equivalent to one image.

\\* Tuned model endpoint has the same prediction price as the base model.

The below modality pricing is based on average use cases for reference only. Actual billing will only be based on tokens:

- 4 characters result in approximately 1 text token including white space.
- For an 1024x1024 image, it consumes 1290 tokens. Per image token count varies by image resolution. For more information on how to calculate tokens, you can refer to our [documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-understanding#image-requirements).
- Video input consumes 258 tokens per second at the sample rate of one frame per second. Video with audio bills for both video tokens and audio tokens.
- Audio input consumes 25 tokens per second without timestamp.

| Model | Type | Storage (Modality-hour) | Price (USD) |
| Gemini 2.0 Flash | Input text ($/M char) | $0.25 | $0.009375 |
|  | Input image ($/image) | $0.00129 | $0.000048375 |
|  | Input video ($/sec) | $0.000258 | $0.000009675 |
|  | Input audio ($/sec) | $0.000025 | $0.00000625 |
|  | Output text ($/M char) | NA | NA |
| Gemini 2.0 Flash Lite | Input text ($/M char) | $0.25 | $0.0046875 |
|  | Input image ($/image) | $0.00129 |  |
|  | Input video ($/sec) | $0.000258 | $0.000009675 |
|  | Input audio ($/sec) | $0.000258 | $0.0000048375 |
|  | Output text ($/M char) | NA | NA |

\\* Prices are listed in US Dollars (USD). If you pay in a currency other than USD, the prices listed in your currency on [Cloud Platform SKUs](https://cloud.google.com/skus/) apply.

\\* PDFs are billed as image input, with one PDF page equivalent to one image.

\\* Tuned model endpoint has the same prediction price as the base model.

Pricing with grounding

| Feature | Price (USD) |
| Grounding with Google Search\* | Gemini 2.0 Flash includes up to 1,500 grounded requests per day at no additional charge. Grounded requests exceeding 1,500 per day are billed at $35 per 1,000 requests (up to 1 million requests per day).<br>Please contact your account team if you require more than 1 million requests per day.<br>Customers may decide not to display Search Suggestions with Grounded Results in their Customer Application interface; however, this is subject to alternate pricing. Please contact your Google Cloud Account team to request this waiver. |
| Web Grounding for enterprise\* | $45 per 1,000 request (up to 1 million requests per day) starting May 5, 2025.<br>Please contact your account team if you require more than 1 million requests per day.<br>Customers may decide not to display Search Suggestions with Grounded Results in their Customer Application interface; however, this is subject to alternate pricing. Please contact your Google Cloud Account team to request this waiver. |

\\* This apply to modality-based pricing.

**Note:** Grounding with Google Search is billed only for requests that return results containing at least one grounding support URL from the web. Standard Gemini model usage fees also apply.

## Provisioned Throughput

[Provisioned throughput](https://cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput) assures throughput for your generative AI needs and is transacted via [generative AI scale units](https://cloud.google.com/vertex-ai/generative-ai/docs/measure-provisioned-throughput#gsu-burndown-rate), or GSUs. Learn more about how much throughput each GSU provides [here](https://cloud.google.com/vertex-ai/generative-ai/docs/supported-models) and use our online estimator [here](https://console.cloud.google.com/vertex-ai/provisioned-throughput/price-estimate;publisherModelName=;queriesPerSecond=;inputCharsPerQuery=;inputImagesPerQuery=;inputVideoSecondsPerQuery=;inputAudioSecondsPerQuery=;outputCharsPerQuery=;outputImagesPerQuery=0;tierDistribution=100,0?project=cloud-ai-frontend&e=13802955&inv=1&invt=Abo4mg&mods=allow_workbench_image_override).

HourlyHourly

MonthlyMonthly

| Duration | Global price per GSU (USD) | Non-Global\*price per GSU (USD) |
| 1 week commit | $7.14 | $7.854 |
| 1 month commit | $3.698630137 | $4.068493151 |
| 3 month commit | $3.287671233 | $3.616438356 |
| 1 year commit | $2.739726027 | $3.01369863 |

\\* For non-global endpoints, pricing will go into effect for the Generally available Gemini 3 and later families of models on July 1, 2026. Before July 1, 2026, Global endpoint pricing applies to Non-global endpoints.

### Example cost calculation

A user needs to ensure they can support 10 queries per second (QPS) of a query with input of 1,000 text tokens and 500 audio tokens and receive an output of 300 text tokens using gemini-2.0-flash.

Using the throughput and burndown rate [table](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/provisioned-throughput/supported-models.md), for gemini-2.0-flash we know an input text token's burndown rate is 1 token, an input audio token's burndown rate is 7 tokens, and an output text token's burndown rate is 4 tokens.

The user's total input tokens is 1,000\* (1 token per input text token) + 500\* (7 tokens per input audio token) = 4,500 burndown adjusted input tokens. The user's total output tokens is 300\* (4 tokens per output text token) = 1,200 burndown adjusted output tokens. Adding them together gives us 4,500 burndown adjusted input tokens + 1,200 burndown adjusted output tokens = 5,700 total tokens per query.

Multiplying the total tokens per query by QPS gives us 5,700 total tokens per query \* 10 QPS = 57,000 total tokens per second.

Dividing this by the total throughput per second per GSU gives us 57,000 total tokens per second ÷ 3,360 per-second throughput per GSU = 16.96 GSUs. The minimum GSU purchase increment for this model is 1, so the user would need 17 GSUs.

If the user wanted to sustain this throughput for 1 week, it would cost $1,200 \* 17 GSUs = $20,400 per week. If they wanted to sustain this throughput for 1 month, it would cost $2,700 \* 17 GSUs = $45,900 per month. If they wanted to sustain this throughput for 3 months, it would cost $2,400 \* 17 GSUs = $40,800 per month. And finally, if they wanted to sustain this throughput for 1 year, it would cost $2,000 \* 17 GSUs = $34,000 per month.

### 50% Promotional Credits on Gemini 3.6 Flash & Gemini 3.7 Flash Provisioned Throughput Usage

Effective August 13, 2026 through December 31, 2026, Google Cloud is injecting a monthly billing credit equal to 50% of net eligible Provisioned Throughput spending on Gemini 3.6 Flash and Gemini 3.7 Flash models.

This credit will automatically be reflected in monthly invoices and will not alter Provisioned Throughput configurations or commitment burndown rates.

Issued credits apply to usage across On-Demand Gemini 3.6 Flash and 3.7 Flash SKUs, as well as Provisioned Throughput SKUs across all models. Credits are issued on the 7th day of each month following the billing period, and expire 30 days after issuance, under standard [Google Cloud Credit Terms of Service](https://cloud.google.com/terms/open-source-software-tos) **.** Spend for the initial month is pro-rated strictly for active usage between August 13 and August 31, 2026.

## Model Tuning

Model tuning is an effective way to customize large models to your tasks. It's a key step to improve the model's quality and efficiency. Model tuning provides the following benefits:

- Higher quality for your specific tasks
- Increased model robustness
- Lower inference latency and cost due to shorter prompts

Training tokens are calculated by the total number of tokens in your training dataset, multiplied by your number of epochs.

| Model | Type | Price (USD) |
| Gemini 3.5 Flash | Supervised fine-tuning<br>Reinforcement Learning fine-tuning | $0.01 / 1,000 count |
| Gemini 3.1 Flash Lite | Supervised fine-tuning | $0.003 / 1,000 count |
| Gemini 2.5 Pro | Supervised fine-tuning | $0.025 / 1,000 count |
| Gemini 2.5 Flash | Supervised fine-tuning<br>Preference tuning | $0.005 / 1,000 count |
| Gemini 2.5 Flash Lite | Supervised fine-tuning<br>Preference tuning | $0.0015 / 1,000 count |
| Gemma 3 1B IT | Supervised fine-tuning | $0.47 / 1,000,000 count |
| Gemma 3 4B IT | Supervised fine-tuning | $1.14 / 1,000,000 count |
| Gemma 3 12B IT | Supervised fine-tuning | $1.82 / 1,000,000 count |
| Gemma 3 27B IT | Supervised fine-tuning | $6.83 / 1,000,000 count |
| Medgemma 1.5 4B IT | Supervised fine-tuning | $1.14 / 1,000,000 count |
| Llama 3.1 8B | Supervised fine-tuning | $0.67 / 1,000,000 count |
| Llama 3.2 1B | Supervised fine-tuning | $0.28 / 1,000,000 count |
| Llama 3.2 3B | Supervised fine-tuning | $0.61 / 1,000,000 count |
| Llama 3.3 70B | Supervised fine-tuning | $6.72 / 1,000,000 count |
| Llama 4 Scout 17B 16E | Supervised fine-tuning | $5.77 / 1,000,000 count |
| Qwen 3 4B | Supervised fine-tuning | $1.35 / 1,000,000 count |
| Qwen 3 8B | Supervised fine-tuning | $4.18 / 1,000,000 count |
| Qwen 3 14B | Supervised fine-tuning | $8.46 / 1,000,000 count |
| Qwen 3 32B | Supervised fine-tuning | $6.57 / 1,000,000 count |

\\* For model inference starting from Gemini 3, tuned model endpoint prediction price will be 1.5 times of the base model. Old Gemini models prediction price stays the same as the base model.

Special Case of Charging by Characters

| Model | Type | Price /1M (USD) |
| Translation LLM 002 | Supervised fine-tuning | $6.25 |

## AlphaEvolve

The cost of AlphaEvolve is determined by the cost of the Gemini model used plus the cost of the AlphaEvolve agent.

| Gemini model | Type | Gemini model price /1M (USD) | AlphaEvolve agent price /1M (USD) | Total price /1M (USD) |
| Gemini 3.1 Pro Preview | Price per 1M input tokens | $2.00 | $4.00 | $6.00 |
|  | Price per 1M output and thinking tokens | $12.00 | $24.00 | $36.00 |
| Gemini 3.5 Flash | Price per 1M input tokens | $1.50 | $3.00 | $4.50 |
|  | Price per 1M output and thinking tokens | $9.00 | $18.00 | $27.00 |

## Partner models on Agent Platform

Partner models are a curated list of generative AI models developed by Google partners. Partner models are offered as managed APIs. For more information, see [Overview of partner models](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models). The following sections list pricing details for Google partner models.

## Anthropic’s Claude models

**Models with regional pricing**

GlobalUS Multi-Region (US)EU Multi-Region (EU)us-east5europe-west 1asia-southeast1asia-east1

| Model | Type | ModelPrice (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Opus 5 | Input | $5.00 | $5.00 |
|  | Output | $25.00 | $25.00 |
|  | Batch Input | $2.50 |  |
|  | Batch Output | $12.50 |  |
|  | 5m Cache Write | $6.25 | $6.25 |
|  | 1h Cache Write | $10.00 | $10.00 |
|  | Cache Hit | $0.50 | $0.50 |
|  | 5m Batch Cache Write | $3.125 |  |
|  | 1h Batch Cache Write | $5.00 |  |
|  | Batch Cache Hit | $0.25 |  |
| Claude Sonnet 5 | Input | $2.00 | $2.00 |
|  | Output | $10.00 | $10.00 |
|  | Batch Input | $1.00 | $1.00 |
|  | Batch Output | $5.00 | $5.00 |
|  | 5m Cache Write | $2.50 | $2.50 |
|  | 1h Cache Write | $4.00 | $4.00 |
|  | Cache Hit | $0.20 | $0.20 |
| Claude Fable 5 | Input | $10.00 | $10.00 |
|  | Output | $50.00 | $50.00 |
|  | Batch Input | $5.00 |  |
|  | Batch Output | $25.00 |  |
|  | 5m Cache Write | $12.50 | $12.50 |
|  | 1h Cache Write | $20.00 | $20.00 |
|  | Cache Hit | $1.00 | $1.00 |
|  | 5m Batch Cache Write | $6.25 |  |
|  | 1h Batch Cache Write | $10.00 |  |
|  | Batch Cache Hit | $0.50 |  |
| Claude Opus 4.8 | Input | $5.00 | $5.00 |
|  | Output | $25.00 | $25.00 |
|  | Batch Input | $2.50 |  |
|  | Batch Output | $12.50 |  |
|  | 5m Cache Write | $6.25 | $6.25 |
|  | 1h Cache Write | $10.00 | $10.00 |
|  | Cache Hit | $0.50 | $0.50 |
|  | 5m Batch Cache Write | $3.125 |  |
|  | 1h Batch Cache Write | $5.00 |  |
|  | Batch Cache Hit | $0.25 |  |
| Claude Opus 4.7 | Input | $5.00 | $5.00 |
|  | Output | $25.00 | $25.00 |
|  | Batch Input | $2.50 |  |
|  | Batch Output | $12.50 |  |
|  | 5m Cache Write | $6.25 | $6.25 |
|  | 1h Cache Write | $10.00 | $10.00 |
|  | Cache Hit | $0.50 | $0.50 |
|  | 5m Batch Cache Write | $3.125 |  |
|  | 1h Batch Cache Write | $5.00 | $5.00 |
|  | Batch Cache Hit | $0.25 |  |
| Claude Opus 4.6 | Input | $5.00 | $5.00 |
|  | Output | $25.00 | $25.00 |
|  | Batch Input | $2.50 |  |
|  | Batch Output | $12.50 |  |
|  | 5m Cache Write | $6.25 | $6.25 |
|  | 1h Cache Write | $10.00 | $10.00 |
|  | Cache Hit | $0.50 | $0.50 |
|  | 5m Batch Cache Write | $3.125 |  |
|  | 1h Batch Cache Write | $5.00 |  |
|  | Batch Cache Hit | $0.25 |  |
| Claude Opus 4.5 | Input | $5.00 |  |
|  | Output | $25.00 |  |
|  | Batch Input | $2.50 |  |
|  | Batch Output | $12.50 |  |
|  | 5m Cache Write | $6.25 |  |
|  | 1h Cache Write | $10.00 |  |
|  | Cache Hit | $0.50 |  |
|  | 5m Batch Cache Write | $3.125 |  |
|  | 1h Batch Cache Write | $5.00 |  |
|  | Batch Cache Hit | $0.25 |  |
| Claude Sonnet 4.6 | Input | $3.00 | $3.00 |
|  | Output | $15.00 | $15.00 |
|  | Batch Input | $1.50 |  |
|  | Batch Output | $7.50 |  |
|  | 5m Cache Write | $3.75 | $3.75 |
|  | 1h Cache Write | $6.00 | $6.00 |
|  | Cache Hit | $0.30 | $0.30 |
|  | 5m Batch Cache Write | $1.88 |  |
|  | 1h Batch Cache Write | $3.00 |  |
|  | Batch Cache Hit | $0.15 |  |
| Claude Sonnet 4.5 | Input | $3.00 | $6.00 |
|  | Output | $15.00 | $22.50 |
|  | Batch Input | $1.50 |  |
|  | Batch Output | $7.50 |  |
|  | 5m Cache Write | $3.75 | $7.50 |
|  | 1h Cache Write | $6.00 | $12.00 |
|  | Cache Hit | $0.30 | $0.60 |
|  | 5m Batch Cache Write | $1.88 |  |
|  | 1h Batch Cache Write | $3.00 |  |
|  | Batch Cache Hit | $0.15 |  |
|  | 5m Batch Cache Write | $1.00 |  |
| Claude Haiku 4.5 | Input | $1.00 |  |
|  | Output | $5.00 |  |
|  | Batch Input | $0.50 |  |
|  | Batch Output | $2.50 |  |
|  | 5m Cache Write | $1.25 |  |
|  | Batch Cache Hit | $0.05 |  |
|  | 1h Cache Write | $2.00 |  |
|  | Cache Hit | $0.10 |  |
|  | 5m Batch Cache Write | $0.625 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Opus 5 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Sonnet 5 | Input | $2.20 | $2.20 |
|  | Output | $11.00 | $11.00 |
|  | Batch Input | $1.10 | $1.10 |
|  | Batch Output | $5.50 | $5.50 |
|  | 5m Cache Write | $2.75 | $2.75 |
|  | 1h Cache Write | $4.40 | $4.40 |
|  | Cache Hit | $0.22 | $0.22 |
| Claude Fable 5 | Input | $11.00 | $11.00 |
|  | Output | $55.00 | $55.00 |
|  | Batch Input | $5.50 |  |
|  | Batch Output | $27.50 |  |
|  | 5m Cache Write | $13.75 | $13.75 |
|  | 1h Cache Write | $22.00 | $22.00 |
|  | Cache Hit | $1.10 | $1.10 |
|  | 5m Batch Cache Write | $6.875 |  |
|  | 1h Batch Cache Write | $11.00 |  |
|  | Batch Cache Hit | $0.55 |  |
| Claude Opus 4.8 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Opus 4.7 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Opus 5 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Sonnet 5 | Input | $2.20 | $2.20 |
|  | Output | $11.00 | $11.00 |
|  | Batch Input | $1.10 | $1.10 |
|  | Batch Output | $5.50 | $5.50 |
|  | 5m Cache Write | $2.75 | $2.75 |
|  | 1h Cache Write | $4.40 | $4.40 |
|  | Cache Hit | $0.22 | $0.22 |
| Claude Fable 5 | Input | $11.00 | $11.00 |
|  | Output | $55.00 | $55.00 |
|  | Batch Input | $5.50 |  |
|  | Batch Output | $27.50 |  |
|  | 5m Cache Write | $13.75 | $13.75 |
|  | 1h Cache Write | $22.00 | $22.00 |
|  | Cache Hit | $1.10 | $1.10 |
|  | 5m Batch Cache Write | $6.875 |  |
|  | 1h Batch Cache Write | $11.00 |  |
|  | Batch Cache Hit | $0.55 |  |
| Claude Opus 4.8 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Opus 4.7 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Claude Opus 4.6 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Opus 4.5 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Sonnet 4.6 | Input | $3.30 | $3.30 |
|  | Output | $16.50 | $16.50 |
|  | Batch Input | $1.65 |  |
|  | Batch Output | $8.25 |  |
|  | 5m Cache Write | $4.13 | $4.13 |
|  | 1h Cache Write | $6.60 | $6.60 |
|  | Cache Hit | $0.33 | $0.33 |
|  | 5m Batch Cache Write | $2.06 |  |
|  | 1h Batch Cache Write | $3.30 |  |
|  | Batch Cache Hit | $0.17 |  |
|  | Input | $6.60 |  |
|  | Output | $24.75 |  |
| Claude Sonnet 4.5 | Input | $3.30 | $6.60 |
|  | Output | $16.50 | $24.75 |
|  | Batch Input | $1.65 |  |
|  | Batch Output | $8.25 |  |
|  | 5m Cache Write | $4.13 | $8.25 |
|  | 1h Cache Write | $6.60 | $13.20 |
|  | Cache Hit | $0.33 | $0.66 |
|  | 5m Batch Cache Write | $2.06 |  |
|  | 1h Batch Cache Hit | $3.30 |  |
|  | Batch Cache Hit | $0.17 |  |
| Claude Haiku 4.5 | Input | $1.10 |  |
|  | Output | $5.50 |  |
|  | Batch Input | $0.55 |  |
|  | Batch Output | $2.75 |  |
|  | 5m Cache Write | $1.375 |  |
|  | 1h Cache Write | $2.20 |  |
|  | Cache Write | $1.375 |  |
|  | Cache Hit | $0.11 |  |
|  | 5m Batch Cache Write | $0.688 |  |
|  | 1h Batch Cache Write | $1.10 |  |
|  | Batch Cache Hit | $0.055 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Claude Opus 4.6 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Opus 4.5 | Input | $5.50 |  |
|  | Output | $27.50 |  |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 |  |
|  | 1h Cache Write | $11.00 |  |
|  | Cache Hit | $0.55 |  |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Sonnet 4.6 | Input | $3.30 | $3.30 |
|  | Output | $16.50 | $16.50 |
|  | Batch Input | $1.65 |  |
|  | Batch Output | $8.25 |  |
|  | 5m Batch Write | $4.13 | $4.13 |
|  | 1h Cache Write | $6.60 | $6.60 |
|  | Cache Hit | $0.33 | $0.33 |
|  | 5m Batch Cache Hit | $2.06 |  |
|  | 1h Batch Cache Write | $3.30 |  |
|  | Batch Cache Hit | $0.17 |  |
| Claude Sonnet 4.5 | Input | $3.30 | $6.60 |
|  | Output | $16.50 | $24.75 |
|  | Batch Input | $1.65 |  |
|  | Batch Output | $8.25 |  |
|  | 5m Cache Write | $4.13 | $8.25 |
|  | 1h Cache Write | $6.60 | $13.20 |
|  | Cache Hit | $0.33 | $0.66 |
|  | 5m Batch Cache Write | $2.06 |  |
|  | 1h Batch Cache Write | $3.30 |  |
|  | Batch Cache Hit | $0.17 |  |
| Claude Haiku 4.5 | Input | $1.10 |  |
|  | Output | $5.50 |  |
|  | Batch Input | $0.55 |  |
|  | Batch Output | $2.75 |  |
|  | 5m Cache Write | $1.375 |  |
|  | 1h Cache Write | $2.20 |  |
|  | Cache Hit | $0.11 |  |
|  | 5m Batch Cache Write | $0.688 |  |
|  | 1h Batch Cache Write | $1.10 |  |
|  | Batch Cache Hit | $0.055 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Claude Opus 4.6 | Input | $5.50 | $5.50 |
|  | Output | $27.50 | $27.50 |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 | $6.875 |
|  | 1h Cache Write | $11.00 | $11.00 |
|  | Cache Hit | $0.55 | $0.55 |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Opus 4.5 | Input | $5.50 |  |
|  | Output | $27.50 |  |
|  | Batch Input | $2.75 |  |
|  | Batch Output | $13.75 |  |
|  | 5m Cache Write | $6.875 |  |
|  | 1h Cache Write | $11.00 |  |
|  | Cache Hit | $0.55 |  |
|  | 5m Batch Cache Write | $3.438 |  |
|  | 1h Batch Cache Write | $5.50 |  |
|  | Batch Cache Hit | $0.275 |  |
| Claude Sonnet 4.6 | Input | $3.30 | $3.30 |
|  | Output | $16.50 | $16.50 |
|  | Batch Input | $1.65 |  |
|  | Batch Output | $8.25 |  |
|  | 5m Cache Write | $4.13 | $4.13 |
|  | 1h Cache Write | $6.60 | $6.60 |
|  | Cache Hit | $0.33 |  |
|  | 5m Batch Cache Write | $2.06 |  |
|  | 1h Batch Cache Write | $3.30 |  |
|  | Batch Cache Hit | $0.17 |  |
| Claude Sonnet 4.5 | Input | $3.30 | $6.60 |
|  | Output | $16.50 | $24.75 |
|  | Batch Input | $1.65 |  |
|  | Batch Output | $8.25 |  |
|  | 5m Cache Write | $4.13 | $8.25 |
|  | 1h Cache Write | $6.60 | $13.20 |
|  | Cache Hit | $0.33 | $0.66 |
|  | 5m Batch Cache Write | $2.06 |  |
|  | 1h Batch Cache Write | $3.30 |  |
|  | Batch Cache Hit | $0.17 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Claude Haiku 4.5 | Input | $1.10 |  |
|  | Output | $5.50 |  |
|  | Batch Input | $0.55 |  |
|  | Batch Output | $2.75 |  |
|  | 5m Cache Write | $1.375 |  |
|  | 1h Cache Write | $2.20 |  |
|  | Cache Hit | $0.11 |  |
|  | 5m Batch Cache Write | $0.688 |  |
|  | 1h Batch Cache Write | $1.10 |  |
|  | Batch Cache Hit | $0.055 |  |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

Models with uniform pricing across all regions

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Claude Opus 4.1 | Input | $15 | N/A |
|  | Output | $75 | N/A |
|  | Batch Input | $7.50 | N/A |
|  | Batch Output | $37.50 | N/A |
|  | 5m Cache Write | $18.75 | N/A |
|  | 1h Cache Write | $30 | N/A |
|  | Cache Hit | $1.50 | N/A |
|  | 5m Batch Cache Write | $9.375 | N/A |
|  | 1h Batch Cache Write | $15.00 | N/A |
|  | Batch Cache Hit | $0.75 | N/A |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

### Pricing for tools

| Tool | Price (USD) |
| Web Search Request | **$10 per 1000 searches**<br>﻿Models Supported: Claude Haiku 4.5, Claude Sonnet 4.5, Claude Sonnet 4.6, Claude Sonnet 4, Claude Opus 4.1, Claude Opus 4, Claude Opus 4.5 and Claude Opus 4.6. |

\\* If a query input context is longer than or equal to 200K tokens, all tokens (input and output) are charged at long context rates.

## xAI's Grok models

| Model | Type | Price (/1M tokens) =< 200K input tokens | Price (/1M tokens) > 200K input tokens |
| Grok 4.6 | Input | $2.00 | $4.00 |
|  | Output | $6.00 | $12.00 |
|  | Cache Hit | $0.50 | $1.00 |
| Grok 4.20 Reasoning | Input | $1.25 | $2.50 |
|  | Output | $2.50 | $5.00 |
|  | Cache Hit | $0.20 | $0.40 |
| Grok 4.20 Non-Reasoning | Input | $1.25 | $2.50 |
|  | Output | $2.50 | $5.00 |
|  | Cache Hit | $0.20 | $0.40 |
| Grok 4.3 | Input | $1.25 | $2.50 |
|  | Output | $2.50 | $5.00 |
|  | Cache Hit | $0.20 | $0.40 |

\\* If a query input context is longer than 200K tokens, all tokens are charged at long context rates.

| Model | Type | Price / 1M tokens (USD) |
| Grok 4.1 Fast Reasoning | Input | $0.20 |
|  | Output | $0.50 |
|  | Cache Hit | $0.05 |
| Grok 4.1 Fast Non-Reasoning | Input | $0.20 |
|  | Output | $0.50 |
|  | Cache Hit | $0.05 |

## Deepseek's models

| Model | Type | Price /1M (USD) |
| DeepSeek-V3.1 | Input | $0.60 |
|  | Output | $1.70 |
|  | Cache Hit | $0.06 |
|  | Batch Input | $0.30 |
|  | Batch Output | $0.85 |
| DeepSeek-V3.2 | Input | $0.56 |
|  | Output | $1.68 |
|  | Cache Hit | $0.056 |
|  | Batch Input | $0.28 |
|  | Batch Output | $0.84 |
| DeepSeek-R1 (0528) | Input | $1.35 |
|  | Output | $5.40 |
|  | Batch Input | $0.675 |
|  | Batch Output | $2.70 |
| DeepSeek-OCR | Input | $0.30 |
|  | Output | $1.20 |

## MiniMax's models

| Model | Type | Price /1M (USD) |
| MiniMax-M2 | Input | $0.30 |
|  | Output | $1.20 |
|  | Cache Hit | $0.03 |

## Moonshot's models

| Model | Type | Price /1M (USD) |
| Kimi-K2-Thinking | Input | $0.60 |
|  | Output | $2.50 |
|  | Cache Hit | $0.06 |

## Qwen's models

| Model | Type | Price /1M (USD) |
| Qwen3-Next-80B-Thinking | Input | $0.15 |
|  | Output | $1.20 |
| Qwen3-Next-80B-Instruct | Input | $0.15 |
|  | Output | $1.20 |
| Qwen3-Coder-480B-A35B-Instruct | Input | $0.22 |
|  | Output | $1.80 |
|  | Cache Hit | $0.022 |
|  | Batch Input | $0.11 |
|  | Batch Output | $0.90 |
| Qwen3-235B-A22B-Instruct-2507 | Input | $0.22 |
|  | Output | $0.88 |
|  | Batch Input | $0.11 |
|  | Batch Output | $0.44 |

## GLM's models

| Model | Type | Price /1M (USD) |
| GLM-4.7 | Input | $0.60 |
|  | Output | $2.20 |
|  | Cache Hit | $0.06 |
| GLM-5 | Input | $1.00 |
|  | Output | $3.20 |
|  | Cache Hit | $0.10 |
| GLM-5.2 | Input | $1.40 |
|  | Output | $4.40 |
|  | Cached Input: | $0.14 |

## OpenAI's models

| Model | Type | Price /1M (USD) |
| gpt-oss-120b | Input | $0.09 |
|  | Output | $0.36 |
|  | Batch Input | $0.045 |
|  | Batch Output | $0.18 |
| gpt-oss-20b | Input | $0.07 |
|  | Output | $0.25 |
|  | Cache Hit | $0.007 |
|  | Batch Input | $0.035 |
|  | Batch Output | $0.125 |

## Meta's Llama models

| Model | Type | Price /1M (USD) |
| Llama 3.3 70B | Input | $0.72 |
|  | Output | $0.72 |
|  | Batch Input | $0.36 |
|  | Batch Output | $0.36 |
| Llama 4 Scout | Input | $0.25 |
|  | Output | $0.70 |
|  | Batch Input | $0.125 |
|  | Batch Output | $0.35 |
| Llama 4 Maverick | Input | $0.35 |
|  | Output | $1.15 |
|  | Batch Input | $0.175 |
|  | Batch Output | $0.575 |

## Mistral AI’s models

| Model | Type | Price /1M (USD) |
| Mistral OCR (25.05) | Input | $0.0005 (or $0.0005/page) |
|  | Output | $0.0005 (or $0.0005/page) |
| Mistral Medium 3 | Input | $0.40 |
|  | Output | $2.00 |
| Mistral Small 3.1 (25.03) | Input | $0.10 |
|  | Output | $0.30 |
| Codestral 2 | Input | $0.30 |
|  | Output | $0.90 |

## Request a custom quote

With Google Cloud's pay-as-you-go pricing, you only pay for the services you use. Connect with our sales team to get a custom quote for your organization.

Contact sales [Contact sales](https://cloud.google.com/contact?direct=true)