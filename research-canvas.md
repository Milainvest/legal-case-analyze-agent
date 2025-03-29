---
title: "GitHub CopilotKit/CopilotKit LLM Context"
source: "https://uithub.com/CopilotKit/CopilotKit/tree/main/examples/coagents-research-canvas"
author:
  - "[[Code From Anywhere]]"
published:
created: 2025-03-28
description: "Easily ask your LLM code questions about"
tags:
  - "clippings"
---
The response has been limited to 50k tokens of the smallest files in the repo. You can remove this limitation by removing the max tokens filter.

```
└── examples
    └── coagents-research-canvas
        ├── agent-js
            ├── .gitignore
            ├── langgraph.json
            ├── package.json
            ├── pnpm-lock.yaml
            ├── src
            │   ├── agent.ts
            │   ├── chat.ts
            │   ├── delete.ts
            │   ├── download.ts
            │   ├── index.ts
            │   ├── model.ts
            │   ├── search.ts
            │   └── state.ts
            └── tsconfig.json
        ├── agent
            ├── .gitignore
            ├── .vscode
            │   ├── cspell.json
            │   └── settings.json
            ├── install.log
            ├── langgraph.json
            ├── poetry.lock
            ├── pyproject.toml
            └── research_canvas
            │   ├── __init__.py
            │   ├── crewai
            │       ├── __init__.py
            │       ├── agent.py
            │       ├── delete.py
            │       ├── demo.py
            │       ├── download.py
            │       ├── prompt.py
            │       └── tools.py
            │   ├── demo.py
            │   └── langgraph
            │       ├── __init__.py
            │       ├── agent.py
            │       ├── chat.py
            │       ├── delete.py
            │       ├── demo.py
            │       ├── download.py
            │       ├── model.py
            │       ├── search.py
            │       └── state.py
        ├── dockerize.sh
        ├── readme.md
        ├── ui
            ├── .eslintrc.json
            ├── .gitignore
            ├── README.md
            ├── components.json
            ├── next.config.mjs
            ├── package.json
            ├── pnpm-lock.yaml
            ├── postcss.config.mjs
            ├── src
            │   ├── app
            │   │   ├── Main.tsx
            │   │   ├── api
            │   │   │   └── copilotkit
            │   │   │   │   └── route.ts
            │   │   ├── favicon.ico
            │   │   ├── fonts
            │   │   │   ├── GeistMonoVF.woff
            │   │   │   └── GeistVF.woff
            │   │   ├── globals.css
            │   │   ├── layout.tsx
            │   │   └── page.tsx
            │   ├── components
            │   │   ├── AddResourceDialog.tsx
            │   │   ├── EditResourceDialog.tsx
            │   │   ├── ModelSelector.tsx
            │   │   ├── Progress.tsx
            │   │   ├── ResearchCanvas.tsx
            │   │   ├── Resources.tsx
            │   │   └── ui
            │   │   │   ├── button.tsx
            │   │   │   ├── card.tsx
            │   │   │   ├── dialog.tsx
            │   │   │   ├── input.tsx
            │   │   │   ├── select.tsx
            │   │   │   └── textarea.tsx
            │   └── lib
            │   │   ├── model-selector-provider.tsx
            │   │   ├── types.ts
            │   │   └── utils.ts
            ├── tailwind.config.ts
            └── tsconfig.json
        └── wfcms-data.json

/examples/coagents-research-canvas/agent-js/.gitignore:
--------------------------------------------------------------------------------
1 | venv/
2 | __pycache__/
3 | *.pyc
4 | .env
5 | .vercel
6 | 
7 | # LangGraph API
8 | .langgraph_api

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/langgraph.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "node_version": "20",
 3 |   "dockerfile_lines": ["RUN npm i -g corepack@latest"],
 4 |   "dependencies": ["."],
 5 |   "graphs": {
 6 |     "research_agent": "./src/agent.ts:graph"
 7 |   },
 8 |   "env": ".env"
 9 | }
10 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/package.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "name": "agent_js",
 3 |   "version": "1.0.0",
 4 |   "description": "",
 5 |   "main": "index.js",
 6 |   "scripts": {
 7 |     "test": "echo \"Error: no test specified\" && exit 1"
 8 |   },
 9 |   "packageManager": "pnpm@9.5.0",
10 | 
11 |   "keywords": [],
12 |   "author": "",
13 |   "license": "ISC",
14 |   "devDependencies": {
15 |     "@types/html-to-text": "^9.0.4",
16 |     "@types/node": "^22.9.0",
17 |     "typescript": "^5.6.3"
18 |   },
19 |   "dependencies": {
20 |     "@copilotkit/sdk-js": "^1.5.13",
21 |     "@langchain/anthropic": "^0.3.8",
22 |     "@langchain/core": "^0.3.18",
23 |     "@langchain/google-genai": "^0.1.4",
24 |     "@langchain/langgraph": "^0.2.44",
25 |     "@langchain/langgraph-cli": "^0.0.10",
26 |     "@langchain/openai": "^0.3.14",
27 |     "@tavily/core": "^0.0.2",
28 |     "html-to-text": "^9.0.5",
29 |     "zod": "^3.23.8"
30 |   }
31 | }
32 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/agent.ts:
--------------------------------------------------------------------------------
 1 | /**
 2 |  * This is the main entry point for the AI.
 3 |  * It defines the workflow graph and the entry point for the agent.
 4 |  */
 5 | 
 6 | import { AIMessage, ToolMessage } from "@langchain/core/messages";
 7 | import { StateGraph, END } from "@langchain/langgraph";
 8 | import { MemorySaver } from "@langchain/langgraph";
 9 | import { AgentState, AgentStateAnnotation } from "./state";
10 | import { download_node } from "./download";
11 | import { chat_node } from "./chat";
12 | import { search_node } from "./search";
13 | import { delete_node, perform_delete_node } from "./delete";
14 | 
15 | const workflow = new StateGraph(AgentStateAnnotation)
16 |   .addNode("download", download_node)
17 |   .addNode("chat_node", chat_node)
18 |   .addNode("search_node", search_node)
19 |   .addNode("delete_node", delete_node)
20 |   .addNode("perform_delete_node", perform_delete_node)
21 |   .setEntryPoint("download")
22 |   .addEdge("download", "chat_node")
23 |   .addConditionalEdges("chat_node", route, [
24 |     "search_node",
25 |     "chat_node",
26 |     "delete_node",
27 |     END,
28 |   ])
29 |   .addEdge("delete_node", "perform_delete_node")
30 |   .addEdge("perform_delete_node", "chat_node")
31 |   .addEdge("search_node", "download");
32 | 
33 | export const graph = workflow.compile({
34 |   interruptAfter: ["delete_node"],
35 | });
36 | 
37 | function route(state: AgentState) {
38 |   const messages = state.messages || [];
39 | 
40 |   if (
41 |     messages.length > 0 &&
42 |     messages[messages.length - 1].constructor.name === "AIMessageChunk"
43 |   ) {
44 |     const aiMessage = messages[messages.length - 1] as AIMessage;
45 | 
46 |     if (
47 |       aiMessage.tool_calls &&
48 |       aiMessage.tool_calls.length > 0 &&
49 |       aiMessage.tool_calls[0].name === "Search"
50 |     ) {
51 |       return "search_node";
52 |     } else if (
53 |       aiMessage.tool_calls &&
54 |       aiMessage.tool_calls.length > 0 &&
55 |       aiMessage.tool_calls[0].name === "DeleteResources"
56 |     ) {
57 |       return "delete_node";
58 |     }
59 |   }
60 |   if (
61 |     messages.length > 0 &&
62 |     messages[messages.length - 1].constructor.name === "ToolMessage"
63 |   ) {
64 |     return "chat_node";
65 |   }
66 |   return END;
67 | }
68 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/chat.ts:
--------------------------------------------------------------------------------
  1 | /**
  2 |  * Chat Node
  3 |  */
  4 | 
  5 | import { RunnableConfig } from "@langchain/core/runnables";
  6 | import { AgentState, Resource } from "./state";
  7 | import { getModel } from "./model";
  8 | import { getResource } from "./download";
  9 | import {
 10 |   SystemMessage,
 11 |   AIMessage,
 12 |   ToolMessage,
 13 | } from "@langchain/core/messages";
 14 | import { tool } from "@langchain/core/tools";
 15 | import { z } from "zod";
 16 | import { copilotkitCustomizeConfig } from "@copilotkit/sdk-js/langgraph";
 17 | 
 18 | const Search = tool(() => {}, {
 19 |   name: "Search",
 20 |   description:
 21 |     "A list of one or more search queries to find good resources to support the research.",
 22 |   schema: z.object({ queries: z.array(z.string()) }),
 23 | });
 24 | 
 25 | const WriteReport = tool(() => {}, {
 26 |   name: "WriteReport",
 27 |   description: "Write the research report.",
 28 |   schema: z.object({ report: z.string() }),
 29 | });
 30 | 
 31 | const WriteResearchQuestion = tool(() => {}, {
 32 |   name: "WriteResearchQuestion",
 33 |   description: "Write the research question.",
 34 |   schema: z.object({ research_question: z.string() }),
 35 | });
 36 | 
 37 | const DeleteResources = tool(() => {}, {
 38 |   name: "DeleteResources",
 39 |   description: "Delete the URLs from the resources.",
 40 |   schema: z.object({ urls: z.array(z.string()) }),
 41 | });
 42 | 
 43 | export async function chat_node(state: AgentState, config: RunnableConfig) {
 44 |   const customConfig = copilotkitCustomizeConfig(config, {
 45 |     emitIntermediateState: [
 46 |       {
 47 |         stateKey: "report",
 48 |         tool: "WriteReport",
 49 |         toolArgument: "report",
 50 |       },
 51 |       {
 52 |         stateKey: "research_question",
 53 |         tool: "WriteResearchQuestion",
 54 |         toolArgument: "research_question",
 55 |       },
 56 |     ],
 57 |     emitToolCalls: "DeleteResources",
 58 |   });
 59 | 
 60 |   state["resources"] = state.resources || [];
 61 |   const researchQuestion = state.research_question || "";
 62 |   const report = state.report || "";
 63 | 
 64 |   const resources: Resource[] = [];
 65 | 
 66 |   for (const resource of state["resources"]) {
 67 |     const content = getResource(resource.url);
 68 |     if (content === "ERROR") {
 69 |       continue;
 70 |     }
 71 |     resource.content = content;
 72 |     resources.push(resource);
 73 |   }
 74 | 
 75 |   const model = getModel(state);
 76 |   const invokeArgs: Record<string, unknown> = {};
 77 |   if (model.constructor.name === "ChatOpenAI") {
 78 |     invokeArgs["parallel_tool_calls"] = false;
 79 |   }
 80 | 
 81 |   const response = await model.bindTools!(
 82 |     [Search, WriteReport, WriteResearchQuestion, DeleteResources],
 83 |     invokeArgs
 84 |   ).invoke(
 85 |     [
 86 |       new SystemMessage(
 87 |         \`You are a research assistant. You help the user with writing a research report.
 88 |         Do not recite the resources, instead use them to answer the user's question.
 89 |         You should use the search tool to get resources before answering the user's question.
 90 |         If you finished writing the report, ask the user proactively for next steps, changes etc, make it engaging.
 91 |         To write the report, you should use the WriteReport tool. Never EVER respond with the report, only use the tool.
 92 |         If a research question is provided, YOU MUST NOT ASK FOR IT AGAIN.
 93 | 
 94 |         This is the research question:
 95 |         ${researchQuestion}
 96 | 
 97 |         This is the research report:
 98 |         ${report}
 99 | 
100 |         Here are the resources that you have available:
101 |         ${JSON.stringify(resources)}
102 |         \`
103 |       ),
104 |       ...state.messages,
105 |     ],
106 |     customConfig
107 |   );
108 | 
109 |   const aiMessage = response as AIMessage;
110 | 
111 |   if (aiMessage.tool_calls && aiMessage.tool_calls.length > 0) {
112 |     if (aiMessage.tool_calls[0].name === "WriteReport") {
113 |       const report = aiMessage.tool_calls[0].args.report;
114 |       return {
115 |         report,
116 |         messages: [
117 |           aiMessage,
118 |           new ToolMessage({
119 |             tool_call_id: aiMessage.tool_calls![0]["id"]!,
120 |             content: "Report written.",
121 |             name: "WriteReport",
122 |           }),
123 |         ],
124 |       };
125 |     } else if (aiMessage.tool_calls[0].name === "WriteResearchQuestion") {
126 |       const researchQuestion = aiMessage.tool_calls[0].args.research_question;
127 |       return {
128 |         research_question: researchQuestion,
129 |         messages: [
130 |           aiMessage,
131 |           new ToolMessage({
132 |             tool_call_id: aiMessage.tool_calls![0]["id"]!,
133 |             content: "Research question written.",
134 |             name: "WriteResearchQuestion",
135 |           }),
136 |         ],
137 |       };
138 |     }
139 |   }
140 | 
141 |   return {
142 |     messages: response,
143 |   };
144 | }
145 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/delete.ts:
--------------------------------------------------------------------------------
 1 | /**
 2 |  * Delete Resources
 3 |  */
 4 | 
 5 | import { AgentState } from "./state";
 6 | import { RunnableConfig } from "@langchain/core/runnables";
 7 | import { ToolMessage, AIMessage } from "@langchain/core/messages";
 8 | 
 9 | export async function delete_node(
10 |   state: AgentState,
11 |   config: RunnableConfig
12 | ): Promise<AgentState> {
13 |   /**
14 |    * Delete Node
15 |    */
16 |   return state;
17 | }
18 | 
19 | export async function perform_delete_node(
20 |   state: AgentState,
21 |   config: RunnableConfig
22 | ) {
23 |   /**
24 |    * Perform Delete Node
25 |    */
26 |   const aiMessage = state["messages"][
27 |     state["messages"].length - 2
28 |   ] as AIMessage;
29 |   const toolMessage = state["messages"][
30 |     state["messages"].length - 1
31 |   ] as ToolMessage;
32 | 
33 |   let resources = state["resources"];
34 | 
35 |   if (toolMessage.content === "YES") {
36 |     let urls: string[];
37 | 
38 |     if (aiMessage.tool_calls) {
39 |       urls = aiMessage.tool_calls[0].args.urls;
40 |     } else {
41 |       const parsedToolCall = JSON.parse(
42 |         aiMessage.additional_kwargs!.function_call!.arguments
43 |       );
44 |       urls = parsedToolCall.urls;
45 |     }
46 | 
47 |     resources = resources.filter((resource) => !urls.includes(resource.url));
48 |   }
49 | 
50 |   return {
51 |     resources,
52 |   };
53 | }
54 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/download.ts:
--------------------------------------------------------------------------------
 1 | /**
 2 |  * Download Node
 3 |  *
 4 |  * This module contains the implementation of the download_node function.
 5 |  */
 6 | 
 7 | import { RunnableConfig } from "@langchain/core/runnables";
 8 | import { AgentState } from "./state";
 9 | import { htmlToText } from "html-to-text";
10 | import { copilotkitEmitState } from "@copilotkit/sdk-js/langgraph";
11 | 
12 | const RESOURCE_CACHE: Record<string, string> = {};
13 | 
14 | export function getResource(url: string): string {
15 |   return RESOURCE_CACHE[url] || "";
16 | }
17 | 
18 | const USER_AGENT =
19 |   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3";
20 | 
21 | async function downloadResource(url: string): Promise<string> {
22 |   const controller = new AbortController();
23 |   const timeoutId = setTimeout(() => controller.abort(), 5000);
24 | 
25 |   try {
26 |     const response = await fetch(url, {
27 |       headers: { "User-Agent": USER_AGENT },
28 |       signal: controller.signal,
29 |     });
30 |     clearTimeout(timeoutId);
31 | 
32 |     if (!response.ok) {
33 |       throw new Error(\`Failed to download resource: ${response.statusText}\`);
34 |     }
35 | 
36 |     const htmlContent = await response.text();
37 |     const markdownContent = htmlToText(htmlContent);
38 |     RESOURCE_CACHE[url] = markdownContent;
39 |     return markdownContent;
40 |   } catch (error) {
41 |     clearTimeout(timeoutId);
42 |     RESOURCE_CACHE[url] = "ERROR";
43 |     return \`Error downloading resource: ${error}\`;
44 |   }
45 | }
46 | 
47 | export async function download_node(state: AgentState, config: RunnableConfig) {
48 |   const resources = state["resources"] || [];
49 |   const logs = state["logs"] || [];
50 | 
51 |   const resourcesToDownload = [];
52 | 
53 |   const logsOffset = logs.length;
54 | 
55 |   // Find resources that are not downloaded
56 |   for (const resource of resources) {
57 |     if (!getResource(resource.url)) {
58 |       resourcesToDownload.push(resource);
59 |       logs.push({
60 |         message: \`Downloading ${resource.url}\`,
61 |         done: false,
62 |       });
63 |     }
64 |   }
65 | 
66 |   // Emit the state to let the UI update
67 |   const { messages, ...restOfState } = state;
68 |   await copilotkitEmitState(config, {
69 |     ...restOfState,
70 |     resources,
71 |     logs,
72 |   });
73 | 
74 |   // Download the resources
75 |   for (let i = 0; i < resourcesToDownload.length; i++) {
76 |     const resource = resourcesToDownload[i];
77 |     await downloadResource(resource.url);
78 |     logs[logsOffset + i]["done"] = true;
79 |     await copilotkitEmitState(config, state);
80 |   }
81 |   return {
82 |     resources,
83 |     logs,
84 |   };
85 | }
86 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/index.ts:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/agent-js/src/index.ts

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/model.ts:
--------------------------------------------------------------------------------
 1 | /**
 2 |  * This module provides a function to get a model based on the configuration.
 3 |  */
 4 | import { BaseChatModel } from "@langchain/core/language_models/chat_models";
 5 | import { AgentState } from "./state";
 6 | import { ChatOpenAI } from "@langchain/openai";
 7 | import { ChatAnthropic } from "@langchain/anthropic";
 8 | import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
 9 | 
10 | function getModel(state: AgentState): BaseChatModel {
11 |   /**
12 |    * Get a model based on the environment variable.
13 |    */
14 |   const stateModel = state.model;
15 |   const model = process.env.MODEL || stateModel;
16 | 
17 |   console.log(\`Using model: ${model}\`);
18 | 
19 |   if (model === "openai") {
20 |     return new ChatOpenAI({ temperature: 0, model: "gpt-4o" });
21 |   }
22 |   if (model === "anthropic") {
23 |     return new ChatAnthropic({
24 |       temperature: 0,
25 |       modelName: "claude-3-5-sonnet-20240620",
26 |     });
27 |   }
28 |   if (model === "google_genai") {
29 |     return new ChatGoogleGenerativeAI({
30 |       temperature: 0,
31 |       model: "gemini-1.5-pro",
32 |       apiKey: process.env.GOOGLE_API_KEY || undefined,
33 |     });
34 |   }
35 | 
36 |   throw new Error("Invalid model specified");
37 | }
38 | 
39 | export { getModel };
40 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/search.ts:
--------------------------------------------------------------------------------
  1 | /**
  2 |  * Search Node
  3 |  */
  4 | 
  5 | /**
  6 |  * The search node is responsible for searching the internet for information.
  7 |  */
  8 | 
  9 | import { z } from "zod";
 10 | import { tool } from "@langchain/core/tools";
 11 | import { tavily } from "@tavily/core";
 12 | import { AgentState } from "./state";
 13 | import { RunnableConfig } from "@langchain/core/runnables";
 14 | import {
 15 |   AIMessage,
 16 |   SystemMessage,
 17 |   ToolMessage,
 18 | } from "@langchain/core/messages";
 19 | import { getModel } from "./model";
 20 | import {
 21 |   copilotkitCustomizeConfig,
 22 |   copilotkitEmitState,
 23 | } from "@copilotkit/sdk-js/langgraph";
 24 | 
 25 | const ResourceInput = z.object({
 26 |   url: z.string().describe("The URL of the resource"),
 27 |   title: z.string().describe("The title of the resource"),
 28 |   description: z.string().describe("A short description of the resource"),
 29 | });
 30 | 
 31 | const ExtractResources = tool(() => {}, {
 32 |   name: "ExtractResources",
 33 |   description: "Extract the 3-5 most relevant resources from a search result.",
 34 |   schema: z.object({ resources: z.array(ResourceInput) }),
 35 | });
 36 | 
 37 | const tavilyClient = tavily({
 38 |   apiKey: process.env.TAVILY_API_KEY,
 39 | });
 40 | 
 41 | export async function search_node(state: AgentState, config: RunnableConfig) {
 42 |   const aiMessage = state["messages"][
 43 |     state["messages"].length - 1
 44 |   ] as AIMessage;
 45 | 
 46 |   let resources = state["resources"] || [];
 47 |   let logs = state["logs"] || [];
 48 | 
 49 |   const queries = aiMessage.tool_calls![0]["args"]["queries"];
 50 | 
 51 |   for (const query of queries) {
 52 |     logs.push({
 53 |       message: \`Search for ${query}\`,
 54 |       done: false,
 55 |     });
 56 |   }
 57 |   const { messages, ...restOfState } = state;
 58 |   await copilotkitEmitState(config, {
 59 |     ...restOfState,
 60 |     logs,
 61 |     resources,
 62 |   });
 63 | 
 64 |   const search_results = [];
 65 | 
 66 |   for (let i = 0; i < queries.length; i++) {
 67 |     const query = queries[i];
 68 |     const response = await tavilyClient.search(query, {});
 69 |     search_results.push(response);
 70 |     logs[i]["done"] = true;
 71 |     await copilotkitEmitState(config, {
 72 |       ...restOfState,
 73 |       logs,
 74 |       resources,
 75 |     });
 76 |   }
 77 | 
 78 |   const searchResultsToolMessageFull = new ToolMessage({
 79 |     tool_call_id: aiMessage.tool_calls![0]["id"]!,
 80 |     content: \`Performed search: ${JSON.stringify(search_results)}\`,
 81 |     name: "Search",
 82 |   });
 83 | 
 84 |   const searchResultsToolMessage = new ToolMessage({
 85 |     tool_call_id: aiMessage.tool_calls![0]["id"]!,
 86 |     content: \`Performed search.\`,
 87 |     name: "Search",
 88 |   });
 89 | 
 90 |   const customConfig = copilotkitCustomizeConfig(config, {
 91 |     emitIntermediateState: [
 92 |       {
 93 |         stateKey: "resources",
 94 |         tool: "ExtractResources",
 95 |         toolArgument: "resources",
 96 |       },
 97 |     ],
 98 |   });
 99 | 
100 |   const model = getModel(state);
101 |   const invokeArgs: Record<string, any> = {};
102 |   if (model.constructor.name === "ChatOpenAI") {
103 |     invokeArgs["parallel_tool_calls"] = false;
104 |   }
105 | 
106 |   logs = [];
107 | 
108 |   await copilotkitEmitState(config, {
109 |     ...restOfState,
110 |     resources,
111 |     logs,
112 |   });
113 | 
114 |   const response = await model.bindTools!([ExtractResources], {
115 |     ...invokeArgs,
116 |     tool_choice: "ExtractResources",
117 |   }).invoke(
118 |     [
119 |       new SystemMessage({
120 |         content: \`You need to extract the 3-5 most relevant resources from the following search results.\`,
121 |       }),
122 |       ...state["messages"],
123 |       searchResultsToolMessageFull,
124 |     ],
125 |     customConfig
126 |   );
127 | 
128 |   const aiMessageResponse = response as AIMessage;
129 |   const newResources = aiMessageResponse.tool_calls![0]["args"]["resources"];
130 | 
131 |   resources.push(...newResources);
132 | 
133 |   return {
134 |     messages: [
135 |       searchResultsToolMessage,
136 |       aiMessageResponse,
137 |       new ToolMessage({
138 |         tool_call_id: aiMessageResponse.tool_calls![0]["id"]!,
139 |         content: \`Resources added.\`,
140 |         name: "ExtractResources",
141 |       }),
142 |     ],
143 |     resources,
144 |     logs,
145 |   };
146 | }
147 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/src/state.ts:
--------------------------------------------------------------------------------
 1 | import { Annotation } from "@langchain/langgraph";
 2 | import { CopilotKitStateAnnotation } from "@copilotkit/sdk-js/langgraph";
 3 | 
 4 | // Define a Resource annotation with properties for URL, title, and description
 5 | const ResourceAnnotation = Annotation.Root({
 6 |   url: Annotation<string>,
 7 |   title: Annotation<string>,
 8 |   description: Annotation<string>,
 9 |   content: Annotation<string>,
10 | });
11 | 
12 | // Define a Log annotation with properties for message and done status
13 | const LogAnnotation = Annotation.Root({
14 |   message: Annotation<string>,
15 |   done: Annotation<boolean>,
16 | });
17 | 
18 | // Define the AgentState annotation, extending MessagesState
19 | export const AgentStateAnnotation = Annotation.Root({
20 |   model: Annotation<string>,
21 |   research_question: Annotation<string>,
22 |   report: Annotation<string>,
23 |   resources: Annotation<(typeof ResourceAnnotation.State)[]>,
24 |   logs: Annotation<(typeof LogAnnotation.State)[]>,
25 |   ...CopilotKitStateAnnotation.spec,
26 | });
27 | 
28 | export type AgentState = typeof AgentStateAnnotation.State;
29 | export type Resource = typeof ResourceAnnotation.State;
30 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent-js/tsconfig.json:
--------------------------------------------------------------------------------
  1 | {
  2 |   "compilerOptions": {
  3 |     /* Visit https://aka.ms/tsconfig to read more about this file */
  4 | 
  5 |     /* Projects */
  6 |     // "incremental": true,                              /* Save .tsbuildinfo files to allow for incremental compilation of projects. */
  7 |     // "composite": true,                                /* Enable constraints that allow a TypeScript project to be used with project references. */
  8 |     // "tsBuildInfoFile": "./.tsbuildinfo",              /* Specify the path to .tsbuildinfo incremental compilation file. */
  9 |     // "disableSourceOfProjectReferenceRedirect": true,  /* Disable preferring source files instead of declaration files when referencing composite projects. */
 10 |     // "disableSolutionSearching": true,                 /* Opt a project out of multi-project reference checking when editing. */
 11 |     // "disableReferencedProjectLoad": true,             /* Reduce the number of projects loaded automatically by TypeScript. */
 12 | 
 13 |     /* Language and Environment */
 14 |     "target": "es2016",                                  /* Set the JavaScript language version for emitted JavaScript and include compatible library declarations. */
 15 |     // "lib": [],                                        /* Specify a set of bundled library declaration files that describe the target runtime environment. */
 16 |     // "jsx": "preserve",                                /* Specify what JSX code is generated. */
 17 |     // "experimentalDecorators": true,                   /* Enable experimental support for legacy experimental decorators. */
 18 |     // "emitDecoratorMetadata": true,                    /* Emit design-type metadata for decorated declarations in source files. */
 19 |     // "jsxFactory": "",                                 /* Specify the JSX factory function used when targeting React JSX emit, e.g. 'React.createElement' or 'h'. */
 20 |     // "jsxFragmentFactory": "",                         /* Specify the JSX Fragment reference used for fragments when targeting React JSX emit e.g. 'React.Fragment' or 'Fragment'. */
 21 |     // "jsxImportSource": "",                            /* Specify module specifier used to import the JSX factory functions when using 'jsx: react-jsx*'. */
 22 |     // "reactNamespace": "",                             /* Specify the object invoked for 'createElement'. This only applies when targeting 'react' JSX emit. */
 23 |     // "noLib": true,                                    /* Disable including any library files, including the default lib.d.ts. */
 24 |     // "useDefineForClassFields": true,                  /* Emit ECMAScript-standard-compliant class fields. */
 25 |     // "moduleDetection": "auto",                        /* Control what method is used to detect module-format JS files. */
 26 | 
 27 |     /* Modules */
 28 |     "module": "commonjs",                                /* Specify what module code is generated. */
 29 |     // "rootDir": "./",                                  /* Specify the root folder within your source files. */
 30 |     // "moduleResolution": "node10",                     /* Specify how TypeScript looks up a file from a given module specifier. */
 31 |     // "baseUrl": "./",                                  /* Specify the base directory to resolve non-relative module names. */
 32 |     // "paths": {},                                      /* Specify a set of entries that re-map imports to additional lookup locations. */
 33 |     // "rootDirs": [],                                   /* Allow multiple folders to be treated as one when resolving modules. */
 34 |     // "typeRoots": [],                                  /* Specify multiple folders that act like './node_modules/@types'. */
 35 |     // "types": [],                                      /* Specify type package names to be included without being referenced in a source file. */
 36 |     // "allowUmdGlobalAccess": true,                     /* Allow accessing UMD globals from modules. */
 37 |     // "moduleSuffixes": [],                             /* List of file name suffixes to search when resolving a module. */
 38 |     // "allowImportingTsExtensions": true,               /* Allow imports to include TypeScript file extensions. Requires '--moduleResolution bundler' and either '--noEmit' or '--emitDeclarationOnly' to be set. */
 39 |     // "resolvePackageJsonExports": true,                /* Use the package.json 'exports' field when resolving package imports. */
 40 |     // "resolvePackageJsonImports": true,                /* Use the package.json 'imports' field when resolving imports. */
 41 |     // "customConditions": [],                           /* Conditions to set in addition to the resolver-specific defaults when resolving imports. */
 42 |     // "noUncheckedSideEffectImports": true,             /* Check side effect imports. */
 43 |     // "resolveJsonModule": true,                        /* Enable importing .json files. */
 44 |     // "allowArbitraryExtensions": true,                 /* Enable importing files with any extension, provided a declaration file is present. */
 45 |     // "noResolve": true,                                /* Disallow 'import's, 'require's or '<reference>'s from expanding the number of files TypeScript should add to a project. */
 46 | 
 47 |     /* JavaScript Support */
 48 |     // "allowJs": true,                                  /* Allow JavaScript files to be a part of your program. Use the 'checkJS' option to get errors from these files. */
 49 |     // "checkJs": true,                                  /* Enable error reporting in type-checked JavaScript files. */
 50 |     // "maxNodeModuleJsDepth": 1,                        /* Specify the maximum folder depth used for checking JavaScript files from 'node_modules'. Only applicable with 'allowJs'. */
 51 | 
 52 |     /* Emit */
 53 |     // "declaration": true,                              /* Generate .d.ts files from TypeScript and JavaScript files in your project. */
 54 |     // "declarationMap": true,                           /* Create sourcemaps for d.ts files. */
 55 |     // "emitDeclarationOnly": true,                      /* Only output d.ts files and not JavaScript files. */
 56 |     // "sourceMap": true,                                /* Create source map files for emitted JavaScript files. */
 57 |     // "inlineSourceMap": true,                          /* Include sourcemap files inside the emitted JavaScript. */
 58 |     // "noEmit": true,                                   /* Disable emitting files from a compilation. */
 59 |     // "outFile": "./",                                  /* Specify a file that bundles all outputs into one JavaScript file. If 'declaration' is true, also designates a file that bundles all .d.ts output. */
 60 |     // "outDir": "./",                                   /* Specify an output folder for all emitted files. */
 61 |     // "removeComments": true,                           /* Disable emitting comments. */
 62 |     // "importHelpers": true,                            /* Allow importing helper functions from tslib once per project, instead of including them per-file. */
 63 |     // "downlevelIteration": true,                       /* Emit more compliant, but verbose and less performant JavaScript for iteration. */
 64 |     // "sourceRoot": "",                                 /* Specify the root path for debuggers to find the reference source code. */
 65 |     // "mapRoot": "",                                    /* Specify the location where debugger should locate map files instead of generated locations. */
 66 |     // "inlineSources": true,                            /* Include source code in the sourcemaps inside the emitted JavaScript. */
 67 |     // "emitBOM": true,                                  /* Emit a UTF-8 Byte Order Mark (BOM) in the beginning of output files. */
 68 |     // "newLine": "crlf",                                /* Set the newline character for emitting files. */
 69 |     // "stripInternal": true,                            /* Disable emitting declarations that have '@internal' in their JSDoc comments. */
 70 |     // "noEmitHelpers": true,                            /* Disable generating custom helper functions like '__extends' in compiled output. */
 71 |     // "noEmitOnError": true,                            /* Disable emitting files if any type checking errors are reported. */
 72 |     // "preserveConstEnums": true,                       /* Disable erasing 'const enum' declarations in generated code. */
 73 |     // "declarationDir": "./",                           /* Specify the output directory for generated declaration files. */
 74 | 
 75 |     /* Interop Constraints */
 76 |     // "isolatedModules": true,                          /* Ensure that each file can be safely transpiled without relying on other imports. */
 77 |     // "verbatimModuleSyntax": true,                     /* Do not transform or elide any imports or exports not marked as type-only, ensuring they are written in the output file's format based on the 'module' setting. */
 78 |     // "isolatedDeclarations": true,                     /* Require sufficient annotation on exports so other tools can trivially generate declaration files. */
 79 |     // "allowSyntheticDefaultImports": true,             /* Allow 'import x from y' when a module doesn't have a default export. */
 80 |     "esModuleInterop": true,                             /* Emit additional JavaScript to ease support for importing CommonJS modules. This enables 'allowSyntheticDefaultImports' for type compatibility. */
 81 |     // "preserveSymlinks": true,                         /* Disable resolving symlinks to their realpath. This correlates to the same flag in node. */
 82 |     "forceConsistentCasingInFileNames": true,            /* Ensure that casing is correct in imports. */
 83 | 
 84 |     /* Type Checking */
 85 |     "strict": true,                                      /* Enable all strict type-checking options. */
 86 |     // "noImplicitAny": true,                            /* Enable error reporting for expressions and declarations with an implied 'any' type. */
 87 |     // "strictNullChecks": true,                         /* When type checking, take into account 'null' and 'undefined'. */
 88 |     // "strictFunctionTypes": true,                      /* When assigning functions, check to ensure parameters and the return values are subtype-compatible. */
 89 |     // "strictBindCallApply": true,                      /* Check that the arguments for 'bind', 'call', and 'apply' methods match the original function. */
 90 |     // "strictPropertyInitialization": true,             /* Check for class properties that are declared but not set in the constructor. */
 91 |     // "strictBuiltinIteratorReturn": true,              /* Built-in iterators are instantiated with a 'TReturn' type of 'undefined' instead of 'any'. */
 92 |     // "noImplicitThis": true,                           /* Enable error reporting when 'this' is given the type 'any'. */
 93 |     // "useUnknownInCatchVariables": true,               /* Default catch clause variables as 'unknown' instead of 'any'. */
 94 |     // "alwaysStrict": true,                             /* Ensure 'use strict' is always emitted. */
 95 |     // "noUnusedLocals": true,                           /* Enable error reporting when local variables aren't read. */
 96 |     // "noUnusedParameters": true,                       /* Raise an error when a function parameter isn't read. */
 97 |     // "exactOptionalPropertyTypes": true,               /* Interpret optional property types as written, rather than adding 'undefined'. */
 98 |     // "noImplicitReturns": true,                        /* Enable error reporting for codepaths that do not explicitly return in a function. */
 99 |     // "noFallthroughCasesInSwitch": true,               /* Enable error reporting for fallthrough cases in switch statements. */
100 |     // "noUncheckedIndexedAccess": true,                 /* Add 'undefined' to a type when accessed using an index. */
101 |     // "noImplicitOverride": true,                       /* Ensure overriding members in derived classes are marked with an override modifier. */
102 |     // "noPropertyAccessFromIndexSignature": true,       /* Enforces using indexed accessors for keys declared using an indexed type. */
103 |     // "allowUnusedLabels": true,                        /* Disable error reporting for unused labels. */
104 |     // "allowUnreachableCode": true,                     /* Disable error reporting for unreachable code. */
105 | 
106 |     /* Completeness */
107 |     // "skipDefaultLibCheck": true,                      /* Skip type checking .d.ts files that are included with TypeScript. */
108 |     "skipLibCheck": true                                 /* Skip type checking all .d.ts files. */
109 |   }
110 | }
111 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/.gitignore:
--------------------------------------------------------------------------------
1 | venv/
2 | __pycache__/
3 | *.pyc
4 | .env
5 | .vercel
6 | .langgraph_api

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/.vscode/cspell.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "version": "0.2",
 3 |   "language": "en",
 4 |   "words": [
 5 |     "langgraph",
 6 |     "langchain",
 7 |     "perplexity",
 8 |     "openai",
 9 |     "ainvoke",
10 |     "pydantic",
11 |     "tavily",
12 |     "copilotkit",
13 |     "fastapi",
14 |     "uvicorn",
15 |     "checkpointer",
16 |     "aiohttp",
17 |     "dotenv",
18 |     "khtml"
19 |   ]
20 | }
21 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/.vscode/settings.json:
--------------------------------------------------------------------------------
1 | {
2 |   "python.analysis.typeCheckingMode": "basic"
3 | }
4 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/langgraph.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "python_version": "3.12",
 3 |   "dockerfile_lines": [],
 4 |   "dependencies": ["."],
 5 |   "graphs": {
 6 |     "research_agent": "./research_canvas/langgraph/agent.py:graph"
 7 |   },
 8 |   "env": ".env"
 9 | }
10 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/pyproject.toml:
--------------------------------------------------------------------------------
 1 | [tool.poetry]
 2 | name = "research_canvas"
 3 | version = "0.1.0"
 4 | description = "Research Canvas"
 5 | authors = ["Markus Ecker <markus.ecker@gmail.com>"]
 6 | license = "MIT"
 7 | 
 8 | [project]
 9 | name = "research_canvas"
10 | version = "0.0.1"
11 | dependencies = [
12 |     "copilotkit[crewai]>=0.1.41",
13 |     "langchain-openai>=0.2.3",
14 |     "langchain-community>=0.3.1",
15 |     "langchain-anthropic>=0.3.1",
16 |     "langchain-google-genai>=2.0.5",
17 |     "langchain>=0.3.4",
18 |     "openai>=1.52.1",
19 |     "tavily-python>=0.5.0",
20 |     "python-dotenv>=1.0.1",
21 |     "uvicorn>=0.31.0",
22 |     "requests>=2.32.3",
23 |     "html2text>=2024.2.26",
24 |     "langchain-core>=0.3.25",
25 |     "langgraph-cli[inmem]>=0.1.64",
26 |     "langgraph-checkpoint-sqlite>=2.0.1",
27 |     "aiosqlite>=0.20.0",
28 |     "aiohttp>=3.9.3"
29 | ]
30 | 
31 | [build-system]
32 | requires = ["setuptools >= 61.0"]
33 | build-backend = "setuptools.build_meta"
34 | 
35 | [tool.poetry.dependencies]
36 | python = ">=3.12,<3.13"
37 | copilotkit = {extras = ["crewai"], version = "^0.1.41"}
38 | langchain-openai = "0.2.3"
39 | langchain-community = "^0.3.1"
40 | langchain-anthropic = "0.3.1"
41 | langchain-google-genai = "2.0.5"
42 | langchain = "0.3.4"
43 | openai = "^1.52.1"
44 | tavily-python = "^0.5.0"
45 | python-dotenv = "^1.0.1"
46 | uvicorn = "^0.31.0"
47 | requests = "^2.32.3"
48 | html2text = "^2024.2.26"
49 | langchain-core = "^0.3.25"
50 | langgraph-cli = {extras = ["inmem"], version = "^0.1.64"}
51 | langgraph-checkpoint-sqlite = "^2.0.1"
52 | aiosqlite = "^0.20.0"
53 | aiohttp = "^3.9.3"
54 | 
55 | [tool.poetry.scripts]
56 | demo = "research_canvas.demo:main"
57 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/agent/research_canvas/__init__.py

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/agent/research_canvas/crewai/__init__.py

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/agent.py:
--------------------------------------------------------------------------------
 1 | """
 2 | This is the main entry point for the CrewAI agent.
 3 | """
 4 | from typing_extensions import Dict, Any, cast
 5 | from crewai.flow.flow import Flow, start, router, listen
 6 | from litellm import completion
 7 | from copilotkit.crewai import copilotkit_stream, copilotkit_predict_state
 8 | from research_canvas.crewai.download import download_resources, get_resources
 9 | from research_canvas.crewai.delete import maybe_perform_delete
10 | from research_canvas.crewai.prompt import format_prompt
11 | from research_canvas.crewai.tools import (
12 |     SEARCH_TOOL,
13 |     WRITE_REPORT_TOOL,
14 |     WRITE_RESEARCH_QUESTION_TOOL,
15 |     DELETE_RESOURCES_TOOL,
16 |     perform_tool_calls
17 | )
18 | 
19 | class ResearchCanvasFlow(Flow[Dict[str, Any]]):
20 |     """
21 |     Research Canvas CrewAI Flow
22 |     """
23 | 
24 |     @start()
25 |     @listen("route_follow_up")
26 |     async def start(self):
27 |         """
28 |         Download any pending assets that are needed for the research.
29 |         """
30 |         self.state["resources"] = self.state.get("resources", [])
31 |         self.state["research_question"] = self.state.get("research_question", "")
32 |         self.state["report"] = self.state.get("report", "")
33 | 
34 |         await download_resources(self.state)
35 | 
36 |         # If the user requested deletion, perform it
37 |         maybe_perform_delete(self.state)
38 | 
39 | 
40 | 
41 |     @router(start)
42 |     async def chat(self):
43 |         """
44 |         Listen for the download event.
45 |         """
46 |         resources = get_resources(self.state)
47 |         prompt = format_prompt(
48 |             self.state["research_question"],
49 |             self.state["report"],
50 |             resources
51 |         )
52 | 
53 |         await copilotkit_predict_state(
54 |           {
55 |             "report": {
56 |               "tool_name": "WriteReport",
57 |               "tool_argument": "report",
58 |             },
59 |             "research_question": {
60 |               "tool_name": "WriteResearchQuestion",
61 |               "tool_argument": "research_question",
62 |             },
63 |           }
64 |         )
65 | 
66 |         response = await copilotkit_stream(
67 |             completion(
68 |                 model="openai/gpt-4o",
69 |                 messages=[
70 |                     {"role": "system", "content": prompt},
71 |                     *self.state["messages"]
72 |                 ],
73 |                 tools=[
74 |                     SEARCH_TOOL,
75 |                     WRITE_REPORT_TOOL,
76 |                     WRITE_RESEARCH_QUESTION_TOOL,
77 |                     DELETE_RESOURCES_TOOL
78 |                 ],
79 | 
80 |                 parallel_tool_calls=False,
81 |                 stream=True
82 |             )
83 |         )
84 |         message = cast(Any, response).choices[0]["message"]
85 | 
86 |         self.state["messages"].append(message)
87 | 
88 |         follow_up = await perform_tool_calls(self.state)
89 | 
90 |         return "route_follow_up" if follow_up else "route_end"
91 | 
92 |     @listen("route_end")
93 |     async def end(self):
94 |         """
95 |         End the flow.
96 |         """
97 | 
98 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/delete.py:
--------------------------------------------------------------------------------
 1 | """
 2 | Delete Resources
 3 | """
 4 | 
 5 | import json
 6 | from typing_extensions import Dict, Any
 7 | 
 8 | def maybe_perform_delete(state: Dict[str, Any]):
 9 |     """
10 |     Maybe perform delete.
11 |     """
12 |     messages = state["messages"]
13 |     if len(messages) >= 2:
14 |         last_message = messages[-1]
15 |         prev_message = messages[-2]
16 |         if (prev_message.get("tool_calls") and
17 |             prev_message["tool_calls"][0]["function"].get("name") == "DeleteResources" and
18 |             last_message.get("content") == "YES"):
19 |             urls = json.loads(prev_message["tool_calls"][0]["function"]["arguments"])["urls"]
20 |             state["resources"] = [
21 |                 resource for resource in state["resources"] if resource["url"] not in urls
22 |             ]
23 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/demo.py:
--------------------------------------------------------------------------------
 1 | """Demo"""
 2 | 
 3 | import os
 4 | from dotenv import load_dotenv
 5 | load_dotenv()
 6 | 
 7 | # pylint: disable=wrong-import-position
 8 | from fastapi import FastAPI
 9 | import uvicorn
10 | from copilotkit.integrations.fastapi import add_fastapi_endpoint
11 | from copilotkit import CopilotKitRemoteEndpoint, CrewAIAgent
12 | from research_canvas.crewai.agent import ResearchCanvasFlow
13 | 
14 | app = FastAPI()
15 | sdk = CopilotKitRemoteEndpoint(
16 |     agents=[
17 |         CrewAIAgent(
18 |             name="research_agent_crewai",
19 |             description="Research agent using CrewAI.",
20 |             flow=ResearchCanvasFlow(),
21 |         ),
22 |     ],
23 | )
24 | 
25 | add_fastapi_endpoint(app, sdk, "/copilotkit")
26 | 
27 | # add new route for health check
28 | @app.get("/health")
29 | def health():
30 |     """Health check."""
31 |     return {"status": "ok"}
32 | 
33 | 
34 | def main():
35 |     """Run the uvicorn server."""
36 |     port = int(os.getenv("PORT", "8000"))
37 |     uvicorn.run(
38 |         "research_canvas.crewai.demo:app",
39 |         host="0.0.0.0",
40 |         port=port,
41 |         reload=True,
42 |         reload_dirs=(
43 |             ["."] +
44 |             (["../../../../sdk-python/copilotkit"]
45 |              if os.path.exists("../../../../sdk-python/copilotkit")
46 |              else []
47 |              )
48 |         )
49 |     )
50 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/download.py:
--------------------------------------------------------------------------------
 1 | """
 2 | Utility functions for downloading resources.
 3 | """
 4 | import aiohttp
 5 | import html2text
 6 | from typing_extensions import Dict, Any
 7 | from copilotkit.crewai import copilotkit_emit_state
 8 | from research_canvas.crewai.tools import prepare_state_for_serialization
 9 | 
10 | _RESOURCE_CACHE = {}
11 | 
12 | def get_resource(url: str):
13 |     """
14 |     Get a resource from the cache.
15 |     """
16 |     return _RESOURCE_CACHE.get(url, "")
17 | 
18 | _USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" # pylint: disable=line-too-long
19 | 
20 | async def _download_resource(url: str):
21 |     """
22 |     Download a resource from the internet asynchronously.
23 |     """
24 |     try:
25 |         async with aiohttp.ClientSession() as session:
26 |             async with session.get(
27 |                 url,
28 |                 headers={"User-Agent": _USER_AGENT},
29 |                 timeout=aiohttp.ClientTimeout(total=10)
30 |             ) as response:
31 |                 response.raise_for_status()
32 |                 html_content = await response.text()
33 |                 markdown_content = html2text.html2text(html_content)
34 |                 _RESOURCE_CACHE[url] = markdown_content
35 |                 return markdown_content
36 |     except Exception as e: # pylint: disable=broad-except
37 |         _RESOURCE_CACHE[url] = "ERROR"
38 |         return f"Error downloading resource: {e}"
39 | 
40 | 
41 | async def download_resources(state: Dict[str, Any]):
42 |     """
43 |     Download resources from the internet.
44 |     """
45 |     state["resources"] = state.get("resources", [])
46 |     state["logs"] = state.get("logs", [])
47 |     resources_to_download = []
48 | 
49 |     logs_offset = len(state["logs"])
50 | 
51 |     # Find resources that are not downloaded
52 |     for resource in state["resources"]:
53 |         if not get_resource(resource["url"]):
54 |             resources_to_download.append(resource)
55 |             state["logs"].append({
56 |                 "message": f"Downloading {resource['url']}",
57 |                 "done": False
58 |             })
59 | 
60 |     # Prepare serializable state and emit to let the UI update
61 |     serializable_state = prepare_state_for_serialization(state)
62 |     await copilotkit_emit_state(serializable_state)
63 | 
64 |     # Download the resources
65 |     for i, resource in enumerate(resources_to_download):
66 |         await _download_resource(resource["url"])
67 |         state["logs"][logs_offset + i]["done"] = True
68 | 
69 |         # Prepare serializable state and update UI
70 |         serializable_state = prepare_state_for_serialization(state)
71 |         await copilotkit_emit_state(serializable_state)
72 | 
73 | def get_resources(state: Dict[str, Any]):
74 |     """
75 |     Get the resources from the state.
76 |     """
77 |     resources = []
78 | 
79 |     for resource in state["resources"]:
80 |         content = get_resource(resource["url"])
81 |         if content == "ERROR":
82 |             continue
83 |         resources.append({
84 |             **resource,
85 |             "content": content
86 |         })
87 | 
88 |     return resources
89 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/prompt.py:
--------------------------------------------------------------------------------
 1 | """
 2 | Prompt
 3 | """
 4 | 
 5 | from typing_extensions import Dict, Any, List
 6 | 
 7 | def format_prompt(
 8 |     research_question: str,
 9 |     report: str,
10 |     resources: List[Dict[str, Any]]
11 | ):
12 |     """
13 |     Format the main prompt.
14 |     """
15 | 
16 |     return f"""
17 |         You are a research assistant. You help the user with writing a research report.
18 |         Do not recite the resources, instead use them to answer the user's question.
19 |         You should use the search tool to get resources before answering the user's question.
20 |         If you finished writing the report, ask the user proactively for next steps, changes etc, make it engaging.
21 |         To write the report, you should use the WriteReport tool. Never EVER respond with the report, only use the tool.
22 |         If a research question is provided, YOU MUST NOT ASK FOR IT AGAIN.
23 | 
24 |         This is the research question:
25 |         {research_question}
26 | 
27 |         This is the research report:
28 |         {report}
29 | 
30 |         Here are the resources that you have available:
31 |         {resources}
32 |     """

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/crewai/tools.py:
--------------------------------------------------------------------------------
  1 | """
  2 | Tools
  3 | """
  4 | import os
  5 | import json
  6 | from typing_extensions import Dict, Any, List, cast
  7 | from tavily import TavilyClient
  8 | from copilotkit.crewai import copilotkit_emit_state, copilotkit_predict_state, copilotkit_stream
  9 | from litellm import completion
 10 | from litellm.types.utils import Message as LiteLLMMessage, ChatCompletionMessageToolCall
 11 | 
 12 | HITL_TOOLS = ["DeleteResources"]
 13 | 
 14 | tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
 15 | 
 16 | # Custom JSON encoder to handle Message objects
 17 | class MessageEncoder(json.JSONEncoder):
 18 |     def default(self, obj):
 19 |         if isinstance(obj, LiteLLMMessage) or (hasattr(obj, "__class__") and obj.__class__.__name__ == "Message"):
 20 |             # Convert Message object to a serializable dictionary
 21 |             return {
 22 |                 'role': getattr(obj, 'role', ''),
 23 |                 'content': getattr(obj, 'content', ''),
 24 |                 'tool_calls': getattr(obj, 'tool_calls', []),
 25 |                 'tool_call_id': getattr(obj, 'tool_call_id', None)
 26 |             }
 27 |         elif isinstance(obj, ChatCompletionMessageToolCall) or (hasattr(obj, "__class__") and obj.__class__.__name__ == "ChatCompletionMessageToolCall"):
 28 |             # Convert ChatCompletionMessageToolCall to a serializable dictionary
 29 |             return {
 30 |                 'id': getattr(obj, 'id', ''),
 31 |                 'type': getattr(obj, 'type', ''),
 32 |                 'function': {
 33 |                     'name': getattr(obj.function, 'name', '') if hasattr(obj, 'function') else '',
 34 |                     'arguments': getattr(obj.function, 'arguments', '') if hasattr(obj, 'function') else ''
 35 |                 }
 36 |             }
 37 |         return super().default(obj)
 38 | 
 39 | # Helper function to prepare state for JSON serialization
 40 | def prepare_state_for_serialization(state):
 41 |     """
 42 |     Recursively convert non-serializable objects in state to serializable dictionaries.
 43 |     """
 44 |     if isinstance(state, dict):
 45 |         # Handle dictionary
 46 |         result = {}
 47 |         for key, value in state.items():
 48 |             result[key] = prepare_state_for_serialization(value)
 49 |         return result
 50 |     elif isinstance(state, list):
 51 |         # Handle list
 52 |         return [prepare_state_for_serialization(item) for item in state]
 53 |     elif isinstance(state, (str, int, float, bool, type(None))):
 54 |         # Base primitive types
 55 |         return state
 56 |     elif isinstance(state, LiteLLMMessage) or (hasattr(state, "__class__") and state.__class__.__name__ == "Message"):
 57 |         # Handle Message objects
 58 |         return {
 59 |             'role': getattr(state, 'role', ''),
 60 |             'content': getattr(state, 'content', ''),
 61 |             'tool_calls': prepare_state_for_serialization(getattr(state, 'tool_calls', [])),
 62 |             'tool_call_id': getattr(state, 'tool_call_id', None)
 63 |         }
 64 |     elif isinstance(state, ChatCompletionMessageToolCall) or (hasattr(state, "__class__") and state.__class__.__name__ == "ChatCompletionMessageToolCall"):
 65 |         # Handle ChatCompletionMessageToolCall objects
 66 |         function_data = {}
 67 |         if hasattr(state, 'function'):
 68 |             function_data = {
 69 |                 'name': getattr(state.function, 'name', ''),
 70 |                 'arguments': getattr(state.function, 'arguments', '')
 71 |             }
 72 |         
 73 |         return {
 74 |             'id': getattr(state, 'id', ''),
 75 |             'type': getattr(state, 'type', ''),
 76 |             'function': function_data
 77 |         }
 78 |     else:
 79 |         # Try to convert other objects to dict if possible
 80 |         try:
 81 |             # Try to convert to dict using __dict__
 82 |             if hasattr(state, '__dict__'):
 83 |                 return prepare_state_for_serialization(state.__dict__)
 84 |             # Try to use model_dump for pydantic models
 85 |             elif hasattr(state, 'model_dump'):
 86 |                 return prepare_state_for_serialization(state.model_dump())
 87 |             # If object has a to_dict method
 88 |             elif hasattr(state, 'to_dict') and callable(getattr(state, 'to_dict')):
 89 |                 return prepare_state_for_serialization(state.to_dict())
 90 |             # Last resort: try to convert using vars()
 91 |             else:
 92 |                 return prepare_state_for_serialization(vars(state))
 93 |         except:
 94 |             # If all else fails, convert to string
 95 |             return str(state)
 96 | 
 97 | async def perform_tool_calls(state: Dict[str, Any]):
 98 |     """
 99 |     Perform tool calls on the state.
100 |     """
101 |     if len(state["messages"]) == 0:
102 |         return False
103 |     message = state["messages"][-1]
104 | 
105 |     if not message.get("tool_calls"):
106 |         return False
107 | 
108 |     tool_call = message["tool_calls"][0]
109 |     tool_call_id = tool_call["id"]
110 |     tool_call_name = tool_call["function"]["name"]
111 |     tool_call_args = json.loads(tool_call["function"]["arguments"])
112 | 
113 |     if tool_call_name in HITL_TOOLS:
114 |         return False
115 | 
116 |     if tool_call_name == "Search":
117 |         queries = tool_call_args.get("queries", [])
118 |         await perform_search(state, queries, tool_call_id)
119 | 
120 |     elif tool_call_name == "WriteReport":
121 |         state["report"] = tool_call_args.get("report", "")
122 |         state["messages"].append({
123 |             "role": "tool",
124 |             "content": "Report written.",
125 |             "tool_call_id": tool_call_id
126 |         })
127 | 
128 |     elif tool_call_name == "WriteResearchQuestion":
129 |         state["research_question"] = tool_call_args.get("research_question", "")
130 |         state["messages"].append({
131 |             "role": "tool",
132 |             "content": "Research question written.",
133 |             "tool_call_id": tool_call_id
134 |         })
135 | 
136 |     return True
137 | 
138 | async def perform_search(state: Dict[str, Any], queries: List[str], tool_call_id: str):
139 |     """
140 |     Perform a search.
141 |     """
142 |     state["resources"] = state.get("resources", [])
143 |     state["logs"] = state.get("logs", [])
144 | 
145 |     for query in queries:
146 |         state["logs"].append({
147 |             "message": f"Search for {query}",
148 |             "done": False
149 |         })
150 | 
151 |     # Use the prepared state for serialization
152 |     serializable_state = prepare_state_for_serialization(state)
153 |     await copilotkit_emit_state(serializable_state)
154 | 
155 |     search_results = []
156 | 
157 |     for i, query in enumerate(queries):
158 |         response = tavily_client.search(query)
159 |         search_results.append(response)
160 |         state["logs"][i]["done"] = True
161 |         # Use the prepared state for serialization
162 |         serializable_state = prepare_state_for_serialization(state)
163 |         await copilotkit_emit_state(serializable_state)
164 | 
165 |     await copilotkit_predict_state(
166 |         {
167 |             "resources": {
168 |                 "tool_name": "ExtractResources",
169 |                 "tool_argument": "resources",
170 |             },
171 |         }
172 |     )
173 | 
174 |     response = await copilotkit_stream(
175 |         completion(
176 |             model="openai/gpt-4o",
177 |             messages=[
178 |                 {
179 |                     "role": "system", 
180 |                     "content": "You need to extract the 3-5 most relevant resources from the following search results."
181 |                 },
182 |                 *state["messages"],
183 |                 {
184 |                     "role": "tool",
185 |                     "content": f"Performed search: {search_results}",
186 |                     "tool_call_id": tool_call_id
187 |                 }
188 |             ],
189 |             tools=[EXTRACT_RESOURCES_TOOL],
190 |             tool_choice="required",
191 |             parallel_tool_calls=False,
192 |             stream=True
193 |         )
194 |     )
195 | 
196 |     state["logs"] = []
197 |     # Use the prepared state for serialization
198 |     serializable_state = prepare_state_for_serialization(state)
199 |     await copilotkit_emit_state(serializable_state)
200 | 
201 |     message = cast(Any, response).choices[0]["message"]
202 |     resources = json.loads(message["tool_calls"][0]["function"]["arguments"])["resources"]
203 | 
204 |     state["resources"].extend(resources)
205 | 
206 |     state["messages"].append({
207 |         "role": "tool",
208 |         "content": f"Added the following resources: {resources}",
209 |         "tool_call_id": tool_call_id
210 |     })
211 | 
212 | EXTRACT_RESOURCES_TOOL = {
213 |     "type": "function",
214 |     "function": {
215 |         "name": "ExtractResources",
216 |         "description": "Extract the 3-5 most relevant resources from a search result.",
217 |         "parameters": {
218 |             "type": "object",
219 |             "properties": {
220 |                 "resources": {
221 |                     "type": "array",
222 |                     "items": {
223 |                         "type": "object",
224 |                         "properties": {
225 |                             "url": {
226 |                                 "type": "string",
227 |                                 "description": "The URL of the resource"
228 |                             },
229 |                             "title": {
230 |                                 "type": "string",
231 |                                 "description": "The title of the resource"
232 |                             },
233 |                             "description": {
234 |                                 "type": "string",
235 |                                 "description": "A short description of the resource"
236 |                             }
237 |                         },
238 |                         "required": ["url", "title", "description"]
239 |                     },
240 |                     "description": "The list of resources"
241 |                 },
242 |             },
243 |             "required": ["resources"]
244 |         },
245 |     },
246 | }
247 | 
248 | 
249 | SEARCH_TOOL = {
250 |     "type": "function",
251 |     "function": {
252 |         "name": "Search",
253 |         "description": "Provide a list of one or more search queries to find good resources for the research.",
254 |         "parameters": {
255 |             "type": "object",
256 |             "properties": {
257 |                 "queries": {
258 |                     "type": "array",
259 |                     "items": {
260 |                         "type": "string"
261 |                     },
262 |                     "description": "The list of search queries",
263 |                 },
264 |             },
265 |             "required": ["queries"],
266 |         },
267 |     },
268 | }
269 | 
270 | WRITE_REPORT_TOOL = {
271 |     "type": "function",
272 |     "function": {
273 |         "name": "WriteReport",
274 |         "description": "Write the research report.",
275 |         "parameters": {
276 |             "type": "object",
277 |             "properties": {
278 |                 "report": {
279 |                     "type": "string",
280 |                     "description": "The research report.",
281 |                 },
282 |             },
283 |             "required": ["report"],
284 |         },
285 |     },
286 | }
287 | 
288 | WRITE_RESEARCH_QUESTION_TOOL = {
289 |     "type": "function",
290 |     "function": {
291 |         "name": "WriteResearchQuestion",
292 |         "description": "Write the research question.",
293 |         "parameters": {
294 |             "type": "object",
295 |             "properties": {
296 |                 "research_question": {
297 |                     "type": "string",
298 |                     "description": "The research question.",
299 |                 },
300 |             },
301 |             "required": ["research_question"],
302 |         },
303 |     },
304 | }
305 | 
306 | DELETE_RESOURCES_TOOL = {
307 |     "type": "function",
308 |     "function": {
309 |         "name": "DeleteResources",
310 |         "description": "Delete the URLs from the resources.",
311 |         "parameters": {
312 |             "type": "object",
313 |             "properties": {
314 |                 "urls": {
315 |                     "type": "array",
316 |                     "items": {
317 |                         "type": "string"
318 |                     },
319 |                     "description": "The URLs to delete.",
320 |                 },
321 |             },
322 |             "required": ["urls"],
323 |         },
324 |     },
325 | }
326 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/demo.py:
--------------------------------------------------------------------------------
 1 | """Demo"""
 2 | 
 3 | import os
 4 | from dotenv import load_dotenv
 5 | load_dotenv()
 6 | 
 7 | # pylint: disable=wrong-import-position
 8 | from fastapi import FastAPI
 9 | import uvicorn
10 | from copilotkit.integrations.fastapi import add_fastapi_endpoint
11 | from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
12 | from copilotkit.crewai import CrewAIAgent
13 | from research_canvas.crewai.agent import ResearchCanvasFlow
14 | from research_canvas.langgraph.agent import graph
15 | 
16 | # from contextlib import asynccontextmanager
17 | # from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
18 | # @asynccontextmanager
19 | # async def lifespan(fastapi_app: FastAPI):
20 | #     """Lifespan for the FastAPI app."""
21 | #     async with AsyncSqliteSaver.from_conn_string(
22 | #         ":memory:"
23 | #     ) as checkpointer:
24 | #         # Create an async graph
25 | #         graph = workflow.compile(checkpointer=checkpointer)
26 | 
27 | #         # Create SDK with the graph
28 | #         sdk = CopilotKitRemoteEndpoint(
29 | #             agents=[
30 | #                 LangGraphAgent(
31 | #                     name="research_agent",
32 | #                     description="Research agent.",
33 | #                     graph=graph,
34 | #                 ),
35 | #                 LangGraphAgent(
36 | #                     name="research_agent_google_genai",
37 | #                     description="Research agent.",
38 | #                     graph=graph
39 | #                 ),
40 | #             ],
41 | #         )
42 | 
43 | #         # Add the CopilotKit FastAPI endpoint
44 | #         add_fastapi_endpoint(fastapi_app, sdk, "/copilotkit")
45 | #         yield
46 | 
47 | # app = FastAPI(lifespan=lifespan)
48 | 
49 | 
50 | app = FastAPI()
51 | sdk = CopilotKitRemoteEndpoint(
52 |     agents=[
53 |         CrewAIAgent(
54 |             name="research_agent_crewai",
55 |             description="Research agent.",
56 |             flow=ResearchCanvasFlow(),
57 |         ),
58 |         LangGraphAgent(
59 |             name="research_agent",
60 |             description="Research agent.",
61 |             graph=graph,
62 |         ),
63 |          LangGraphAgent(
64 |             name="research_agent_google_genai",
65 |             description="Research agent.",
66 |             graph=graph
67 |         ),
68 |     ],
69 | )
70 | 
71 | add_fastapi_endpoint(app, sdk, "/copilotkit")
72 | 
73 | 
74 | @app.get("/health")
75 | def health():
76 |     """Health check."""
77 |     return {"status": "ok"}
78 | 
79 | 
80 | def main():
81 |     """Run the uvicorn server."""
82 |     port = int(os.getenv("PORT", "8000"))
83 |     uvicorn.run(
84 |         "research_canvas.demo:app",
85 |         host="0.0.0.0",
86 |         port=port,
87 |         reload=True,
88 |         reload_dirs=(
89 |             ["."] +
90 |             (["../../../sdk-python/copilotkit"]
91 |              if os.path.exists("../../../sdk-python/copilotkit")
92 |              else []
93 |              )
94 |         )
95 |     )
96 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/agent/research_canvas/langgraph/__init__.py

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/agent.py:
--------------------------------------------------------------------------------
 1 | """
 2 | This is the main entry point for the AI.
 3 | It defines the workflow graph and the entry point for the agent.
 4 | """
 5 | # pylint: disable=line-too-long, unused-import
 6 | import json
 7 | from typing import cast
 8 | 
 9 | from langchain_core.messages import AIMessage, ToolMessage
10 | from langgraph.graph import StateGraph, END
11 | from langgraph.checkpoint.memory import MemorySaver
12 | from research_canvas.langgraph.state import AgentState
13 | from research_canvas.langgraph.download import download_node
14 | from research_canvas.langgraph.chat import chat_node
15 | from research_canvas.langgraph.search import search_node
16 | from research_canvas.langgraph.delete import delete_node, perform_delete_node
17 | 
18 | # Define a new graph
19 | workflow = StateGraph(AgentState)
20 | workflow.add_node("download", download_node)
21 | workflow.add_node("chat_node", chat_node)
22 | workflow.add_node("search_node", search_node)
23 | workflow.add_node("delete_node", delete_node)
24 | workflow.add_node("perform_delete_node", perform_delete_node)
25 | 
26 | 
27 | memory = MemorySaver()
28 | workflow.set_entry_point("download")
29 | workflow.add_edge("download", "chat_node")
30 | workflow.add_edge("delete_node", "perform_delete_node")
31 | workflow.add_edge("perform_delete_node", "chat_node")
32 | workflow.add_edge("search_node", "download")
33 | graph = workflow.compile(checkpointer=memory, interrupt_after=["delete_node"])
34 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/chat.py:
--------------------------------------------------------------------------------
  1 | """Chat Node"""
  2 | 
  3 | from typing import List, cast, Literal
  4 | from langchain_core.runnables import RunnableConfig
  5 | from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
  6 | from langchain.tools import tool
  7 | from langgraph.types import Command
  8 | from copilotkit.langgraph import copilotkit_customize_config
  9 | from research_canvas.langgraph.state import AgentState
 10 | from research_canvas.langgraph.model import get_model
 11 | from research_canvas.langgraph.download import get_resource
 12 | 
 13 | 
 14 | @tool
 15 | def Search(queries: List[str]): # pylint: disable=invalid-name,unused-argument
 16 |     """A list of one or more search queries to find good resources to support the research."""
 17 | 
 18 | @tool
 19 | def WriteReport(report: str): # pylint: disable=invalid-name,unused-argument
 20 |     """Write the research report."""
 21 | 
 22 | @tool
 23 | def WriteResearchQuestion(research_question: str): # pylint: disable=invalid-name,unused-argument
 24 |     """Write the research question."""
 25 | 
 26 | @tool
 27 | def DeleteResources(urls: List[str]): # pylint: disable=invalid-name,unused-argument
 28 |     """Delete the URLs from the resources."""
 29 | 
 30 | 
 31 | async def chat_node(state: AgentState, config: RunnableConfig) -> \
 32 |     Command[Literal["search_node", "chat_node", "delete_node", "__end__"]]:
 33 |     """
 34 |     Chat Node
 35 |     """
 36 | 
 37 |     config = copilotkit_customize_config(
 38 |         config,
 39 |         emit_intermediate_state=[{
 40 |             "state_key": "report",
 41 |             "tool": "WriteReport",
 42 |             "tool_argument": "report",
 43 |         }, {
 44 |             "state_key": "research_question",
 45 |             "tool": "WriteResearchQuestion",
 46 |             "tool_argument": "research_question",
 47 |         }],
 48 |     )
 49 | 
 50 |     state["resources"] = state.get("resources", [])
 51 |     research_question = state.get("research_question", "")
 52 |     report = state.get("report", "")
 53 | 
 54 |     resources = []
 55 | 
 56 |     for resource in state["resources"]:
 57 |         content = get_resource(resource["url"])
 58 |         if content == "ERROR":
 59 |             continue
 60 |         resources.append({
 61 |             **resource,
 62 |             "content": content
 63 |         })
 64 | 
 65 |     model = get_model(state)
 66 |     # Prepare the kwargs for the ainvoke method
 67 |     ainvoke_kwargs = {}
 68 |     if model.__class__.__name__ in ["ChatOpenAI"]:
 69 |         ainvoke_kwargs["parallel_tool_calls"] = False
 70 | 
 71 |     response = await model.bind_tools(
 72 |         [
 73 |             Search,
 74 |             WriteReport,
 75 |             WriteResearchQuestion,
 76 |             DeleteResources,
 77 |         ],
 78 |         **ainvoke_kwargs  # Pass the kwargs conditionally
 79 |     ).ainvoke([
 80 |         SystemMessage(
 81 |             content=f"""
 82 |             You are a research assistant. You help the user with writing a research report.
 83 |             Do not recite the resources, instead use them to answer the user's question.
 84 |             You should use the search tool to get resources before answering the user's question.
 85 |             If you finished writing the report, ask the user proactively for next steps, changes etc, make it engaging.
 86 |             To write the report, you should use the WriteReport tool. Never EVER respond with the report, only use the tool.
 87 |             If a research question is provided, YOU MUST NOT ASK FOR IT AGAIN.
 88 | 
 89 |             This is the research question:
 90 |             {research_question}
 91 | 
 92 |             This is the research report:
 93 |             {report}
 94 | 
 95 |             Here are the resources that you have available:
 96 |             {resources}
 97 |             """
 98 |         ),
 99 |         *state["messages"],
100 |     ], config)
101 | 
102 |     ai_message = cast(AIMessage, response)
103 | 
104 |     if ai_message.tool_calls:
105 |         if ai_message.tool_calls[0]["name"] == "WriteReport":
106 |             report = ai_message.tool_calls[0]["args"].get("report", "")
107 |             return Command(
108 |                 goto="chat_node",
109 |                 update={
110 |                     "report": report,
111 |                     "messages": [ai_message, ToolMessage(
112 |                     tool_call_id=ai_message.tool_calls[0]["id"],
113 |                     content="Report written."
114 |                     )]
115 |                 }
116 |             )
117 |         if ai_message.tool_calls[0]["name"] == "WriteResearchQuestion":
118 |             return Command(
119 |                 goto="chat_node",
120 |                 update={
121 |                     "research_question": ai_message.tool_calls[0]["args"]["research_question"],
122 |                     "messages": [ai_message, ToolMessage(
123 |                         tool_call_id=ai_message.tool_calls[0]["id"],
124 |                         content="Research question written."
125 |                     )]
126 |                 }
127 |             )
128 |        
129 |     goto = "__end__"
130 |     if ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "Search":
131 |         goto = "search_node"
132 |     elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "DeleteResources":
133 |         goto = "delete_node"
134 | 
135 | 
136 |     return Command(
137 |         goto=goto,
138 |         update={
139 |             "messages": response
140 |         }
141 |     )
142 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/delete.py:
--------------------------------------------------------------------------------
 1 | """Delete Resources"""
 2 | 
 3 | import json
 4 | from typing import cast
 5 | from langchain_core.runnables import RunnableConfig
 6 | from langchain_core.messages import ToolMessage, AIMessage
 7 | from research_canvas.langgraph.state import AgentState
 8 | 
 9 | async def delete_node(state: AgentState, config: RunnableConfig): # pylint: disable=unused-argument
10 |     """
11 |     Delete Node
12 |     """
13 |     return state
14 | 
15 | async def perform_delete_node(state: AgentState, config: RunnableConfig): # pylint: disable=unused-argument
16 |     """
17 |     Perform Delete Node
18 |     """
19 |     ai_message = cast(AIMessage, state["messages"][-2])
20 |     tool_message = cast(ToolMessage, state["messages"][-1])
21 |     if tool_message.content == "YES":
22 |         if ai_message.tool_calls:
23 |             urls = ai_message.tool_calls[0]["args"]["urls"]
24 |         else:
25 |             parsed_tool_call = json.loads(ai_message.additional_kwargs["function_call"]["arguments"])
26 |             urls = parsed_tool_call["urls"]
27 | 
28 |         state["resources"] = [
29 |             resource for resource in state["resources"] if resource["url"] not in urls
30 |         ]
31 | 
32 |     return state
33 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/demo.py:
--------------------------------------------------------------------------------
 1 | """Demo"""
 2 | 
 3 | import os
 4 | # from contextlib import asynccontextmanager
 5 | from dotenv import load_dotenv
 6 | load_dotenv()
 7 | 
 8 | # pylint: disable=wrong-import-position
 9 | # from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
10 | from fastapi import FastAPI
11 | import uvicorn
12 | from copilotkit.integrations.fastapi import add_fastapi_endpoint
13 | from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
14 | from research_canvas.langgraph.agent import graph
15 | 
16 | 
17 | # @asynccontextmanager
18 | # async def lifespan(fastapi_app: FastAPI):
19 | #     """Lifespan for the FastAPI app."""
20 | #     async with AsyncSqliteSaver.from_conn_string(
21 | #         "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
22 | #     ) as checkpointer:
23 | #         # Create an async graph
24 | #         graph = workflow.compile(checkpointer=checkpointer)
25 | 
26 | #         # Create SDK with the graph
27 | #         sdk = CopilotKitRemoteEndpoint(
28 | #             agents=[
29 | #                 LangGraphAgent(
30 | #                     name="research_agent",
31 | #                     description="Research agent.",
32 | #                     graph=graph,
33 | #                 ),
34 | #                 LangGraphAgent(
35 | #                     name="research_agent_google_genai",
36 | #                     description="Research agent.",
37 | #                     graph=graph
38 | #                 ),
39 | #             ],
40 | #         )
41 | 
42 | #         # Add the CopilotKit FastAPI endpoint
43 | #         add_fastapi_endpoint(fastapi_app, sdk, "/copilotkit")
44 | #         yield
45 | 
46 | # app = FastAPI(lifespan=lifespan)
47 | 
48 | 
49 | app = FastAPI()
50 | sdk = CopilotKitRemoteEndpoint(
51 |     agents=[
52 |         LangGraphAgent(
53 |             name="research_agent",
54 |             description="Research agent.",
55 |             graph=graph,
56 |         ),
57 |         LangGraphAgent(
58 |             name="research_agent_google_genai",
59 |             description="Research agent.",
60 |             graph=graph
61 |         ),
62 |     ],
63 | )
64 | 
65 | add_fastapi_endpoint(app, sdk, "/copilotkit")
66 | 
67 | 
68 | 
69 | # add new route for health check
70 | @app.get("/health")
71 | def health():
72 |     """Health check."""
73 |     return {"status": "ok"}
74 | 
75 | def main():
76 |     """Run the uvicorn server."""
77 |     port = int(os.getenv("PORT", "8000"))
78 |     uvicorn.run(
79 |         "research_canvas.langgraph.demo:app",
80 |         host="0.0.0.0",
81 |         port=port,
82 |         reload=True,
83 |         reload_dirs=(
84 |             ["."] +
85 |             (["../../../../sdk-python/copilotkit"]
86 |              if os.path.exists("../../../../sdk-python/copilotkit")
87 |              else []
88 |              )
89 |         )
90 |     )
91 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/download.py:
--------------------------------------------------------------------------------
 1 | """
 2 | This module contains the implementation of the download_node function.
 3 | """
 4 | 
 5 | import aiohttp
 6 | import html2text
 7 | from copilotkit.langgraph import copilotkit_emit_state
 8 | from langchain_core.runnables import RunnableConfig
 9 | from research_canvas.langgraph.state import AgentState
10 | 
11 | _RESOURCE_CACHE = {}
12 | 
13 | def get_resource(url: str):
14 |     """
15 |     Get a resource from the cache.
16 |     """
17 |     return _RESOURCE_CACHE.get(url, "")
18 | 
19 | 
20 | _USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" # pylint: disable=line-too-long
21 | 
22 | async def _download_resource(url: str):
23 |     """
24 |     Download a resource from the internet asynchronously.
25 |     """
26 |     try:
27 |         async with aiohttp.ClientSession() as session:
28 |             async with session.get(
29 |                 url,
30 |                 headers={"User-Agent": _USER_AGENT},
31 |                 timeout=aiohttp.ClientTimeout(total=10)
32 |             ) as response:
33 |                 response.raise_for_status()
34 |                 html_content = await response.text()
35 |                 markdown_content = html2text.html2text(html_content)
36 |                 _RESOURCE_CACHE[url] = markdown_content
37 |                 return markdown_content
38 |     except Exception as e: # pylint: disable=broad-except
39 |         _RESOURCE_CACHE[url] = "ERROR"
40 |         return f"Error downloading resource: {e}"
41 | 
42 | async def download_node(state: AgentState, config: RunnableConfig):
43 |     """
44 |     Download resources from the internet.
45 |     """
46 |     state["resources"] = state.get("resources", [])
47 |     state["logs"] = state.get("logs", [])
48 |     resources_to_download = []
49 | 
50 |     logs_offset = len(state["logs"])
51 | 
52 |     # Find resources that are not downloaded
53 |     for resource in state["resources"]:
54 |         if not get_resource(resource["url"]):
55 |             resources_to_download.append(resource)
56 |             state["logs"].append({
57 |                 "message": f"Downloading {resource['url']}",
58 |                 "done": False
59 |             })
60 | 
61 |     # Emit the state to let the UI update
62 |     await copilotkit_emit_state(config, state)
63 | 
64 |     # Download the resources
65 |     for i, resource in enumerate(resources_to_download):
66 |         await _download_resource(resource["url"])
67 |         state["logs"][logs_offset + i]["done"] = True
68 | 
69 |         # update UI
70 |         await copilotkit_emit_state(config, state)
71 | 
72 |     return state
73 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/model.py:
--------------------------------------------------------------------------------
 1 | """
 2 | This module provides a function to get a model based on the configuration.
 3 | """
 4 | import os
 5 | from typing import cast, Any
 6 | from langchain_core.language_models.chat_models import BaseChatModel
 7 | from research_canvas.langgraph.state import AgentState
 8 | 
 9 | def get_model(state: AgentState) -> BaseChatModel:
10 |     """
11 |     Get a model based on the environment variable.
12 |     """
13 | 
14 |     state_model = state.get("model")
15 |     model = os.getenv("MODEL", state_model)
16 | 
17 |     print(f"Using model: {model}")
18 | 
19 |     if model == "openai":
20 |         from langchain_openai import ChatOpenAI
21 |         return ChatOpenAI(temperature=0, model="gpt-4o-mini")
22 |     if model == "anthropic":
23 |         from langchain_anthropic import ChatAnthropic
24 |         return ChatAnthropic(
25 |             temperature=0,
26 |             model_name="claude-3-5-sonnet-20240620",
27 |             timeout=None,
28 |             stop=None
29 |         )
30 |     if model == "google_genai":
31 |         from langchain_google_genai import ChatGoogleGenerativeAI
32 |         return ChatGoogleGenerativeAI(
33 |             temperature=0,
34 |             model="gemini-1.5-pro",
35 |             api_key=cast(Any, os.getenv("GOOGLE_API_KEY")) or None
36 |         )
37 | 
38 |     raise ValueError("Invalid model specified")
39 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/search.py:
--------------------------------------------------------------------------------
  1 | """
  2 | The search node is responsible for searching the internet for information.
  3 | """
  4 | 
  5 | import os
  6 | from typing import cast, List
  7 | from pydantic import BaseModel, Field
  8 | from langchain_core.runnables import RunnableConfig
  9 | from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
 10 | from langchain.tools import tool
 11 | from tavily import TavilyClient
 12 | from copilotkit.langgraph import copilotkit_emit_state, copilotkit_customize_config
 13 | from research_canvas.langgraph.state import AgentState
 14 | from research_canvas.langgraph.model import get_model
 15 | 
 16 | class ResourceInput(BaseModel):
 17 |     """A resource with a short description"""
 18 |     url: str = Field(description="The URL of the resource")
 19 |     title: str = Field(description="The title of the resource")
 20 |     description: str = Field(description="A short description of the resource")
 21 | 
 22 | @tool
 23 | def ExtractResources(resources: List[ResourceInput]): # pylint: disable=invalid-name,unused-argument
 24 |     """Extract the 3-5 most relevant resources from a search result."""
 25 | 
 26 | tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
 27 | 
 28 | async def search_node(state: AgentState, config: RunnableConfig):
 29 |     """
 30 |     The search node is responsible for searching the internet for resources.
 31 |     """
 32 | 
 33 |     ai_message = cast(AIMessage, state["messages"][-1])
 34 | 
 35 |     state["resources"] = state.get("resources", [])
 36 |     state["logs"] = state.get("logs", [])
 37 |     queries = ai_message.tool_calls[0]["args"]["queries"]
 38 | 
 39 |     for query in queries:
 40 |         state["logs"].append({
 41 |             "message": f"Search for {query}",
 42 |             "done": False
 43 |         })
 44 | 
 45 |     await copilotkit_emit_state(config, state)
 46 | 
 47 |     search_results = []
 48 | 
 49 |     for i, query in enumerate(queries):
 50 |         response = tavily_client.search(query)
 51 |         search_results.append(response)
 52 |         state["logs"][i]["done"] = True
 53 |         await copilotkit_emit_state(config, state)
 54 | 
 55 |     config = copilotkit_customize_config(
 56 |         config,
 57 |         emit_intermediate_state=[{
 58 |             "state_key": "resources",
 59 |             "tool": "ExtractResources",
 60 |             "tool_argument": "resources",
 61 |         }],
 62 |     )
 63 | 
 64 |     model = get_model(state)
 65 |     ainvoke_kwargs = {}
 66 |     if model.__class__.__name__ in ["ChatOpenAI"]:
 67 |         ainvoke_kwargs["parallel_tool_calls"] = False
 68 | 
 69 |     # figure out which resources to use
 70 |     response = await model.bind_tools(
 71 |         [ExtractResources],
 72 |         tool_choice="ExtractResources",
 73 |         **ainvoke_kwargs
 74 |     ).ainvoke([
 75 |         SystemMessage(
 76 |             content="""
 77 |             You need to extract the 3-5 most relevant resources from the following search results.
 78 |             """
 79 |         ),
 80 |         *state["messages"],
 81 |         ToolMessage(
 82 |         tool_call_id=ai_message.tool_calls[0]["id"],
 83 |         content=f"Performed search: {search_results}"
 84 |     )
 85 |     ], config)
 86 | 
 87 |     state["logs"] = []
 88 |     await copilotkit_emit_state(config, state)
 89 | 
 90 |     ai_message_response = cast(AIMessage, response)
 91 |     resources = ai_message_response.tool_calls[0]["args"]["resources"]
 92 | 
 93 |     state["resources"].extend(resources)
 94 | 
 95 |     state["messages"].append(ToolMessage(
 96 |         tool_call_id=ai_message.tool_calls[0]["id"],
 97 |         content=f"Added the following resources: {resources}"
 98 |     ))
 99 | 
100 |     return state
101 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/agent/research_canvas/langgraph/state.py:
--------------------------------------------------------------------------------
 1 | """
 2 | This is the state definition for the AI.
 3 | It defines the state of the agent and the state of the conversation.
 4 | """
 5 | 
 6 | from typing import List, TypedDict
 7 | from langgraph.graph import MessagesState
 8 | 
 9 | class Resource(TypedDict):
10 |     """
11 |     Represents a resource. Give it a good title and a short description.
12 |     """
13 |     url: str
14 |     title: str
15 |     description: str
16 | 
17 | class Log(TypedDict):
18 |     """
19 |     Represents a log of an action performed by the agent.
20 |     """
21 |     message: str
22 |     done: bool
23 | 
24 | class AgentState(MessagesState):
25 |     """
26 |     This is the state of the agent.
27 |     It is a subclass of the MessagesState class from langgraph.
28 |     """
29 |     model: str
30 |     research_question: str
31 |     report: str
32 |     resources: List[Resource]
33 |     logs: List[Log]
34 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/dockerize.sh:
--------------------------------------------------------------------------------
1 | docker build -t ${IMAGE_TAG} . --platform=linux/amd64 -f ./examples/Dockerfile.ui --build-arg APP_DIR=${APP_DIR} --push

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/readme.md:
--------------------------------------------------------------------------------
  1 | # CoAgents Research Canvas Example
  2 | 
  3 | This example demonstrates a research canvas UI.
  4 | 
  5 | **Live demo:** https://examples-coagents-research-canvas-ui.vercel.app/
  6 | 
  7 | Tutorial Video:
  8 | 
  9 | [![IMAGE ALT TEXT](http://img.youtube.com/vi/0b6BVqPwqA0/0.jpg)](http://www.youtube.com/watch?v=0b6BVqPwqA0 "Build Agent-Native Apps with LangGraph & CoAgents (tutorial)")
 10 | 
 11 | 
 12 | ---
 13 | 
 14 | ## Running the Agent
 15 | 
 16 | **These instructions assume you are in the \`coagents-research-canvas/\` directory**
 17 | 
 18 | ## Running the Agent
 19 | 
 20 | First, install the backend dependencies:
 21 | 
 22 | ### Python SDK
 23 | 
 24 | \`\`\`sh
 25 | cd agent-py
 26 | poetry install
 27 | \`\`\`
 28 | 
 29 | ### JS-SDK
 30 | 
 31 | \`\`\`sh
 32 | cd agent-js
 33 | pnpm install
 34 | \`\`\`
 35 | 
 36 | Then, create a \`.env\` file inside \`./agent-py\` or \`./agent-js\` with the following:
 37 | 
 38 | \`\`\`
 39 | OPENAI_API_KEY=...
 40 | TAVILY_API_KEY=...
 41 | LANGSMITH_API_KEY=...(JS ONLY)
 42 | \`\`\`
 43 | 
 44 | ⚠️ IMPORTANT:
 45 | Make sure the OpenAI API Key you provide, supports gpt-4o.
 46 | 
 47 | Then, run the demo:
 48 | 
 49 | ### Python
 50 | 
 51 | \`\`\`sh
 52 | poetry run demo
 53 | \`\`\`
 54 | 
 55 | ## Running the UI
 56 | 
 57 | First, install the dependencies:
 58 | 
 59 | \`\`\`sh
 60 | cd ./ui
 61 | pnpm i
 62 | \`\`\`
 63 | 
 64 | Then, create a \`.env\` file inside \`./ui\` with the following:
 65 | 
 66 | \`\`\`
 67 | OPENAI_API_KEY=...
 68 | \`\`\`
 69 | 
 70 | Then, run the Next.js project:
 71 | 
 72 | \`\`\`sh
 73 | pnpm run dev
 74 | \`\`\`
 75 | 
 76 | ⚠️ IMPORTANT:
 77 | If you're using the JS agent, follow the steps and uncomment the code inside the \`app/api/copilotkit/route.ts\`, \`remoteEndpoints\` action: 
 78 | 
 79 | \`\`\`ts
 80 | //const runtime = new CopilotRuntime({
 81 |  // remoteEndpoints: [
 82 |     // Uncomment this if you want to use LangGraph JS, make sure to
 83 |     // remove the remote action url below too.
 84 |     //
 85 |     // langGraphPlatformEndpoint({
 86 |     //   deploymentUrl: "http://localhost:8123",
 87 |     //   langsmithApiKey: process.env.LANGSMITH_API_KEY || "", // only used in LangGraph Platform deployments
 88 |     //   agents: [{
 89 |     //       name: "research_agentt",
 90 |     //       description: "Research agent"
 91 |     //   }]
 92 |     // }),
 93 |  // ],
 94 | //});
 95 | \`\`\`
 96 | **Next for JS run these commands:**
 97 | - Run this command to start your LangGraph server \`npx @langchain/langgraph-cli dev --host localhost --port 8123\`
 98 | - Run this command to connect your Copilot Cloud Tunnel to the LangGraph server \`npx copilotkit@latest dev --port 8123\`
 99 | 
100 | ## Usage
101 | 
102 | Navigate to [http://localhost:3000](http://localhost:3000).
103 | 
104 | # LangGraph Studio
105 | 
106 | Run LangGraph studio, then load the \`./agent-py\` folder into it.
107 | 
108 | # Troubleshooting
109 | 
110 | A few things to try if you are running into trouble:
111 | 
112 | 1. Make sure there is no other local application server running on the 8000 port.
113 | 2. Under \`/agent/research_canvas/demo.py\`, change \`0.0.0.0\` to \`127.0.0.1\` or to \`localhost\`
114 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/.eslintrc.json:
--------------------------------------------------------------------------------
1 | {
2 |   "extends": ["next/core-web-vitals", "next/typescript"],
3 |   "rules": {
4 |     "@typescript-eslint/no-explicit-any": "off",
5 |     "@typescript-eslint/no-unused-vars": "off"
6 |   }
7 | }

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/.gitignore:
--------------------------------------------------------------------------------
 1 | # See https://help.github.com/articles/ignoring-files/ for more about ignoring files.
 2 | 
 3 | # dependencies
 4 | /node_modules
 5 | /.pnp
 6 | .pnp.js
 7 | .yarn/install-state.gz
 8 | 
 9 | # testing
10 | /coverage
11 | 
12 | # next.js
13 | /.next/
14 | /out/
15 | 
16 | # production
17 | /build
18 | 
19 | # misc
20 | .DS_Store
21 | *.pem
22 | 
23 | # debug
24 | npm-debug.log*
25 | yarn-debug.log*
26 | yarn-error.log*
27 | 
28 | # local env files
29 | .env*.local
30 | 
31 | # vercel
32 | .vercel
33 | 
34 | # typescript
35 | *.tsbuildinfo
36 | next-env.d.ts
37 | 
38 | .env
39 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/README.md:
--------------------------------------------------------------------------------
 1 | This is a [Next.js](https://nextjs.org) project bootstrapped with [\`create-next-app\`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).
 2 | 
 3 | ## Getting Started
 4 | 
 5 | First, run the development server:
 6 | 
 7 | \`\`\`bash
 8 | npm run dev
 9 | # or
10 | yarn dev
11 | # or
12 | pnpm dev
13 | # or
14 | bun dev
15 | \`\`\`
16 | 
17 | Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
18 | 
19 | You can start editing the page by modifying \`app/page.tsx\`. The page auto-updates as you edit the file.
20 | 
21 | This project uses [\`next/font\`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.
22 | 
23 | ## Learn More
24 | 
25 | To learn more about Next.js, take a look at the following resources:
26 | 
27 | - [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
28 | - [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
29 | 
30 | You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!
31 | 
32 | ## Deploy on Vercel
33 | 
34 | The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.
35 | 
36 | Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
37 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/components.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "$schema": "https://ui.shadcn.com/schema.json",
 3 |   "style": "new-york",
 4 |   "rsc": true,
 5 |   "tsx": true,
 6 |   "tailwind": {
 7 |     "config": "tailwind.config.ts",
 8 |     "css": "src/app/globals.css",
 9 |     "baseColor": "neutral",
10 |     "cssVariables": true,
11 |     "prefix": ""
12 |   },
13 |   "aliases": {
14 |     "components": "@/components",
15 |     "utils": "@/lib/utils",
16 |     "ui": "@/components/ui",
17 |     "lib": "@/lib",
18 |     "hooks": "@/hooks"
19 |   }
20 | }

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/next.config.mjs:
--------------------------------------------------------------------------------
1 | /** @type {import('next').NextConfig} */
2 | const nextConfig = {
3 |   output: "standalone"
4 | };
5 | 
6 | export default nextConfig;
7 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/package.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "name": "ui",
 3 |   "version": "0.1.0",
 4 |   "private": true,
 5 |   "scripts": {
 6 |     "dev": "next dev",
 7 |     "build": "next build",
 8 |     "start": "next start",
 9 |     "lint": "next lint"
10 |   },
11 |   "dependencies": {
12 |     "@copilotkit/react-core": "1.8.3",
13 |     "@copilotkit/react-ui": "1.8.3",
14 |     "@copilotkit/runtime": "1.8.3",
15 |     "@radix-ui/react-dialog": "^1.1.2",
16 |     "@radix-ui/react-icons": "^1.3.2",
17 |     "@radix-ui/react-select": "^2.1.2",
18 |     "@radix-ui/react-slot": "^1.1.0",
19 |     "class-variance-authority": "^0.7.0",
20 |     "clsx": "^2.1.1",
21 |     "lucide-react": "^0.451.0",
22 |     "next": "15.1.0",
23 |     "openai": "^4.85.1",
24 |     "react": "19.0.0",
25 |     "react-dom": "19.0.0",
26 |     "tailwind-merge": "^2.5.3",
27 |     "tailwindcss-animate": "^1.0.7"
28 |   },
29 |   "devDependencies": {
30 |     "@types/node": "^22.0.0",
31 |     "@types/react": "19.0.1",
32 |     "@types/react-dom": "19.0.2",
33 |     "eslint": "^9.0.0",
34 |     "eslint-config-next": "15.1.0",
35 |     "postcss": "^8",
36 |     "tailwindcss": "^3.4.1",
37 |     "typescript": "^5"
38 |   },
39 |   "pnpm": {
40 |     "overrides": {
41 |       "@types/react": "19.0.1",
42 |       "@types/react-dom": "19.0.2"
43 |     }
44 |   }
45 | }
46 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/postcss.config.mjs:
--------------------------------------------------------------------------------
1 | /** @type {import('postcss-load-config').Config} */
2 | const config = {
3 |   plugins: {
4 |     tailwindcss: {},
5 |   },
6 | };
7 | 
8 | export default config;
9 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/Main.tsx:
--------------------------------------------------------------------------------
 1 | import { ResearchCanvas } from "@/components/ResearchCanvas";
 2 | import { useModelSelectorContext } from "@/lib/model-selector-provider";
 3 | import { AgentState } from "@/lib/types";
 4 | import { useCoAgent } from "@copilotkit/react-core";
 5 | import { CopilotChat } from "@copilotkit/react-ui";
 6 | import { useCopilotChatSuggestions } from "@copilotkit/react-ui";
 7 | 
 8 | export default function Main() {
 9 |   const { model, agent } = useModelSelectorContext();
10 |   const { state, setState } = useCoAgent<AgentState>({
11 |     name: agent,
12 |     initialState: {
13 |       model,
14 |       research_question: "",
15 |       resources: [],
16 |       report: "",
17 |       logs: [],
18 |     },
19 |   });
20 | 
21 |   useCopilotChatSuggestions({
22 |     instructions: "Lifespan of penguins",
23 |   });
24 | 
25 |   return (
26 |     <>
27 |       <h1 className="flex h-[60px] bg-[#0E103D] text-white items-center px-10 text-2xl font-medium">
28 |         Research Helper
29 |       </h1>
30 | 
31 |       <div
32 |         className="flex flex-1 border"
33 |         style={{ height: "calc(100vh - 60px)" }}
34 |       >
35 |         <div className="flex-1 overflow-hidden">
36 |           <ResearchCanvas />
37 |         </div>
38 |         <div
39 |           className="w-[500px] h-full flex-shrink-0"
40 |           style={
41 |             {
42 |               "--copilot-kit-background-color": "#E0E9FD",
43 |               "--copilot-kit-secondary-color": "#6766FC",
44 |               "--copilot-kit-separator-color": "#b8b8b8",
45 |               "--copilot-kit-primary-color": "#FFFFFF",
46 |               "--copilot-kit-contrast-color": "#000000",
47 |               "--copilot-kit-secondary-contrast-color": "#000",
48 |             } as any
49 |           }
50 |         >
51 |           <CopilotChat
52 |             className="h-full"
53 |             onSubmitMessage={async (message) => {
54 |               // clear the logs before starting the new research
55 |               setState({ ...state, logs: [] });
56 |               await new Promise((resolve) => setTimeout(resolve, 30));
57 |             }}
58 |             labels={{
59 |               initial: "Hi! How can I assist you with your research today?",
60 |             }}
61 |           />
62 |         </div>
63 |       </div>
64 |     </>
65 |   );
66 | }
67 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/api/copilotkit/route.ts:
--------------------------------------------------------------------------------
 1 | import {
 2 |   CopilotRuntime,
 3 |   OpenAIAdapter,
 4 |   copilotRuntimeNextJSAppRouterEndpoint,
 5 |   langGraphPlatformEndpoint,
 6 |   copilotKitEndpoint,
 7 | } from "@copilotkit/runtime";
 8 | import OpenAI from "openai";
 9 | import { NextRequest } from "next/server";
10 | 
11 | const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
12 | const llmAdapter = new OpenAIAdapter({ openai } as any);
13 | const langsmithApiKey = process.env.LANGSMITH_API_KEY as string;
14 | 
15 | export const POST = async (req: NextRequest) => {
16 |   const searchParams = req.nextUrl.searchParams;
17 |   const deploymentUrl =
18 |     searchParams.get("lgcDeploymentUrl") || process.env.LGC_DEPLOYMENT_URL;
19 | 
20 |   const isCrewAi = searchParams.get("coAgentsModel") === "crewai";
21 | 
22 |   const remoteEndpoint =
23 |     deploymentUrl && !isCrewAi
24 |       ? langGraphPlatformEndpoint({
25 |           deploymentUrl,
26 |           langsmithApiKey,
27 |           agents: [
28 |             {
29 |               name: "research_agent",
30 |               description: "Research agent",
31 |             },
32 |             {
33 |               name: "research_agent_google_genai",
34 |               description: "Research agent",
35 |               assistantId: "9dc0ca3b-1aa6-547d-93f0-e21597d2011c",
36 |             },
37 |           ],
38 |         })
39 |       : copilotKitEndpoint({
40 |           url:
41 |             process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit",
42 |         });
43 | 
44 |   const runtime = new CopilotRuntime({
45 |     remoteEndpoints: [remoteEndpoint],
46 |   });
47 | 
48 |   const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
49 |     runtime,
50 |     serviceAdapter: llmAdapter,
51 |     endpoint: "/api/copilotkit",
52 |   });
53 | 
54 |   return handleRequest(req);
55 | };
56 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/favicon.ico:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/ui/src/app/favicon.ico

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/fonts/GeistMonoVF.woff:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/ui/src/app/fonts/GeistMonoVF.woff

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/fonts/GeistVF.woff:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/CopilotKit/CopilotKit/main/examples/coagents-research-canvas/ui/src/app/fonts/GeistVF.woff

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/globals.css:
--------------------------------------------------------------------------------
  1 | @tailwind base;
  2 | @tailwind components;
  3 | @tailwind utilities;
  4 | 
  5 | body {
  6 |   font-family: Arial, Helvetica, sans-serif;
  7 | }
  8 | 
  9 | @layer utilities {
 10 |   .text-balance {
 11 |     text-wrap: balance;
 12 |   }
 13 | }
 14 | 
 15 | @layer base {
 16 |   :root {
 17 |     --background: 0 0% 100%;
 18 |     --foreground: 0 0% 3.9%;
 19 |     --card: 0 0% 100%;
 20 |     --card-foreground: 0 0% 3.9%;
 21 |     --popover: 0 0% 100%;
 22 |     --popover-foreground: 0 0% 3.9%;
 23 |     --primary: 0 0% 9%;
 24 |     --primary-foreground: 0 0% 98%;
 25 |     --secondary: 0 0% 96.1%;
 26 |     --secondary-foreground: 0 0% 9%;
 27 |     --muted: 0 0% 96.1%;
 28 |     --muted-foreground: 0 0% 45.1%;
 29 |     --accent: 0 0% 96.1%;
 30 |     --accent-foreground: 0 0% 9%;
 31 |     --destructive: 0 84.2% 60.2%;
 32 |     --destructive-foreground: 0 0% 98%;
 33 |     --border: 0 0% 89.8%;
 34 |     --input: 0 0% 89.8%;
 35 |     --ring: 0 0% 3.9%;
 36 |     --chart-1: 12 76% 61%;
 37 |     --chart-2: 173 58% 39%;
 38 |     --chart-3: 197 37% 24%;
 39 |     --chart-4: 43 74% 66%;
 40 |     --chart-5: 27 87% 67%;
 41 |     --radius: 0.5rem;
 42 |   }
 43 |   .dark {
 44 |     --background: 0 0% 3.9%;
 45 |     --foreground: 0 0% 98%;
 46 |     --card: 0 0% 3.9%;
 47 |     --card-foreground: 0 0% 98%;
 48 |     --popover: 0 0% 3.9%;
 49 |     --popover-foreground: 0 0% 98%;
 50 |     --primary: 0 0% 98%;
 51 |     --primary-foreground: 0 0% 9%;
 52 |     --secondary: 0 0% 14.9%;
 53 |     --secondary-foreground: 0 0% 98%;
 54 |     --muted: 0 0% 14.9%;
 55 |     --muted-foreground: 0 0% 63.9%;
 56 |     --accent: 0 0% 14.9%;
 57 |     --accent-foreground: 0 0% 98%;
 58 |     --destructive: 0 62.8% 30.6%;
 59 |     --destructive-foreground: 0 0% 98%;
 60 |     --border: 0 0% 14.9%;
 61 |     --input: 0 0% 14.9%;
 62 |     --ring: 0 0% 83.1%;
 63 |     --chart-1: 220 70% 50%;
 64 |     --chart-2: 160 60% 45%;
 65 |     --chart-3: 30 80% 55%;
 66 |     --chart-4: 280 65% 60%;
 67 |     --chart-5: 340 75% 55%;
 68 |   }
 69 | }
 70 | 
 71 | @layer base {
 72 |   * {
 73 |     @apply border-border;
 74 |   }
 75 |   body {
 76 |     @apply bg-background text-foreground;
 77 |   }
 78 | }
 79 | 
 80 | .copilotKitMessage.copilotKitUserMessage {
 81 |   border-radius: 0.5rem 0.5rem 0 0.5rem;
 82 | }
 83 | 
 84 | .copilotKitMessage.copilotKitAssistantMessage {
 85 |   border-radius: 0.5rem 0.5rem 0.5rem 0;
 86 | }
 87 | 
 88 | .copilotKitChat {
 89 |   background-color: #e0e9fd;
 90 | }
 91 | 
 92 | .copilotKitResponseButton {
 93 |   background-color: transparent;
 94 |   color: var(--copilot-kit-secondary-color);
 95 |   border: 0px;
 96 | }
 97 | 
 98 | .copilotKitInput {
 99 |   background-color: white;
100 | }
101 | 
102 | .copilotKitMessageControlButton {
103 |   color: #6766FC;
104 | }
105 | 
106 | .copilotKitInput > textarea {
107 |   background-color: white;
108 |   color: black;
109 | }
110 | 
111 | .copilotKitInput > .copilotKitInputControls > button:not([disabled]) {
112 |   color: var(--copilot-kit-secondary-color);
113 | }
114 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/layout.tsx:
--------------------------------------------------------------------------------
 1 | import type { Metadata } from "next";
 2 | import localFont from "next/font/local";
 3 | import "@copilotkit/react-ui/styles.css";
 4 | import "./globals.css";
 5 | 
 6 | const geistSans = localFont({
 7 |   src: "./fonts/GeistVF.woff",
 8 |   variable: "--font-geist-sans",
 9 |   weight: "100 900",
10 | });
11 | const geistMono = localFont({
12 |   src: "./fonts/GeistMonoVF.woff",
13 |   variable: "--font-geist-mono",
14 |   weight: "100 900",
15 | });
16 | 
17 | export const metadata: Metadata = {
18 |   title: "Create Next App",
19 |   description: "Generated by create next app",
20 | };
21 | 
22 | export default function RootLayout({
23 |   children,
24 | }: Readonly<{
25 |   children: React.ReactNode;
26 | }>) {
27 |   return (
28 |     <html lang="en">
29 |       <body
30 |         className={\`${geistSans.variable} ${geistMono.variable} antialiased\`}
31 |       >
32 |         {children}
33 |       </body>
34 |     </html>
35 |   );
36 | }
37 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/app/page.tsx:
--------------------------------------------------------------------------------
 1 | "use client";
 2 | 
 3 | import { CopilotKit } from "@copilotkit/react-core";
 4 | import Main from "./Main";
 5 | import {
 6 |   ModelSelectorProvider,
 7 |   useModelSelectorContext,
 8 | } from "@/lib/model-selector-provider";
 9 | import { ModelSelector } from "@/components/ModelSelector";
10 | 
11 | export default function ModelSelectorWrapper() {
12 |   return (
13 |     <ModelSelectorProvider>
14 |       <Home />
15 |       <ModelSelector />
16 |     </ModelSelectorProvider>
17 |   );
18 | }
19 | 
20 | function Home() {
21 |   const { agent, lgcDeploymentUrl } = useModelSelectorContext();
22 | 
23 |   // This logic is implemented to demonstrate multi-agent frameworks in this demo project.
24 |   // There are cleaner ways to handle this in a production environment.
25 |   const runtimeUrl = lgcDeploymentUrl
26 |     ? \`/api/copilotkit?lgcDeploymentUrl=${lgcDeploymentUrl}\`
27 |     : \`/api/copilotkit${
28 |         agent.includes("crewai") ? "?coAgentsModel=crewai" : ""
29 |       }\`;
30 | 
31 |   return (
32 |     <CopilotKit runtimeUrl={runtimeUrl} showDevConsole={false} agent={agent}>
33 |       <Main />
34 |     </CopilotKit>
35 |   );
36 | }
37 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/AddResourceDialog.tsx:
--------------------------------------------------------------------------------
  1 | import {
  2 |   Dialog,
  3 |   DialogContent,
  4 |   DialogHeader,
  5 |   DialogTitle,
  6 |   DialogTrigger,
  7 | } from "@/components/ui/dialog";
  8 | import { Input } from "@/components/ui/input";
  9 | import { Textarea } from "@/components/ui/textarea";
 10 | import { Button } from "@/components/ui/button";
 11 | import { PlusCircle, Plus } from "lucide-react";
 12 | import { Resource } from "@/lib/types";
 13 | 
 14 | type AddResourceDialogProps = {
 15 |   isOpen: boolean;
 16 |   onOpenChange: (isOpen: boolean) => void;
 17 |   newResource: Resource;
 18 |   setNewResource: (resource: Resource) => void;
 19 |   addResource: () => void;
 20 | };
 21 | 
 22 | export function AddResourceDialog({
 23 |   isOpen,
 24 |   onOpenChange,
 25 |   newResource,
 26 |   setNewResource,
 27 |   addResource,
 28 | }: AddResourceDialogProps) {
 29 |   return (
 30 |     <Dialog open={isOpen} onOpenChange={onOpenChange}>
 31 |       <DialogTrigger asChild>
 32 |         <Button
 33 |           variant="link"
 34 |           size="sm"
 35 |           className="text-sm font-bold text-[#6766FC]"
 36 |         >
 37 |           Add Resource <PlusCircle className="w-6 h-6 ml-2" />
 38 |         </Button>
 39 |       </DialogTrigger>
 40 |       <DialogContent className="sm:max-w-[425px]">
 41 |         <DialogHeader>
 42 |           <DialogTitle>Add New Resource</DialogTitle>
 43 |         </DialogHeader>
 44 |         <div className="grid gap-4 py-4">
 45 |           <label htmlFor="new-url" className="text-sm font-bold">
 46 |             Resource URL
 47 |           </label>
 48 |           <Input
 49 |             id="new-url"
 50 |             placeholder="Resource URL"
 51 |             value={newResource.url || ""}
 52 |             onChange={(e) =>
 53 |               setNewResource({ ...newResource, url: e.target.value })
 54 |             }
 55 |             aria-label="New resource URL"
 56 |             className="bg-background"
 57 |           />
 58 |           <label htmlFor="new-title" className="text-sm font-bold">
 59 |             Resource Title
 60 |           </label>
 61 |           <Input
 62 |             id="new-title"
 63 |             placeholder="Resource Title"
 64 |             value={newResource.title || ""}
 65 |             onChange={(e) =>
 66 |               setNewResource({ ...newResource, title: e.target.value })
 67 |             }
 68 |             aria-label="New resource title"
 69 |             className="bg-background"
 70 |           />
 71 |           <label htmlFor="new-description" className="text-sm font-bold">
 72 |             Resource Description
 73 |           </label>
 74 |           <Textarea
 75 |             id="new-description"
 76 |             placeholder="Resource Description"
 77 |             value={newResource.description || ""}
 78 |             onChange={(e) =>
 79 |               setNewResource({
 80 |                 ...newResource,
 81 |                 description: e.target.value,
 82 |               })
 83 |             }
 84 |             aria-label="New resource description"
 85 |             className="bg-background"
 86 |           />
 87 |         </div>
 88 |         <Button
 89 |           onClick={addResource}
 90 |           className="w-full bg-[#6766FC] text-white"
 91 |           disabled={
 92 |             !newResource.url || !newResource.title || !newResource.description
 93 |           }
 94 |         >
 95 |           <Plus className="w-4 h-4 mr-2" /> Add Resource
 96 |         </Button>
 97 |       </DialogContent>
 98 |     </Dialog>
 99 |   );
100 | }
101 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/EditResourceDialog.tsx:
--------------------------------------------------------------------------------
 1 | import {
 2 |   Dialog,
 3 |   DialogContent,
 4 |   DialogHeader,
 5 |   DialogTitle,
 6 | } from "@/components/ui/dialog";
 7 | import { Input } from "@/components/ui/input";
 8 | import { Textarea } from "@/components/ui/textarea";
 9 | import { Button } from "@/components/ui/button";
10 | import { Resource } from "@/lib/types";
11 | 
12 | type EditResourceDialogProps = {
13 |   isOpen: boolean;
14 |   onOpenChange: (isOpen: boolean) => void;
15 |   editResource: Resource | null;
16 |   setEditResource: (
17 |     resource: ((prev: Resource | null) => Resource | null) | Resource | null
18 |   ) => void;
19 |   updateResource: () => void;
20 | };
21 | 
22 | export function EditResourceDialog({
23 |   isOpen,
24 |   onOpenChange,
25 |   editResource,
26 |   setEditResource,
27 |   updateResource,
28 | }: EditResourceDialogProps) {
29 |   return (
30 |     <Dialog open={isOpen} onOpenChange={onOpenChange}>
31 |       <DialogContent className="sm:max-w-[425px]">
32 |         <DialogHeader>
33 |           <DialogTitle>Edit Resource</DialogTitle>
34 |         </DialogHeader>
35 |         <div className="grid gap-4 py-4">
36 |           <label htmlFor="edit-url" className="text-sm font-bold">
37 |             Resource URL
38 |           </label>
39 |           <Input
40 |             id="edit-url"
41 |             placeholder="Resource URL"
42 |             value={editResource?.url || ""}
43 |             onChange={(e) =>
44 |               setEditResource((prev) =>
45 |                 prev ? { ...prev, url: e.target.value } : null
46 |               )
47 |             }
48 |             aria-label="Edit resource URL"
49 |             className="bg-background"
50 |           />
51 |           <label htmlFor="edit-title" className="text-sm font-bold">
52 |             Resource Title
53 |           </label>
54 |           <Input
55 |             id="edit-title"
56 |             placeholder="Resource Title"
57 |             value={editResource?.title || ""}
58 |             onChange={(e) =>
59 |               setEditResource((prev: any) =>
60 |                 prev ? { ...prev, title: e.target.value } : null
61 |               )
62 |             }
63 |             aria-label="Edit resource title"
64 |             className="bg-background"
65 |           />
66 |           <label htmlFor="edit-description" className="text-sm font-bold">
67 |             Resource Description
68 |           </label>
69 |           <Textarea
70 |             id="edit-description"
71 |             placeholder="Resource Description"
72 |             value={editResource?.description || ""}
73 |             onChange={(e) =>
74 |               setEditResource((prev) =>
75 |                 prev ? { ...prev, description: e.target.value } : null
76 |               )
77 |             }
78 |             aria-label="Edit resource description"
79 |             className="bg-background"
80 |           />
81 |         </div>
82 |         <Button
83 |           onClick={updateResource}
84 |           className="w-full bg-[#6766FC] text-white"
85 |           disabled={
86 |             !editResource?.url ||
87 |             !editResource?.title ||
88 |             !editResource?.description
89 |           }
90 |         >
91 |           Save Changes
92 |         </Button>
93 |       </DialogContent>
94 |     </Dialog>
95 |   );
96 | }
97 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ModelSelector.tsx:
--------------------------------------------------------------------------------
 1 | "use client";
 2 | 
 3 | import React from "react";
 4 | import {
 5 |   Select,
 6 |   SelectContent,
 7 |   SelectItem,
 8 |   SelectTrigger,
 9 |   SelectValue,
10 | } from "@/components/ui/select";
11 | import { useModelSelectorContext } from "@/lib/model-selector-provider";
12 | 
13 | export function ModelSelector() {
14 |   const { model, setModel } = useModelSelectorContext();
15 | 
16 |   return (
17 |     <div className="fixed bottom-0 left-0 p-4 z-50">
18 |       <Select value={model} onValueChange={(v) => setModel(v)}>
19 |         <SelectTrigger className="w-[180px]">
20 |           <SelectValue placeholder="Theme" />
21 |         </SelectTrigger>
22 |         <SelectContent>
23 |           <SelectItem value="openai">OpenAI</SelectItem>
24 |           <SelectItem value="anthropic">Anthropic</SelectItem>
25 |           <SelectItem value="google_genai">Google Generative AI</SelectItem>
26 |           <SelectItem value="crewai">CrewAI</SelectItem>
27 |         </SelectContent>
28 |       </Select>
29 |     </div>
30 |   );
31 | }
32 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/Progress.tsx:
--------------------------------------------------------------------------------
 1 | import { cn } from "@/lib/utils";
 2 | import { CheckIcon, LoaderCircle } from "lucide-react";
 3 | import { truncateUrl } from "@/lib/utils";
 4 | 
 5 | export function Progress({
 6 |   logs,
 7 | }: {
 8 |   logs: {
 9 |     message: string;
10 |     done: boolean;
11 |   }[];
12 | }) {
13 |   if (logs.length === 0) {
14 |     return null;
15 |   }
16 | 
17 |   return (
18 |     <div data-test-id="progress-steps">
19 |       <div className="border border-slate-200 bg-slate-100/30 shadow-md rounded-lg overflow-hidden text-sm py-2">
20 |         {logs.map((log, index) => (
21 |           <div
22 |             key={index}
23 |             data-test-id="progress-step-item"
24 |             className={\`flex ${
25 |               log.done || index === logs.findIndex((log) => !log.done)
26 |                 ? ""
27 |                 : "opacity-50"
28 |             }\`}
29 |           >
30 |             <div className="w-8">
31 |               <div
32 |                   className="w-4 h-4 bg-slate-700 flex items-center justify-center rounded-full mt-[10px] ml-[12px]"
33 |                   data-test-id={log.done ? 'progress-step-item_done' : 'progress-step-item_loading'}
34 |               >
35 |                 {log.done ? (
36 |                   <CheckIcon className="w-3 h-3 text-white" />
37 |                 ) : (
38 |                   <LoaderCircle className="w-3 h-3 text-white animate-spin" />
39 |                 )}
40 |               </div>
41 |               {index < logs.length - 1 && (
42 |                 <div
43 |                   className={cn("h-full w-[1px] bg-slate-200 ml-[20px]")}
44 |                 ></div>
45 |               )}
46 |             </div>
47 |             <div className="flex-1 flex justify-center py-2 pl-2 pr-4">
48 |               <div className="flex-1 flex items-center text-xs">
49 |                 {log.message.replace(
50 |                   /https?:\/\/[^\s]+/g, // Regex to match URLs
51 |                   (url) => truncateUrl(url) // Replace with truncated URL
52 |                 )}
53 |               </div>
54 |             </div>
55 |           </div>
56 |         ))}
57 |       </div>
58 |     </div>
59 |   );
60 | }
61 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ResearchCanvas.tsx:
--------------------------------------------------------------------------------
  1 | "use client";
  2 | 
  3 | import { useState } from "react";
  4 | import { Input } from "@/components/ui/input";
  5 | import { Textarea } from "@/components/ui/textarea";
  6 | import {
  7 |   useCoAgent,
  8 |   useCoAgentStateRender,
  9 |   useCopilotAction,
 10 | } from "@copilotkit/react-core";
 11 | import { Progress } from "./Progress";
 12 | import { EditResourceDialog } from "./EditResourceDialog";
 13 | import { AddResourceDialog } from "./AddResourceDialog";
 14 | import { Resources } from "./Resources";
 15 | import { AgentState, Resource } from "@/lib/types";
 16 | import { useModelSelectorContext } from "@/lib/model-selector-provider";
 17 | 
 18 | export function ResearchCanvas() {
 19 |   const { model, agent } = useModelSelectorContext();
 20 | 
 21 |   const { state, setState } = useCoAgent<AgentState>({
 22 |     name: agent,
 23 |     initialState: {
 24 |       model,
 25 |     },
 26 |   });
 27 | 
 28 |   useCoAgentStateRender({
 29 |     name: agent,
 30 |     render: ({ state, nodeName, status }) => {
 31 |       if (!state.logs || state.logs.length === 0) {
 32 |         return null;
 33 |       }
 34 |       return <Progress logs={state.logs} />;
 35 |     },
 36 |   });
 37 | 
 38 |   useCopilotAction({
 39 |     name: "DeleteResources",
 40 |     description:
 41 |       "Prompt the user for resource delete confirmation, and then perform resource deletion",
 42 |     available: "remote",
 43 |     parameters: [
 44 |       {
 45 |         name: "urls",
 46 |         type: "string[]",
 47 |       },
 48 |     ],
 49 |     renderAndWait: ({ args, status, handler }) => {
 50 |       return (
 51 |         <div
 52 |           className=""
 53 |           data-test-id="delete-resource-generative-ui-container"
 54 |         >
 55 |           <div className="font-bold text-base mb-2">
 56 |             Delete these resources?
 57 |           </div>
 58 |           <Resources
 59 |             resources={resources.filter((resource) =>
 60 |               (args.urls || []).includes(resource.url)
 61 |             )}
 62 |             customWidth={200}
 63 |           />
 64 |           {status === "executing" && (
 65 |             <div className="mt-4 flex justify-start space-x-2">
 66 |               <button
 67 |                 onClick={() => handler("NO")}
 68 |                 className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
 69 |               >
 70 |                 Cancel
 71 |               </button>
 72 |               <button
 73 |                 data-test-id="button-delete"
 74 |                 onClick={() => handler("YES")}
 75 |                 className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
 76 |               >
 77 |                 Delete
 78 |               </button>
 79 |             </div>
 80 |           )}
 81 |         </div>
 82 |       );
 83 |     },
 84 |   });
 85 | 
 86 |   const resources: Resource[] = state.resources || [];
 87 |   const setResources = (resources: Resource[]) => {
 88 |     setState({ ...state, resources });
 89 |   };
 90 | 
 91 |   // const [resources, setResources] = useState<Resource[]>(dummyResources);
 92 |   const [newResource, setNewResource] = useState<Resource>({
 93 |     url: "",
 94 |     title: "",
 95 |     description: "",
 96 |   });
 97 |   const [isAddResourceOpen, setIsAddResourceOpen] = useState(false);
 98 | 
 99 |   const addResource = () => {
100 |     if (newResource.url) {
101 |       setResources([...resources, { ...newResource }]);
102 |       setNewResource({ url: "", title: "", description: "" });
103 |       setIsAddResourceOpen(false);
104 |     }
105 |   };
106 | 
107 |   const removeResource = (url: string) => {
108 |     setResources(
109 |       resources.filter((resource: Resource) => resource.url !== url)
110 |     );
111 |   };
112 | 
113 |   const [editResource, setEditResource] = useState<Resource | null>(null);
114 |   const [originalUrl, setOriginalUrl] = useState<string | null>(null);
115 |   const [isEditResourceOpen, setIsEditResourceOpen] = useState(false);
116 | 
117 |   const handleCardClick = (resource: Resource) => {
118 |     setEditResource({ ...resource }); // Ensure a new object is created
119 |     setOriginalUrl(resource.url); // Store the original URL
120 |     setIsEditResourceOpen(true);
121 |   };
122 | 
123 |   const updateResource = () => {
124 |     if (editResource && originalUrl) {
125 |       setResources(
126 |         resources.map((resource) =>
127 |           resource.url === originalUrl ? { ...editResource } : resource
128 |         )
129 |       );
130 |       setEditResource(null);
131 |       setOriginalUrl(null);
132 |       setIsEditResourceOpen(false);
133 |     }
134 |   };
135 | 
136 |   return (
137 |     <div className="w-full h-full overflow-y-auto p-10 bg-[#F5F8FF]">
138 |       <div className="space-y-8 pb-10">
139 |         <div>
140 |           <h2 className="text-lg font-medium mb-3 text-primary">
141 |             Research Question
142 |           </h2>
143 |           <Input
144 |             placeholder="Enter your research question"
145 |             value={state.research_question || ""}
146 |             onChange={(e) =>
147 |               setState({ ...state, research_question: e.target.value })
148 |             }
149 |             aria-label="Research question"
150 |             className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
151 |           />
152 |         </div>
153 | 
154 |         <div>
155 |           <div className="flex justify-between items-center mb-4">
156 |             <h2 className="text-lg font-medium text-primary">Resources</h2>
157 |             <EditResourceDialog
158 |               isOpen={isEditResourceOpen}
159 |               onOpenChange={setIsEditResourceOpen}
160 |               editResource={editResource}
161 |               setEditResource={setEditResource}
162 |               updateResource={updateResource}
163 |             />
164 |             <AddResourceDialog
165 |               isOpen={isAddResourceOpen}
166 |               onOpenChange={setIsAddResourceOpen}
167 |               newResource={newResource}
168 |               setNewResource={setNewResource}
169 |               addResource={addResource}
170 |             />
171 |           </div>
172 |           {resources.length === 0 && (
173 |             <div className="text-sm text-slate-400">
174 |               Click the button above to add resources.
175 |             </div>
176 |           )}
177 | 
178 |           {resources.length !== 0 && (
179 |             <Resources
180 |               resources={resources}
181 |               handleCardClick={handleCardClick}
182 |               removeResource={removeResource}
183 |             />
184 |           )}
185 |         </div>
186 | 
187 |         <div className="flex flex-col h-full">
188 |           <h2 className="text-lg font-medium mb-3 text-primary">
189 |             Research Draft
190 |           </h2>
191 |           <Textarea
192 |             data-test-id="research-draft"
193 |             placeholder="Write your research draft here"
194 |             value={state.report || ""}
195 |             onChange={(e) => setState({ ...state, report: e.target.value })}
196 |             rows={10}
197 |             aria-label="Research draft"
198 |             className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
199 |             style={{ minHeight: "200px" }}
200 |           />
201 |         </div>
202 |       </div>
203 |     </div>
204 |   );
205 | }
206 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/Resources.tsx:
--------------------------------------------------------------------------------
  1 | import { Card, CardContent } from "@/components/ui/card";
  2 | import { Button } from "@/components/ui/button";
  3 | import { Trash2 } from "lucide-react";
  4 | import { Resource } from "@/lib/types";
  5 | import { truncateUrl } from "@/lib/utils";
  6 | 
  7 | type ResourcesProps = {
  8 |   resources: Resource[];
  9 |   customWidth?: number;
 10 |   handleCardClick?: (resource: Resource) => void;
 11 |   removeResource?: (url: string) => void;
 12 | };
 13 | 
 14 | export function Resources({
 15 |   resources,
 16 |   handleCardClick,
 17 |   removeResource,
 18 |   customWidth,
 19 | }: ResourcesProps) {
 20 |   return (
 21 |     <div data-test-id="resources" className="flex space-x-3 overflow-x-auto">
 22 |       {resources.map((resource, idx) => (
 23 |         <Card
 24 |           data-test-id={\`resource\`}
 25 |           key={idx}
 26 |           className={
 27 |             "bg-background border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 flex-none" +
 28 |             (handleCardClick ? " cursor-pointer" : "")
 29 |           }
 30 |           style={{ width: customWidth + "px" || "320px" }}
 31 |           onClick={() => handleCardClick?.(resource)}
 32 |         >
 33 |           <CardContent className="px-6 py-6 relative">
 34 |             <div className="flex items-start space-x-3 text-sm">
 35 |               <div className="flex-grow">
 36 |                 <h3
 37 |                   className="font-bold text-lg"
 38 |                   style={{
 39 |                     maxWidth: customWidth ? customWidth - 30 + "px" : "230px",
 40 |                     overflow: "hidden",
 41 |                     textOverflow: "ellipsis",
 42 |                     whiteSpace: "nowrap",
 43 |                   }}
 44 |                 >
 45 |                   {resource.title}
 46 |                 </h3>
 47 |                 <p
 48 |                   className="text-base mt-2"
 49 |                   style={{
 50 |                     maxWidth: customWidth ? customWidth - 30 + "px" : "250px",
 51 |                     overflowWrap: "break-word",
 52 |                   }}
 53 |                 >
 54 |                   {resource.description?.length > 250
 55 |                     ? resource.description.slice(0, 250) + "..."
 56 |                     : resource.description}
 57 |                 </p>
 58 |                 <a
 59 |                   href={resource.url}
 60 |                   target="_blank"
 61 |                   rel="noopener noreferrer"
 62 |                   className="text-sm text-primary hover:underline mt-3 text-slate-400 inline-block"
 63 |                   title={resource.url}
 64 |                   style={{
 65 |                     width: customWidth ? customWidth - 30 + "px" : "250px",
 66 |                     overflow: "hidden",
 67 |                     textOverflow: "ellipsis",
 68 |                     whiteSpace: "nowrap",
 69 |                   }}
 70 |                 >
 71 |                   {resource.description && (
 72 |                     <>
 73 |                       <img
 74 |                         src={\`https://www.google.com/s2/favicons?domain=${resource.url}\`}
 75 |                         alt="favicon"
 76 |                         className="inline-block mr-2"
 77 |                         style={{ width: "16px", height: "16px" }}
 78 |                       />
 79 |                       {truncateUrl(resource.url)}
 80 |                     </>
 81 |                   )}
 82 |                 </a>
 83 |               </div>
 84 |               {removeResource && (
 85 |                 <div className="flex items-start absolute top-4 right-4">
 86 |                   <Button
 87 |                     data-test-id="remove-resource"
 88 |                     variant="ghost"
 89 |                     size="icon"
 90 |                     onClick={(e) => {
 91 |                       e.stopPropagation();
 92 |                       removeResource?.(resource.url);
 93 |                     }}
 94 |                     aria-label={\`Remove ${resource.url}\`}
 95 |                   >
 96 |                     <Trash2 className="w-6 h-6 text-gray-400 hover:text-red-500" />
 97 |                   </Button>
 98 |                 </div>
 99 |               )}
100 |             </div>
101 |           </CardContent>
102 |         </Card>
103 |       ))}
104 |     </div>
105 |   );
106 | }
107 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ui/button.tsx:
--------------------------------------------------------------------------------
 1 | import * as React from "react"
 2 | import { Slot } from "@radix-ui/react-slot"
 3 | import { cva, type VariantProps } from "class-variance-authority"
 4 | 
 5 | import { cn } from "@/lib/utils"
 6 | 
 7 | const buttonVariants = cva(
 8 |   "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
 9 |   {
10 |     variants: {
11 |       variant: {
12 |         default:
13 |           "bg-primary text-primary-foreground shadow hover:bg-primary/90",
14 |         destructive:
15 |           "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
16 |         outline:
17 |           "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
18 |         secondary:
19 |           "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
20 |         ghost: "hover:bg-accent hover:text-accent-foreground",
21 |         link: "text-primary underline-offset-4 hover:underline",
22 |       },
23 |       size: {
24 |         default: "h-9 px-4 py-2",
25 |         sm: "h-8 rounded-md px-3 text-xs",
26 |         lg: "h-10 rounded-md px-8",
27 |         icon: "h-9 w-9",
28 |       },
29 |     },
30 |     defaultVariants: {
31 |       variant: "default",
32 |       size: "default",
33 |     },
34 |   }
35 | )
36 | 
37 | export interface ButtonProps
38 |   extends React.ButtonHTMLAttributes<HTMLButtonElement>,
39 |     VariantProps<typeof buttonVariants> {
40 |   asChild?: boolean
41 | }
42 | 
43 | const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
44 |   ({ className, variant, size, asChild = false, ...props }, ref) => {
45 |     const Comp = asChild ? Slot : "button"
46 |     return (
47 |       <Comp
48 |         className={cn(buttonVariants({ variant, size, className }))}
49 |         ref={ref}
50 |         {...props}
51 |       />
52 |     )
53 |   }
54 | )
55 | Button.displayName = "Button"
56 | 
57 | export { Button, buttonVariants }
58 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ui/card.tsx:
--------------------------------------------------------------------------------
 1 | import * as React from "react"
 2 | 
 3 | import { cn } from "@/lib/utils"
 4 | 
 5 | const Card = React.forwardRef<
 6 |   HTMLDivElement,
 7 |   React.HTMLAttributes<HTMLDivElement>
 8 | >(({ className, ...props }, ref) => (
 9 |   <div
10 |     ref={ref}
11 |     className={cn(
12 |       "rounded-xl border bg-card text-card-foreground shadow",
13 |       className
14 |     )}
15 |     {...props}
16 |   />
17 | ))
18 | Card.displayName = "Card"
19 | 
20 | const CardHeader = React.forwardRef<
21 |   HTMLDivElement,
22 |   React.HTMLAttributes<HTMLDivElement>
23 | >(({ className, ...props }, ref) => (
24 |   <div
25 |     ref={ref}
26 |     className={cn("flex flex-col space-y-1.5 p-6", className)}
27 |     {...props}
28 |   />
29 | ))
30 | CardHeader.displayName = "CardHeader"
31 | 
32 | const CardTitle = React.forwardRef<
33 |   HTMLParagraphElement,
34 |   React.HTMLAttributes<HTMLHeadingElement>
35 | >(({ className, ...props }, ref) => (
36 |   <h3
37 |     ref={ref}
38 |     className={cn("font-semibold leading-none tracking-tight", className)}
39 |     {...props}
40 |   />
41 | ))
42 | CardTitle.displayName = "CardTitle"
43 | 
44 | const CardDescription = React.forwardRef<
45 |   HTMLParagraphElement,
46 |   React.HTMLAttributes<HTMLParagraphElement>
47 | >(({ className, ...props }, ref) => (
48 |   <p
49 |     ref={ref}
50 |     className={cn("text-sm text-muted-foreground", className)}
51 |     {...props}
52 |   />
53 | ))
54 | CardDescription.displayName = "CardDescription"
55 | 
56 | const CardContent = React.forwardRef<
57 |   HTMLDivElement,
58 |   React.HTMLAttributes<HTMLDivElement>
59 | >(({ className, ...props }, ref) => (
60 |   <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
61 | ))
62 | CardContent.displayName = "CardContent"
63 | 
64 | const CardFooter = React.forwardRef<
65 |   HTMLDivElement,
66 |   React.HTMLAttributes<HTMLDivElement>
67 | >(({ className, ...props }, ref) => (
68 |   <div
69 |     ref={ref}
70 |     className={cn("flex items-center p-6 pt-0", className)}
71 |     {...props}
72 |   />
73 | ))
74 | CardFooter.displayName = "CardFooter"
75 | 
76 | export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
77 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ui/dialog.tsx:
--------------------------------------------------------------------------------
  1 | "use client"
  2 | 
  3 | import * as React from "react"
  4 | import * as DialogPrimitive from "@radix-ui/react-dialog"
  5 | import { Cross2Icon } from "@radix-ui/react-icons"
  6 | 
  7 | import { cn } from "@/lib/utils"
  8 | 
  9 | const Dialog = DialogPrimitive.Root
 10 | 
 11 | const DialogTrigger = DialogPrimitive.Trigger
 12 | 
 13 | const DialogPortal = DialogPrimitive.Portal
 14 | 
 15 | const DialogClose = DialogPrimitive.Close
 16 | 
 17 | const DialogOverlay = React.forwardRef<
 18 |   React.ElementRef<typeof DialogPrimitive.Overlay>,
 19 |   React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
 20 | >(({ className, ...props }, ref) => (
 21 |   <DialogPrimitive.Overlay
 22 |     ref={ref}
 23 |     className={cn(
 24 |       "fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
 25 |       className
 26 |     )}
 27 |     {...props}
 28 |   />
 29 | ))
 30 | DialogOverlay.displayName = DialogPrimitive.Overlay.displayName
 31 | 
 32 | const DialogContent = React.forwardRef<
 33 |   React.ElementRef<typeof DialogPrimitive.Content>,
 34 |   React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
 35 | >(({ className, children, ...props }, ref) => (
 36 |   <DialogPortal>
 37 |     <DialogOverlay />
 38 |     <DialogPrimitive.Content
 39 |       ref={ref}
 40 |       className={cn(
 41 |         "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
 42 |         className
 43 |       )}
 44 |       {...props}
 45 |     >
 46 |       {children}
 47 |       <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
 48 |         <Cross2Icon className="h-4 w-4" />
 49 |         <span className="sr-only">Close</span>
 50 |       </DialogPrimitive.Close>
 51 |     </DialogPrimitive.Content>
 52 |   </DialogPortal>
 53 | ))
 54 | DialogContent.displayName = DialogPrimitive.Content.displayName
 55 | 
 56 | const DialogHeader = ({
 57 |   className,
 58 |   ...props
 59 | }: React.HTMLAttributes<HTMLDivElement>) => (
 60 |   <div
 61 |     className={cn(
 62 |       "flex flex-col space-y-1.5 text-center sm:text-left",
 63 |       className
 64 |     )}
 65 |     {...props}
 66 |   />
 67 | )
 68 | DialogHeader.displayName = "DialogHeader"
 69 | 
 70 | const DialogFooter = ({
 71 |   className,
 72 |   ...props
 73 | }: React.HTMLAttributes<HTMLDivElement>) => (
 74 |   <div
 75 |     className={cn(
 76 |       "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",
 77 |       className
 78 |     )}
 79 |     {...props}
 80 |   />
 81 | )
 82 | DialogFooter.displayName = "DialogFooter"
 83 | 
 84 | const DialogTitle = React.forwardRef<
 85 |   React.ElementRef<typeof DialogPrimitive.Title>,
 86 |   React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
 87 | >(({ className, ...props }, ref) => (
 88 |   <DialogPrimitive.Title
 89 |     ref={ref}
 90 |     className={cn(
 91 |       "text-lg font-semibold leading-none tracking-tight",
 92 |       className
 93 |     )}
 94 |     {...props}
 95 |   />
 96 | ))
 97 | DialogTitle.displayName = DialogPrimitive.Title.displayName
 98 | 
 99 | const DialogDescription = React.forwardRef<
100 |   React.ElementRef<typeof DialogPrimitive.Description>,
101 |   React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
102 | >(({ className, ...props }, ref) => (
103 |   <DialogPrimitive.Description
104 |     ref={ref}
105 |     className={cn("text-sm text-muted-foreground", className)}
106 |     {...props}
107 |   />
108 | ))
109 | DialogDescription.displayName = DialogPrimitive.Description.displayName
110 | 
111 | export {
112 |   Dialog,
113 |   DialogPortal,
114 |   DialogOverlay,
115 |   DialogTrigger,
116 |   DialogClose,
117 |   DialogContent,
118 |   DialogHeader,
119 |   DialogFooter,
120 |   DialogTitle,
121 |   DialogDescription,
122 | }
123 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ui/input.tsx:
--------------------------------------------------------------------------------
 1 | import * as React from "react"
 2 | 
 3 | import { cn } from "@/lib/utils"
 4 | 
 5 | export type InputProps = React.InputHTMLAttributes<HTMLInputElement>
 6 | 
 7 | const Input = React.forwardRef<HTMLInputElement, InputProps>(
 8 |   ({ className, type, ...props }, ref) => {
 9 |     return (
10 |       <input
11 |         type={type}
12 |         className={cn(
13 |           "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
14 |           className
15 |         )}
16 |         ref={ref}
17 |         {...props}
18 |       />
19 |     )
20 |   }
21 | )
22 | Input.displayName = "Input"
23 | 
24 | export { Input }
25 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ui/select.tsx:
--------------------------------------------------------------------------------
  1 | "use client"
  2 | 
  3 | import * as React from "react"
  4 | import {
  5 |   CaretSortIcon,
  6 |   CheckIcon,
  7 |   ChevronDownIcon,
  8 |   ChevronUpIcon,
  9 | } from "@radix-ui/react-icons"
 10 | import * as SelectPrimitive from "@radix-ui/react-select"
 11 | 
 12 | import { cn } from "@/lib/utils"
 13 | 
 14 | const Select = SelectPrimitive.Root
 15 | 
 16 | const SelectGroup = SelectPrimitive.Group
 17 | 
 18 | const SelectValue = SelectPrimitive.Value
 19 | 
 20 | const SelectTrigger = React.forwardRef<
 21 |   React.ElementRef<typeof SelectPrimitive.Trigger>,
 22 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
 23 | >(({ className, children, ...props }, ref) => (
 24 |   <SelectPrimitive.Trigger
 25 |     ref={ref}
 26 |     className={cn(
 27 |       "flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
 28 |       className
 29 |     )}
 30 |     {...props}
 31 |   >
 32 |     {children}
 33 |     <SelectPrimitive.Icon asChild>
 34 |       <CaretSortIcon className="h-4 w-4 opacity-50" />
 35 |     </SelectPrimitive.Icon>
 36 |   </SelectPrimitive.Trigger>
 37 | ))
 38 | SelectTrigger.displayName = SelectPrimitive.Trigger.displayName
 39 | 
 40 | const SelectScrollUpButton = React.forwardRef<
 41 |   React.ElementRef<typeof SelectPrimitive.ScrollUpButton>,
 42 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollUpButton>
 43 | >(({ className, ...props }, ref) => (
 44 |   <SelectPrimitive.ScrollUpButton
 45 |     ref={ref}
 46 |     className={cn(
 47 |       "flex cursor-default items-center justify-center py-1",
 48 |       className
 49 |     )}
 50 |     {...props}
 51 |   >
 52 |     <ChevronUpIcon />
 53 |   </SelectPrimitive.ScrollUpButton>
 54 | ))
 55 | SelectScrollUpButton.displayName = SelectPrimitive.ScrollUpButton.displayName
 56 | 
 57 | const SelectScrollDownButton = React.forwardRef<
 58 |   React.ElementRef<typeof SelectPrimitive.ScrollDownButton>,
 59 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollDownButton>
 60 | >(({ className, ...props }, ref) => (
 61 |   <SelectPrimitive.ScrollDownButton
 62 |     ref={ref}
 63 |     className={cn(
 64 |       "flex cursor-default items-center justify-center py-1",
 65 |       className
 66 |     )}
 67 |     {...props}
 68 |   >
 69 |     <ChevronDownIcon />
 70 |   </SelectPrimitive.ScrollDownButton>
 71 | ))
 72 | SelectScrollDownButton.displayName =
 73 |   SelectPrimitive.ScrollDownButton.displayName
 74 | 
 75 | const SelectContent = React.forwardRef<
 76 |   React.ElementRef<typeof SelectPrimitive.Content>,
 77 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
 78 | >(({ className, children, position = "popper", ...props }, ref) => (
 79 |   <SelectPrimitive.Portal>
 80 |     <SelectPrimitive.Content
 81 |       ref={ref}
 82 |       className={cn(
 83 |         "relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
 84 |         position === "popper" &&
 85 |           "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",
 86 |         className
 87 |       )}
 88 |       position={position}
 89 |       {...props}
 90 |     >
 91 |       <SelectScrollUpButton />
 92 |       <SelectPrimitive.Viewport
 93 |         className={cn(
 94 |           "p-1",
 95 |           position === "popper" &&
 96 |             "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]"
 97 |         )}
 98 |       >
 99 |         {children}
100 |       </SelectPrimitive.Viewport>
101 |       <SelectScrollDownButton />
102 |     </SelectPrimitive.Content>
103 |   </SelectPrimitive.Portal>
104 | ))
105 | SelectContent.displayName = SelectPrimitive.Content.displayName
106 | 
107 | const SelectLabel = React.forwardRef<
108 |   React.ElementRef<typeof SelectPrimitive.Label>,
109 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
110 | >(({ className, ...props }, ref) => (
111 |   <SelectPrimitive.Label
112 |     ref={ref}
113 |     className={cn("px-2 py-1.5 text-sm font-semibold", className)}
114 |     {...props}
115 |   />
116 | ))
117 | SelectLabel.displayName = SelectPrimitive.Label.displayName
118 | 
119 | const SelectItem = React.forwardRef<
120 |   React.ElementRef<typeof SelectPrimitive.Item>,
121 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
122 | >(({ className, children, ...props }, ref) => (
123 |   <SelectPrimitive.Item
124 |     ref={ref}
125 |     className={cn(
126 |       "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
127 |       className
128 |     )}
129 |     {...props}
130 |   >
131 |     <span className="absolute right-2 flex h-3.5 w-3.5 items-center justify-center">
132 |       <SelectPrimitive.ItemIndicator>
133 |         <CheckIcon className="h-4 w-4" />
134 |       </SelectPrimitive.ItemIndicator>
135 |     </span>
136 |     <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
137 |   </SelectPrimitive.Item>
138 | ))
139 | SelectItem.displayName = SelectPrimitive.Item.displayName
140 | 
141 | const SelectSeparator = React.forwardRef<
142 |   React.ElementRef<typeof SelectPrimitive.Separator>,
143 |   React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
144 | >(({ className, ...props }, ref) => (
145 |   <SelectPrimitive.Separator
146 |     ref={ref}
147 |     className={cn("-mx-1 my-1 h-px bg-muted", className)}
148 |     {...props}
149 |   />
150 | ))
151 | SelectSeparator.displayName = SelectPrimitive.Separator.displayName
152 | 
153 | export {
154 |   Select,
155 |   SelectGroup,
156 |   SelectValue,
157 |   SelectTrigger,
158 |   SelectContent,
159 |   SelectLabel,
160 |   SelectItem,
161 |   SelectSeparator,
162 |   SelectScrollUpButton,
163 |   SelectScrollDownButton,
164 | }
165 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/components/ui/textarea.tsx:
--------------------------------------------------------------------------------
 1 | import * as React from "react"
 2 | 
 3 | import { cn } from "@/lib/utils"
 4 | 
 5 | export type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement>
 6 | 
 7 | const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
 8 |   ({ className, ...props }, ref) => {
 9 |     return (
10 |       <textarea
11 |         className={cn(
12 |           "flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
13 |           className
14 |         )}
15 |         ref={ref}
16 |         {...props}
17 |       />
18 |     )
19 |   }
20 | )
21 | Textarea.displayName = "Textarea"
22 | 
23 | export { Textarea }
24 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/lib/model-selector-provider.tsx:
--------------------------------------------------------------------------------
 1 | "use client";
 2 | 
 3 | import React from "react";
 4 | import { createContext, useContext, useState, ReactNode } from "react";
 5 | 
 6 | type ModelSelectorContextType = {
 7 |   model: string;
 8 |   setModel: (model: string) => void;
 9 |   agent: string;
10 |   lgcDeploymentUrl?: string | null;
11 |   hidden: boolean;
12 |   setHidden: (hidden: boolean) => void;
13 | };
14 | 
15 | const ModelSelectorContext = createContext<
16 |   ModelSelectorContextType | undefined
17 | >(undefined);
18 | 
19 | export const ModelSelectorProvider = ({
20 |   children,
21 | }: {
22 |   children: ReactNode;
23 | }) => {
24 |   const model =
25 |     globalThis.window === undefined
26 |       ? "openai"
27 |       : new URL(window.location.href).searchParams.get("coAgentsModel") ??
28 |         "openai";
29 |   const [hidden, setHidden] = useState<boolean>(false);
30 | 
31 |   const setModel = (model: string) => {
32 |     const url = new URL(window.location.href);
33 |     url.searchParams.set("coAgentsModel", model);
34 |     window.location.href = url.toString();
35 |   };
36 | 
37 |   const lgcDeploymentUrl =
38 |     globalThis.window === undefined
39 |       ? null
40 |       : new URL(window.location.href).searchParams.get("lgcDeploymentUrl");
41 | 
42 |   let agent = "research_agent";
43 |   if (model === "google_genai") {
44 |     agent = "research_agent_google_genai";
45 |   } else if (model === "crewai") {
46 |     agent = "research_agent_crewai";
47 |   }
48 | 
49 |   return (
50 |     <ModelSelectorContext.Provider
51 |       value={{
52 |         model,
53 |         agent,
54 |         lgcDeploymentUrl,
55 |         hidden,
56 |         setModel,
57 |         setHidden,
58 |       }}
59 |     >
60 |       {children}
61 |     </ModelSelectorContext.Provider>
62 |   );
63 | };
64 | 
65 | export const useModelSelectorContext = () => {
66 |   const context = useContext(ModelSelectorContext);
67 |   if (context === undefined) {
68 |     throw new Error(
69 |       "useModelSelectorContext must be used within a ModelSelectorProvider"
70 |     );
71 |   }
72 |   return context;
73 | };
74 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/lib/types.ts:
--------------------------------------------------------------------------------
 1 | export type Resource = {
 2 |   url: string;
 3 |   title: string;
 4 |   description: string;
 5 | };
 6 | 
 7 | export type AgentState = {
 8 |   model: string;
 9 |   research_question: string;
10 |   report: string;
11 |   resources: any[];
12 |   logs: any[];
13 | }

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/src/lib/utils.ts:
--------------------------------------------------------------------------------
 1 | import { clsx, type ClassValue } from "clsx";
 2 | import { twMerge } from "tailwind-merge";
 3 | 
 4 | export function cn(...inputs: ClassValue[]) {
 5 |   return twMerge(clsx(inputs));
 6 | }
 7 | 
 8 | export const truncateUrl = (url: string, maxLength: number = 40) => {
 9 |   if (!url) return "";
10 |   if (url.length <= maxLength) return url;
11 |   return url.substring(0, maxLength - 3) + "...";
12 | };
13 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/tailwind.config.ts:
--------------------------------------------------------------------------------
 1 | import type { Config } from "tailwindcss";
 2 | 
 3 | const config: Config = {
 4 |     darkMode: ["class"],
 5 |     content: [
 6 |     "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
 7 |     "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
 8 |     "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
 9 |   ],
10 |   theme: {
11 |       extend: {
12 |           colors: {
13 |               background: 'hsl(var(--background))',
14 |               foreground: 'hsl(var(--foreground))',
15 |               card: {
16 |                   DEFAULT: 'hsl(var(--card))',
17 |                   foreground: 'hsl(var(--card-foreground))'
18 |               },
19 |               popover: {
20 |                   DEFAULT: 'hsl(var(--popover))',
21 |                   foreground: 'hsl(var(--popover-foreground))'
22 |               },
23 |               primary: {
24 |                   DEFAULT: 'hsl(var(--primary))',
25 |                   foreground: 'hsl(var(--primary-foreground))'
26 |               },
27 |               secondary: {
28 |                   DEFAULT: 'hsl(var(--secondary))',
29 |                   foreground: 'hsl(var(--secondary-foreground))'
30 |               },
31 |               muted: {
32 |                   DEFAULT: 'hsl(var(--muted))',
33 |                   foreground: 'hsl(var(--muted-foreground))'
34 |               },
35 |               accent: {
36 |                   DEFAULT: 'hsl(var(--accent))',
37 |                   foreground: 'hsl(var(--accent-foreground))'
38 |               },
39 |               destructive: {
40 |                   DEFAULT: 'hsl(var(--destructive))',
41 |                   foreground: 'hsl(var(--destructive-foreground))'
42 |               },
43 |               border: 'hsl(var(--border))',
44 |               input: 'hsl(var(--input))',
45 |               ring: 'hsl(var(--ring))',
46 |               chart: {
47 |                   '1': 'hsl(var(--chart-1))',
48 |                   '2': 'hsl(var(--chart-2))',
49 |                   '3': 'hsl(var(--chart-3))',
50 |                   '4': 'hsl(var(--chart-4))',
51 |                   '5': 'hsl(var(--chart-5))'
52 |               }
53 |           },
54 |           borderRadius: {
55 |               lg: 'var(--radius)',
56 |               md: 'calc(var(--radius) - 2px)',
57 |               sm: 'calc(var(--radius) - 4px)'
58 |           }
59 |       }
60 |   },
61 |   plugins: [require("tailwindcss-animate")],
62 | };
63 | export default config;
64 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/ui/tsconfig.json:
--------------------------------------------------------------------------------
 1 | {
 2 |   "compilerOptions": {
 3 |     "lib": [
 4 |       "dom",
 5 |       "dom.iterable",
 6 |       "esnext"
 7 |     ],
 8 |     "allowJs": true,
 9 |     "skipLibCheck": true,
10 |     "strict": true,
11 |     "noEmit": true,
12 |     "esModuleInterop": true,
13 |     "module": "esnext",
14 |     "moduleResolution": "bundler",
15 |     "resolveJsonModule": true,
16 |     "isolatedModules": true,
17 |     "jsx": "preserve",
18 |     "incremental": true,
19 |     "plugins": [
20 |       {
21 |         "name": "next"
22 |       }
23 |     ],
24 |     "paths": {
25 |       "@/*": [
26 |         "./src/*"
27 |       ]
28 |     },
29 |     "target": "ES2017"
30 |   },
31 |   "include": [
32 |     "next-env.d.ts",
33 |     "**/*.ts",
34 |     "**/*.tsx",
35 |     ".next/types/**/*.ts"
36 |   ],
37 |   "exclude": [
38 |     "node_modules"
39 |   ]
40 | }
41 | 

--------------------------------------------------------------------------------
/examples/coagents-research-canvas/wfcms-data.json:
--------------------------------------------------------------------------------
1 | {
2 |     "framework": "LangGraph",
3 |     "usecase": "Research, Planning, Human-in-the-loop",
4 |     "title": "Research Canvas",
5 |     "description": "A research canvas to help you plan, track, and organize your research.",
6 |     "live_demo": "https://examples-coagents-research-canvas-ui.vercel.app/",
7 |     "cover_img": "https://examples-coagents-research-canvas-ui.vercel.app/image.png"
8 | }

--------------------------------------------------------------------------------
```