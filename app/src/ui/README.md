# Legal Case Analysis Agent - Frontend UI

This is the Next.js frontend application for the Legal Case Analysis Agent. It provides the user interface for interacting with the backend agent to analyze legal cases, view generated reports, and chat about the findings.

This project utilizes [CopilotKit](https://github.com/CopilotKit/CopilotKit) for integrating the AI agent capabilities into the React frontend.

## Getting Started

Prerequisites:
*   Node.js and pnpm installed.
*   The backend Python agent (`../agent/`) should be running.

First, install dependencies:
```bash
pnpm install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) (or the configured port) with your browser to see the result.

The main UI logic can be found in `src/app/Main.tsx` and components within `src/components/`.

## Key Technologies

*   **Framework:** [Next.js](https://nextjs.org) (App Router)
*   **Language:** TypeScript
*   **UI:** [shadcn/ui](https://ui.shadcn.com/), [Tailwind CSS](https://tailwindcss.com/)
*   **AI Integration:** [@copilotkit/react-core](https://docs.copilotkit.ai/), [@copilotkit/react-ui](https://docs.copilotkit.ai/)
*   **Styling:** Tailwind CSS
*   **Font:** [Geist](https://vercel.com/font) (via `next/font`)

## Learn More about Next.js

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
